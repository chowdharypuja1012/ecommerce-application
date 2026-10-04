from decimal import Decimal
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Cart(models.Model):
    """
    Cart model representing a user's shopping cart.
    Enforces ONE active cart per user at a time via unique constraint.
    """
    STATUS_CHOICES = (
        ("active", "Active"),
        ("completed", "Completed"),
        ("abandoned", "Abandoned"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="carts")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active", db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Shopping Cart"
        verbose_name_plural = "Shopping Carts"
        ordering = ["-updated_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["user"],
                condition=models.Q(status="active"),
                name="unique_active_cart_per_user",
            ),
        ]

    def __str__(self) -> str:
        return f"Cart ({self.status}) of {self.user.username}"

    @property
    def subtotal(self) -> Decimal:
        """Server-calculated total price of all items in cart."""
        return sum((item.line_total for item in self.items.all()), Decimal("0.00"))

    @property
    def total_items(self) -> int:
        """Total quantity of all items in cart."""
        return sum((item.quantity for item in self.items.all()), 0)


class CartItem(models.Model):
    """
    CartItem model representing a product added to a Cart.
    Stores reference to Catalogue product, server-validated unit price, and quantity.
    """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product_id = models.IntegerField(db_index=True)
    product_sku = models.CharField(max_length=100, db_index=True)
    product_name = models.CharField(max_length=255)
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"
        ordering = ["created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["cart", "product_id"],
                name="unique_product_per_cart",
            ),
            models.CheckConstraint(
                condition=models.Q(quantity__gte=1),
                name="cart_item_quantity_gte_1",
            ),
            models.CheckConstraint(
                condition=models.Q(unit_price__gte=Decimal("0.00")),
                name="cart_item_unit_price_gte_0",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.quantity}x {self.product_name} in Cart #{self.cart.id}"

    @property
    def line_total(self) -> Decimal:
        """Server-calculated line total (unit_price * quantity)."""
        return self.unit_price * Decimal(self.quantity)
