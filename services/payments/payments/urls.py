from django.contrib import admin
from django.urls import path
from .health import make_health_view
from .views import (
    ProcessPaymentView,
    PaymentWebhookCallbackView,
    PaymentOrderTransactionsView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/health/", make_health_view("payments"), name="health"),
    path("api/v1/payments/process/", ProcessPaymentView.as_view(), name="payment-process"),
    path("api/v1/payments/webhook/", PaymentWebhookCallbackView.as_view(), name="payment-webhook"),
    path("api/v1/payments/order/<int:order_id>/", PaymentOrderTransactionsView.as_view(), name="payment-order-history"),
]
