from django.contrib import admin
from .models import PaymentTransaction


@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ("transaction_reference", "user", "order_id", "amount", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("transaction_reference", "user__username", "order_id", "idempotency_key")
    readonly_fields = ("transaction_reference", "created_at", "updated_at")
