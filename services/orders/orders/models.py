import uuid
from decimal import Decimal
from django.db import models
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

User = get_user_model()


class OrderStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    PAID = "PAID", "Paid"
    SHIPPED = "SHIPPED", "Shipped"
    DELIVERED = "DELIVERED", "Delivered"
    CANCELLED = "CANCELLED", "Cancelled"


def generate_order_number():
    return f"ORD-{uuid.uuid4().hex[:12].upper()}"


# Allowed status transitions map
ALLOWED_TRANSITIONS = {
    OrderStatus.PENDING: [OrderStatus.PAID, OrderStatus.CANCELLED],
    OrderStatus.PAID: [OrderStatus.SHIPPED, OrderStatus.CANCELLED],
    OrderStatus.SHIPPED: [OrderStatus.DELIVERED],
    OrderStatus.DELIVERED: [],
    OrderStatus.CANCELLED: [],
}


class Order(models.Model):
    """
    Purchase Order representation. Captures purchase-time product name/price snapshots,
    shipping address details, and order status transitions.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    order_number = models.CharField(max_length=32, unique=True, default=generate_order_number, editable=False)
    status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING)

    # Shipping Address Snapshot
    shipping_full_name = models.CharField(max_length=150)
    shipping_street_address = models.CharField(max_length=255)
    shipping_city = models.CharField(max_length=100)
    shipping_state = models.CharField(max_length=100)
    shipping_postal_code = models.CharField(max_length=20)
    shipping_country = models.CharField(max_length=100)
    shipping_phone = models.CharField(max_length=20, blank=True, default="")

    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order {self.order_number} ({self.user.username}) - {self.status}"

    def can_transition_to(self, new_status: str) -> bool:
        """Checks if transition from current status to target status is valid."""
        allowed = ALLOWED_TRANSITIONS.get(self.status, [])
        return new_status in allowed

    def transition_to(self, new_status: str):
        """
        Executes order status transition. Raises ValidationError if transition is illegal.
        """
        if self.status == new_status:
            return  # No-op if status is unchanged

        if not self.can_transition_to(new_status):
            raise ValidationError(
                {"status": f"Invalid status transition from '{self.status}' to '{new_status}'."}
            )

        self.status = new_status
        self.save(update_fields=["status", "updated_at"])


class OrderItem(models.Model):
    """
    Snapshot of an individual product item inside an order at time of purchase.
    Preserves exact purchase-time unit price and product details.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product_id = models.PositiveIntegerField()
    product_sku = models.CharField(max_length=64)
    product_name = models.CharField(max_length=255)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    line_total = models.DecimalField(max_digits=12, decimal_places=2)

    def save(self, *args, **kwargs):
        self.line_total = self.unit_price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"OrderItem {self.product_name} x{self.quantity} (${self.line_total})"
