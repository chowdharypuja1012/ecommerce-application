from django.contrib import admin
from .models import ProductReview


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "product_id", "rating", "title", "is_approved", "created_at")
    list_filter = ("rating", "is_approved", "created_at")
    search_fields = ("user__username", "product_id", "title", "comment")
    readonly_fields = ("created_at", "updated_at")
