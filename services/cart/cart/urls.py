from django.contrib import admin
from django.urls import path
from .health import make_health_view
from .views import (
    AddCartItemView,
    CartDetailView,
    ClearCartView,
    UpdateDestroyCartItemView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/health/", make_health_view("cart"), name="health"),

    # Cart endpoints
    path("api/v1/cart/", CartDetailView.as_view(), name="cart-detail"),
    path("api/v1/cart/items/", AddCartItemView.as_view(), name="cart-item-add"),
    path("api/v1/cart/items/<int:pk>/", UpdateDestroyCartItemView.as_view(), name="cart-item-detail"),
    path("api/v1/cart/clear/", ClearCartView.as_view(), name="cart-clear"),
]
