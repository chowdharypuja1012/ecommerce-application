from django.contrib import admin
from django.urls import path
from .health import make_health_view
from .views import (
    CheckoutPreviewView,
    CheckoutCreateOrderView,
    OrderListView,
    OrderDetailView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/health/", make_health_view("orders"), name="health"),
    path("api/v1/checkout/preview/", CheckoutPreviewView.as_view(), name="checkout-preview"),
    path("api/v1/checkout/", CheckoutCreateOrderView.as_view(), name="checkout-create"),
    path("api/v1/orders/", OrderListView.as_view(), name="order-list"),
    path("api/v1/orders/<int:pk>/", OrderDetailView.as_view(), name="order-detail"),
]
