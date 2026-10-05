from decimal import Decimal, InvalidOperation
from django.db import transaction
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAdminUser
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


# ── ADMIN OPERATIONS ─────────────────────────────────────────────────────────

class AdminProductCreateView(APIView):
    """
    POST /api/v1/catalogue/admin/products/
    Admin-only workflow for creating a new product.
    Enforces server-side IsAdminUser permission.
    """
    permission_classes = [IsAdminUser]

    def post(self, request):
        data = request.data
        name = data.get("name")
        sku = data.get("sku")
        price = data.get("price")
        stock = data.get("stock", 0)
        category_id = data.get("category_id")

        if not name or not sku or price is None:
            return Response(
                {"detail": "name, sku, and price are required fields."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        category = None
        if category_id:
            category = Category.objects.filter(id=category_id).first()

        from django.utils.text import slugify
        product = Product.objects.create(
            category=category,
            name=name,
            slug=slugify(name),
            sku=sku,
            description=data.get("description", ""),
            price=Decimal(str(price)),
            stock=int(stock),
            is_active=data.get("is_active", True),
            image_url=data.get("image_url", ""),
        )

        serializer = ProductDetailSerializer(product)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AdminProductUpdateDeleteView(APIView):
    """
    PATCH / DELETE /api/v1/catalogue/admin/products/<int:pk>/
    Admin-only workflow for updating inventory stock, price, or deleting a product.
    """
    permission_classes = [IsAdminUser]

    def patch(self, request, pk):
        product = Product.objects.filter(pk=pk).first()
        if not product:
            return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

        data = request.data
        if "price" in data:
            product.price = Decimal(str(data["price"]))
        if "stock" in data:
            product.stock = int(data["stock"])
        if "is_active" in data:
            product.is_active = bool(data["is_active"])
        if "name" in data:
            product.name = data["name"]
        if "description" in data:
            product.description = data["description"]

        product.save()
        serializer = ProductDetailSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        product = Product.objects.filter(pk=pk).first()
        if not product:
            return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

        product.is_active = False
        product.save(update_fields=["is_active"])
        return Response({"detail": f"Product '{product.name}' archived successfully."}, status=status.HTTP_200_OK)


class AdminLowStockAlertsView(APIView):
    """
    GET /api/v1/catalogue/admin/inventory/low-stock/
    Admin-only endpoint returning products with stock below threshold (default < 5).
    """
    permission_classes = [IsAdminUser]

    def get(self, request):
        threshold = int(request.query_params.get("threshold", 5))
        low_stock_products = Product.objects.filter(is_active=True, stock__lt=threshold)
        serializer = ProductListSerializer(low_stock_products, many=True)
        return Response({
            "threshold": threshold,
            "total_low_stock": low_stock_products.count(),
            "products": serializer.data,
        }, status=status.HTTP_200_OK)


# ── INVENTORY TRANSACTIONS (Order Placements & Cancellations) ────────────────

class InventoryDeductView(APIView):
    """
    POST /api/v1/catalogue/inventory/deduct/
    Atomic batch inventory deduction with row-level locks (select_for_update).
    Expects payload: {"items": [{"product_id": int, "quantity": int}, ...]}
    """
    permission_classes = [AllowAny]

    def post(self, request):
        items = request.data.get("items", [])
        if not items:
            return Response(
                {"error": "No items provided for stock deduction."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        updated_items = []
        try:
            with transaction.atomic():
                for item in items:
                    product_id = item.get("product_id")
                    quantity = int(item.get("quantity", 0))

                    if quantity <= 0:
                        continue

                    product = Product.objects.select_for_update().filter(id=product_id).first()
                    if not product:
                        return Response(
                            {"error": f"Product #{product_id} does not exist."},
                            status=status.HTTP_404_NOT_FOUND,
                        )

                    if product.stock < quantity:
                        return Response(
                            {
                                "error": f"Insufficient stock for '{product.name}'. Requested {quantity}, but only {product.stock} available.",
                                "product_id": product.id,
                                "available_stock": product.stock,
                            },
                            status=status.HTTP_400_BAD_REQUEST,
                        )

                    product.stock -= quantity
                    product.save(update_fields=["stock"])
                    updated_items.append({
                        "product_id": product.id,
                        "product_name": product.name,
                        "new_stock": product.stock,
                    })

            return Response({
                "success": True,
                "message": "Inventory stock deducted successfully.",
                "updated_items": updated_items,
            }, status=status.HTTP_200_OK)

        except Exception as exc:
            return Response(
                {"error": f"Failed to deduct inventory stock: {str(exc)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class InventoryRestoreView(APIView):
    """
    POST /api/v1/catalogue/inventory/restore/
    Atomic batch inventory restoration for cancelled/refunded orders.
    Expects payload: {"items": [{"product_id": int, "quantity": int}, ...]}
    """
    permission_classes = [AllowAny]

    def post(self, request):
        items = request.data.get("items", [])
        if not items:
            return Response(
                {"error": "No items provided for stock restoration."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        updated_items = []
        try:
            with transaction.atomic():
                for item in items:
                    product_id = item.get("product_id")
                    quantity = int(item.get("quantity", 0))

                    if quantity <= 0:
                        continue

                    product = Product.objects.select_for_update().filter(id=product_id).first()
                    if product:
                        product.stock += quantity
                        product.save(update_fields=["stock"])
                        updated_items.append({
                            "product_id": product.id,
                            "product_name": product.name,
                            "new_stock": product.stock,
                        })

            return Response({
                "success": True,
                "message": "Inventory stock restored successfully.",
                "updated_items": updated_items,
            }, status=status.HTTP_200_OK)

        except Exception as exc:
            return Response(
                {"error": f"Failed to restore inventory stock: {str(exc)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

