from django.contrib import admin
from django.urls import path
from .health import make_health_view
from .views import (
    CheckoutPreviewView,
    CheckoutCreateOrderView,
    OrderListView,
    OrderDetailView,
    OrderCancelView,
    OrderStatusUpdateView,
    AdminAllOrdersView,
    AdminOrderMetricsView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/health/", make_health_view("orders"), name="health"),
    path("api/v1/checkout/preview/", CheckoutPreviewView.as_view(), name="checkout-preview"),
    path("api/v1/checkout/", CheckoutCreateOrderView.as_view(), name="checkout-create"),
    path("api/v1/orders/", OrderListView.as_view(), name="order-list"),
    path("api/v1/orders/<int:pk>/", OrderDetailView.as_view(), name="order-detail"),
    path("api/v1/orders/<int:pk>/cancel/", OrderCancelView.as_view(), name="order-cancel"),
    path("api/v1/orders/<int:pk>/status/", OrderStatusUpdateView.as_view(), name="order-status-update"),

    # Admin Protected Routes
    path("api/v1/orders/admin/all/", AdminAllOrdersView.as_view(), name="orders-admin-all"),
    path("api/v1/orders/admin/metrics/", AdminOrderMetricsView.as_view(), name="orders-admin-metrics"),
]
