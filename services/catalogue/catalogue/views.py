from decimal import Decimal, InvalidOperation
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Category, Product
from .pagination import StandardResultsSetPagination
from .serializers import (
    CategorySerializer,
    ProductDetailSerializer,
    ProductListSerializer,
)


class CategoryListView(ListAPIView):
    """
    GET /api/v1/categories/
    Returns list of active categories.
    Public read-only access.
    """
    permission_classes = [AllowAny]
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(is_active=True).order_by("name")


class CategoryDetailView(RetrieveAPIView):
    """
    GET /api/v1/categories/<slug>/
    Returns detail for a single active category by slug.
    Public read-only access.
    """
    permission_classes = [AllowAny]
    serializer_class = CategorySerializer
    lookup_field = "slug"

    def get_queryset(self):
        return Category.objects.filter(is_active=True)


class ProductListView(APIView):
    """
    GET /api/v1/products/
    Returns paginated list of active products.
    Supports:
    - Search: ?search=keyword (matches name, description, SKU)
    - Category filter: ?category=slug or ?category_id=id
    - Price range: ?min_price=X & ?max_price=Y (validates numeric values)
    - Sorting: ?ordering=price | -price | name | -name | created_at | -created_at
    """
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination

    ALLOWED_ORDERINGS = {
        "price": "price",
        "-price": "-price",
        "name": "name",
        "-name": "-name",
        "created_at": "created_at",
        "-created_at": "-created_at",
    }

    def get(self, request):
        queryset = Product.objects.filter(is_active=True).select_related("category")
        errors = {}

        # 1. Search filter
        search_query = request.query_params.get("search", "").strip()
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query)
                | Q(description__icontains=search_query)
                | Q(sku__icontains=search_query)
            )

        # 2. Category filter
        category_slug = request.query_params.get("category", "").strip()
        category_id = request.query_params.get("category_id", "").strip()

        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        elif category_id:
            if not category_id.isdigit():
                errors["category_id"] = "category_id must be a valid integer."
            else:
                queryset = queryset.filter(category_id=int(category_id))

        # 3. Min Price filter
        min_price_str = request.query_params.get("min_price")
        if min_price_str is not None and min_price_str.strip() != "":
            try:
                min_price = Decimal(min_price_str.strip())
                if min_price < Decimal("0.00"):
                    errors["min_price"] = "min_price must be a non-negative decimal number."
                else:
                    queryset = queryset.filter(price__gte=min_price)
            except (InvalidOperation, ValueError):
                errors["min_price"] = "min_price must be a valid numeric decimal value."

        # 4. Max Price filter
        max_price_str = request.query_params.get("max_price")
        if max_price_str is not None and max_price_str.strip() != "":
            try:
                max_price = Decimal(max_price_str.strip())
                if max_price < Decimal("0.00"):
                    errors["max_price"] = "max_price must be a non-negative decimal number."
                else:
                    queryset = queryset.filter(price__lte=max_price)
            except (InvalidOperation, ValueError):
                errors["max_price"] = "max_price must be a valid numeric decimal value."

        # If price validation failed, return 400 Bad Request
        if errors:
            return Response(
                {"error": "Invalid filter parameters", "details": errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 5. Sorting
        ordering = request.query_params.get("ordering", "-created_at").strip()
        if ordering in self.ALLOWED_ORDERINGS:
            queryset = queryset.order_by(self.ALLOWED_ORDERINGS[ordering])
        else:
            queryset = queryset.order_by("-created_at")

        # 6. Pagination
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request, view=self)
        if page is not None:
            serializer = ProductListSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = ProductListSerializer(queryset, many=True)
        return Response(serializer.data)


class ProductDetailView(APIView):
    """
    GET /api/v1/products/<slug>/
    Returns detail for a single active product by slug (or integer ID).
    Public read-only access.
    """
    permission_classes = [AllowAny]

    def get(self, request, slug):
        queryset = Product.objects.filter(is_active=True).select_related("category")
        
        # Try slug lookup first, then id lookup if slug is digit
        product = queryset.filter(slug=slug).first()
        if not product and slug.isdigit():
            product = queryset.filter(id=int(slug)).first()

        if not product:
            return Response(
                {"detail": "Product not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = ProductDetailSerializer(product)
        return Response(serializer.data)
