from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db import models
from django.core.exceptions import ValidationError


class Category(models.Model):
    """
    Category model representing product groupings in the catalogue.
    """
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    description = models.TextField(blank=True, default="")
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self) -> str:
        return self.name

    def clean(self):
        super().clean()
        if self.name:
            self.name = self.name.strip()


class Product(models.Model):
    """
    Product model representing item listings in the catalogue.
    Includes price, SKU, stock quantity, active status, and optional category/image.
    """
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products",
    )
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    description = models.TextField(blank=True, default="")
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    sku = models.CharField(max_length=100, unique=True, db_index=True)
    stock = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
    )
    is_active = models.BooleanField(default=True, db_index=True)
    image_url = models.URLField(max_length=500, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["sku"]),
            models.Index(fields=["slug"]),
            models.Index(fields=["is_active"]),
            models.Index(fields=["created_at"]),
        ]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(price__gte=Decimal("0.00")),
                name="catalogue_product_price_gte_0",
            ),
            models.CheckConstraint(
                condition=models.Q(stock__gte=0),
                name="catalogue_product_stock_gte_0",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.name} ({self.sku})"

    def clean(self):
        super().clean()
        if self.price is not None and self.price < Decimal("0.00"):
            raise ValidationError({"price": "Price cannot be negative."})
        if self.stock is not None and self.stock < 0:
            raise ValidationError({"stock": "Stock cannot be negative."})
