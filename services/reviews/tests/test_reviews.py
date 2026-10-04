from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from reviews.models import ProductReview

User = get_user_model()


class ProductReviewsAPITestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="alice", password="password123")
        self.token1 = Token.objects.create(user=self.user1)

        self.user2 = User.objects.create_user(username="bob", password="password123")
        self.token2 = Token.objects.create(user=self.user2)

        self.admin = User.objects.create_user(username="admin", password="password123", is_staff=True)
        self.admin_token = Token.objects.create(user=self.admin)

    def test_public_read_approved_reviews(self):
        ProductReview.objects.create(user=self.user1, product_id=10, rating=5, comment="Great product!")
        ProductReview.objects.create(user=self.user2, product_id=10, rating=3, comment="Average performance.")

        response = self.client.get("/api/v1/reviews/product/10/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_reviews"], 2)
        self.assertEqual(response.data["average_rating"], 4.0)
        self.assertEqual(response.data["rating_distribution"]["5"], 1)
        self.assertEqual(response.data["rating_distribution"]["3"], 1)

    def test_rating_boundaries_validation(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token1.key}")

        # Invalid rating: 0 stars
        res_low = self.client.post("/api/v1/reviews/", {"product_id": 101, "rating": 0, "comment": "Too low"}, format="json")
        self.assertEqual(res_low.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("rating", str(res_low.data))

        # Invalid rating: 6 stars
        res_high = self.client.post("/api/v1/reviews/", {"product_id": 101, "rating": 6, "comment": "Too high"}, format="json")
        self.assertEqual(res_high.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("rating", str(res_high.data))

        # Valid rating: 5 stars
        res_valid = self.client.post("/api/v1/reviews/", {"product_id": 101, "rating": 5, "comment": "Perfect"}, format="json")
        self.assertEqual(res_valid.status_code, status.HTTP_201_CREATED)

    def test_prevent_duplicate_review_per_user_and_product(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token1.key}")

        # First review submission succeeds
        res1 = self.client.post("/api/v1/reviews/", {"product_id": 202, "rating": 4, "comment": "Nice"}, format="json")
        self.assertEqual(res1.status_code, status.HTTP_201_CREATED)

        # Second review submission for same product by same user fails
        with transaction.atomic():
            res2 = self.client.post("/api/v1/reviews/", {"product_id": 202, "rating": 5, "comment": "Duplicate"}, format="json")
        self.assertEqual(res2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("already submitted a review", str(res2.data))

    def test_user_can_update_or_delete_own_review(self):
        review = ProductReview.objects.create(user=self.user1, product_id=303, rating=2, comment="Bad quality")

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token1.key}")

        # Update rating & comment
        res_patch = self.client.patch(f"/api/v1/reviews/{review.id}/", {"rating": 4, "comment": "Better after update"}, format="json")
        self.assertEqual(res_patch.status_code, status.HTTP_200_OK)
        self.assertEqual(res_patch.data["rating"], 4)

        # Delete review
        res_del = self.client.delete(f"/api/v1/reviews/{review.id}/")
        self.assertEqual(res_del.status_code, status.HTTP_200_OK)
        self.assertFalse(ProductReview.objects.filter(id=review.id).exists())

    def test_admin_review_moderation(self):
        review = ProductReview.objects.create(user=self.user1, product_id=404, rating=1, comment="Spam review")

        # Regular user denied admin moderation
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token2.key}")
        res_denied = self.client.patch(f"/api/v1/reviews/admin/{review.id}/", {"is_approved": False}, format="json")
        self.assertEqual(res_denied.status_code, status.HTTP_403_FORBIDDEN)

        # Admin user succeeds
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.admin_token.key}")
        res_approved = self.client.patch(f"/api/v1/reviews/admin/{review.id}/", {"is_approved": False}, format="json")
        self.assertEqual(res_approved.status_code, status.HTTP_200_OK)
        self.assertFalse(res_approved.data["is_approved"])
