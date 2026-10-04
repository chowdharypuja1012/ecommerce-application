from unittest.mock import patch
from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from wishlist.models import Wishlist, WishlistItem

User = get_user_model()


class WishlistAPITestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="alice", password="password123")
        self.token1 = Token.objects.create(user=self.user1)

        self.user2 = User.objects.create_user(username="bob", password="password123")
        self.token2 = Token.objects.create(user=self.user2)

    def test_unauthenticated_access_denied(self):
        response = self.client.get("/api/v1/wishlist/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_empty_wishlist(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token1.key}")
        response = self.client.get("/api/v1/wishlist/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_items"], 0)
        self.assertEqual(response.data["items"], [])

    @patch("wishlist.views.fetch_product_details")
    def test_add_wishlist_item(self, mock_fetch):
        mock_fetch.return_value = {
            "id": 101,
            "sku": "PHONE-001",
            "name": "Smartphone X",
            "price": "599.99",
            "stock": 10,
            "is_active": True,
        }
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token1.key}")
        response = self.client.post("/api/v1/wishlist/items/", {"product_id": 101}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["total_items"], 1)
        self.assertEqual(response.data["items"][0]["product_id"], 101)

    @patch("wishlist.views.fetch_product_details")
    def test_prevent_duplicate_wishlist_item(self, mock_fetch):
        mock_fetch.return_value = {
            "id": 101,
            "sku": "PHONE-001",
            "name": "Smartphone X",
            "price": "599.99",
            "stock": 10,
            "is_active": True,
        }
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token1.key}")
        # First add succeeds
        res1 = self.client.post("/api/v1/wishlist/items/", {"product_id": 101}, format="json")
        self.assertEqual(res1.status_code, status.HTTP_201_CREATED)

        # Second add of same product must fail with 400 Bad Request
        with transaction.atomic():
            res2 = self.client.post("/api/v1/wishlist/items/", {"product_id": 101}, format="json")
        self.assertEqual(res2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("already in your wishlist", str(res2.data))

    @patch("wishlist.views.fetch_product_details")
    def test_remove_wishlist_item_by_id(self, mock_fetch):
        mock_fetch.return_value = {"id": 101, "name": "Prod 101"}
        wishlist = Wishlist.objects.create(user=self.user1)
        item = WishlistItem.objects.create(wishlist=wishlist, product_id=101)

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token1.key}")
        response = self.client.delete(f"/api/v1/wishlist/items/{item.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_items"], 0)

    @patch("wishlist.views.fetch_product_details")
    def test_remove_wishlist_item_by_product_id(self, mock_fetch):
        mock_fetch.return_value = {"id": 101, "name": "Prod 101"}
        wishlist = Wishlist.objects.create(user=self.user1)
        WishlistItem.objects.create(wishlist=wishlist, product_id=101)

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token1.key}")
        response = self.client.delete("/api/v1/wishlist/items/by-product/101/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_items"], 0)

    def test_wishlist_ownership_isolation(self):
        # Alice creates a wishlist item
        wishlist_alice = Wishlist.objects.create(user=self.user1)
        item_alice = WishlistItem.objects.create(wishlist=wishlist_alice, product_id=202)

        # Bob attempts to delete Alice's item
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token2.key}")
        response = self.client.delete(f"/api/v1/wishlist/items/{item_alice.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Confirm item still exists in Alice's wishlist
        self.assertTrue(WishlistItem.objects.filter(id=item_alice.id).exists())

    @patch("wishlist.views.fetch_product_details")
    def test_clear_wishlist(self, mock_fetch):
        mock_fetch.return_value = {"id": 1, "name": "Test"}
        wishlist = Wishlist.objects.create(user=self.user1)
        WishlistItem.objects.create(wishlist=wishlist, product_id=101)
        WishlistItem.objects.create(wishlist=wishlist, product_id=102)

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token1.key}")
        response = self.client.post("/api/v1/wishlist/clear/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_items"], 0)
