from decimal import Decimal
from rest_framework import serializers
from .models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    """Serializer for CartItem model with server-calculated line_total."""
    line_total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    unit_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = CartItem
        fields = (
            "id",
            "product_id",
            "product_sku",
            "product_name",
            "unit_price",
            "quantity",
            "line_total",
            "created_at",
            "updated_at",
        )
        read_only_fields = fields


class AddCartItemSerializer(serializers.Serializer):
    """
    Serializer for adding item to cart.
    Accepts product_id and quantity.
    Client-provided prices are intentionally IGNORED to prevent price tampering.
    """
    product_id = serializers.IntegerField(min_value=1)
    quantity = serializers.IntegerField(min_value=1, default=1)


class UpdateCartItemSerializer(serializers.Serializer):
    """Serializer for updating item quantity in cart."""
    quantity = serializers.IntegerField(min_value=0)


class CartSerializer(serializers.ModelSerializer):
    """Serializer for Cart model with nested items and server-calculated totals."""
    items = CartItemSerializer(many=True, read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    total_items = serializers.IntegerField(read_only=True)

    class Meta:
        model = Cart
        fields = (
            "id",
            "status",
            "items",
            "subtotal",
            "total_items",
            "created_at",
            "updated_at",
        )
        read_only_fields = fields
