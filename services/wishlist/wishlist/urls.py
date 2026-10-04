from django.contrib import admin
from django.urls import path
from .health import make_health_view
from .views import (
    WishlistDetailView,
    AddWishlistItemView,
    RemoveWishlistItemView,
    RemoveWishlistItemByProductView,
    ClearWishlistView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/health/", make_health_view("wishlist"), name="health"),
    path("api/v1/wishlist/", WishlistDetailView.as_view(), name="wishlist-detail"),
    path("api/v1/wishlist/items/", AddWishlistItemView.as_view(), name="wishlist-add-item"),
    path("api/v1/wishlist/items/<int:pk>/", RemoveWishlistItemView.as_view(), name="wishlist-remove-item"),
    path("api/v1/wishlist/items/by-product/<int:product_id>/", RemoveWishlistItemByProductView.as_view(), name="wishlist-remove-by-product"),
    path("api/v1/wishlist/clear/", ClearWishlistView.as_view(), name="wishlist-clear"),
]
