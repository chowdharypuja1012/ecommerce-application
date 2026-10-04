from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


class ProductReview(models.Model):
    """
    Customer product review and rating (1 to 5 stars).
    Enforces rating range validation (1 <= rating <= 5) and prevents duplicate
    reviews per user per product.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    product_id = models.PositiveIntegerField()

    rating = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, message="Rating must be at least 1 star."),
            MaxValueValidator(5, message="Rating cannot exceed 5 stars."),
        ]
    )
    title = models.CharField(max_length=150, blank=True, default="")
    comment = models.TextField(blank=True, default="")
    is_approved = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "product_id"],
                name="unique_user_product_review"
            )
        ]

    def __str__(self):
        return f"Review by {self.user.username} for Product #{self.product_id} ({self.rating}★)"
