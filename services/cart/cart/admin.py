from django.contrib import admin
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ("product_id", "product_sku", "product_name", "unit_price", "line_total", "created_at")


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "status", "total_items", "subtotal", "created_at", "updated_at")
    list_filter = ("status", "created_at")
    search_fields = ("user__username", "user__email")
    inlines = [CartItemInline]
    readonly_fields = ("subtotal", "total_items")


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("id", "cart", "product_name", "product_sku", "unit_price", "quantity", "line_total", "created_at")
    search_fields = ("product_name", "product_sku", "cart__user__username")
    readonly_fields = ("line_total",)
