from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .catalogue_service import fetch_and_validate_product
from .models import Cart, CartItem
from .serializers import (
    AddCartItemSerializer,
    CartSerializer,
    UpdateCartItemSerializer,
)


def get_or_create_active_cart(user) -> Cart:
    """Helper to retrieve or create the single active cart for a user."""
    cart, _ = Cart.objects.get_or_create(user=user, status="active")
    return cart


class CartDetailView(APIView):
    """
    GET /api/v1/cart/
    Returns current authenticated user's active cart with server-calculated subtotals.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart = get_or_create_active_cart(request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddCartItemView(APIView):
    """
    POST /api/v1/cart/items/
    Adds an item to the current user's active cart.
    Validates product active status, stock availability, and live unit price server-side.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AddCartItemSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        product_id = serializer.validated_data["product_id"]
        add_quantity = serializer.validated_data["quantity"]

        cart = get_or_create_active_cart(request.user)
        existing_item = cart.items.filter(product_id=product_id).first()
        target_quantity = add_quantity + (existing_item.quantity if existing_item else 0)

        # Server-side validation against Catalogue service
        prod_data = fetch_and_validate_product(product_id, target_quantity)

        if existing_item:
            existing_item.quantity = target_quantity
            existing_item.unit_price = prod_data["unit_price"]  # Always refresh live price
            existing_item.save()
        else:
            CartItem.objects.create(
                cart=cart,
                product_id=prod_data["id"],
                product_sku=prod_data["sku"],
                product_name=prod_data["name"],
                unit_price=prod_data["unit_price"],
                quantity=target_quantity,
            )

        cart.refresh_from_db()
        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)


class UpdateDestroyCartItemView(APIView):
    """
    PATCH/PUT /api/v1/cart/items/<id>/
    DELETE /api/v1/cart/items/<id>/
    Updates or deletes a specific item in the user's cart.
    Strictly enforces user ownership (404/403 if item belongs to another user's cart).
    """
    permission_classes = [IsAuthenticated]

    def _get_item(self, request, pk: int) -> CartItem:
        item = CartItem.objects.filter(pk=pk).select_related("cart").first()
        if not item:
            raise NotFound("Cart item not found.")
        if item.cart.user != request.user:
            raise PermissionDenied("You do not have permission to modify this cart item.")
        return item

    def patch(self, request, pk: int):
        return self._update_item(request, pk)

    def put(self, request, pk: int):
        return self._update_item(request, pk)

    def _update_item(self, request, pk: int):
        item = self._get_item(request, pk)
        serializer = UpdateCartItemSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        new_quantity = serializer.validated_data["quantity"]

        if new_quantity <= 0:
            item.delete()
        else:
            # Validate stock against Catalogue service
            prod_data = fetch_and_validate_product(item.product_id, new_quantity)
            item.quantity = new_quantity
            item.unit_price = prod_data["unit_price"]  # Always refresh live price
            item.save()

        cart = get_or_create_active_cart(request.user)
        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)

    def delete(self, request, pk: int):
        item = self._get_item(request, pk)
        item.delete()
        cart = get_or_create_active_cart(request.user)
        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)


class ClearCartView(APIView):
    """
    POST /api/v1/cart/clear/
    Empties all items from the current user's active cart.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart = get_or_create_active_cart(request.user)
        cart.items.all().delete()
        cart.refresh_from_db()
        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)
