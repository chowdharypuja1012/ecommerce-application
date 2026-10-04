from rest_framework import serializers
from .models import ProductReview


class ProductReviewSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = ProductReview
        fields = ["id", "username", "product_id", "rating", "title", "comment", "is_approved", "created_at"]
        read_only_fields = ["id", "username", "is_approved", "created_at"]

    def get_username(self, obj):
        return obj.user.username

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be an integer between 1 and 5 stars.")
        return value
