import uuid
from decimal import Decimal
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class PaymentStatus(models.TextChoices):
    INITIATED = "INITIATED", "Initiated"
    SUCCESS = "SUCCESS", "Success"
    FAILED = "FAILED", "Failed"
    CANCELLED = "CANCELLED", "Cancelled"


def generate_transaction_ref():
    return f"PAY-SIM-{uuid.uuid4().hex[:12].upper()}"


class PaymentTransaction(models.Model):
    """
    Simulated Payment Sandbox Transaction audit log.
    Stores provider references and status codes ONLY.
    SECURITY MANDATE: NEVER STORE CARD NUMBERS, CVVs, OR EXPIRATION DATES.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payment_transactions")
    order_id = models.PositiveIntegerField()
    transaction_reference = models.CharField(max_length=64, unique=True, default=generate_transaction_ref, editable=False)
    idempotency_key = models.CharField(max_length=64, unique=True, null=True, blank=True)

    amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    currency = models.CharField(max_length=3, default="USD")
    payment_method = models.CharField(max_length=32, default="SIMULATED_SANDBOX")

    status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.INITIATED)
    provider_status_code = models.CharField(max_length=32, blank=True, default="SIM_200_OK")
    provider_message = models.TextField(blank=True, default="Simulated payment sandbox transaction.")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Payment {self.transaction_reference} (Order #{self.order_id}) - {self.status}"
