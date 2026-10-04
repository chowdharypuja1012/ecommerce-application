from rest_framework import serializers
from .models import Wishlist, WishlistItem
from .catalogue_service import fetch_product_details


class WishlistItemSerializer(serializers.ModelSerializer):
    product_details = serializers.SerializerMethodField()

    class Meta:
        model = WishlistItem
        fields = ["id", "product_id", "added_at", "product_details"]
        read_only_fields = ["id", "added_at", "product_details"]

    def get_product_details(self, obj):
        return fetch_product_details(obj.product_id)


class WishlistSerializer(serializers.ModelSerializer):
    items = WishlistItemSerializer(many=True, read_only=True)
    total_items = serializers.IntegerField(read_only=True)

    class Meta:
        model = Wishlist
        fields = ["id", "total_items", "created_at", "updated_at", "items"]
        read_only_fields = ["id", "total_items", "created_at", "updated_at", "items"]
