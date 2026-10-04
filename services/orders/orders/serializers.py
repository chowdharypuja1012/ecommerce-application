from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["id", "product_id", "product_sku", "product_name", "unit_price", "quantity", "line_total"]
        read_only_fields = ["id", "product_id", "product_sku", "product_name", "unit_price", "quantity", "line_total"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "order_number",
            "status",
            "total_amount",
            "shipping_full_name",
            "shipping_street_address",
            "shipping_city",
            "shipping_state",
            "shipping_postal_code",
            "shipping_country",
            "shipping_phone",
            "created_at",
            "updated_at",
            "items",
        ]
        read_only_fields = fields


class CheckoutInputSerializer(serializers.Serializer):
    shipping_full_name = serializers.CharField(max_length=150, required=True)
    shipping_street_address = serializers.CharField(max_length=255, required=True)
    shipping_city = serializers.CharField(max_length=100, required=True)
    shipping_state = serializers.CharField(max_length=100, required=True)
    shipping_postal_code = serializers.CharField(max_length=20, required=True)
    shipping_country = serializers.CharField(max_length=100, required=True)
    shipping_phone = serializers.CharField(max_length=20, required=False, allow_blank=True, default="")

    def validate_shipping_full_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Shipping full name cannot be blank.")
        return value.strip()

    def validate_shipping_street_address(self, value):
        if not value.strip():
            raise serializers.ValidationError("Shipping street address cannot be blank.")
        return value.strip()
