from rest_framework import serializers
from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model."""
    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "slug",
            "description",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = fields


class CategorySummarySerializer(serializers.ModelSerializer):
    """Compact serializer for embedded Category details in Product list."""
    class Meta:
        model = Category
        fields = ("id", "name", "slug")
        read_only_fields = fields


class ProductListSerializer(serializers.ModelSerializer):
    """Serializer for product list view with category summary."""
    category = CategorySummarySerializer(read_only=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, coerce_to_string=True)

    class Meta:
        model = Product
        fields = (
            "id",
            "category",
            "name",
            "slug",
            "description",
            "price",
            "sku",
            "stock",
            "is_active",
            "image_url",
            "created_at",
        )
        read_only_fields = fields


class ProductDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for single product view."""
    category = CategorySerializer(read_only=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, coerce_to_string=True)

    class Meta:
        model = Product
        fields = (
            "id",
            "category",
            "name",
            "slug",
            "description",
            "price",
            "sku",
            "stock",
            "is_active",
            "image_url",
            "created_at",
            "updated_at",
        )
        read_only_fields = fields
