from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Wishlist(models.Model):
    """
    User's wishlist container. Strictly enforced one active wishlist per user.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="wishlist")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Wishlist ({self.user.username})"

    @property
    def total_items(self):
        return self.items.count()


class WishlistItem(models.Model):
    """
    Individual item in user's wishlist linking to product_id from Catalogue service.
    Enforces uniqueness per wishlist to prevent duplicate entries.
    """
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name="items")
    product_id = models.PositiveIntegerField()
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-added_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["wishlist", "product_id"],
                name="unique_wishlist_product"
            )
        ]

    def __str__(self):
        return f"WishlistItem (Wishlist #{self.wishlist_id}, Product #{self.product_id})"
