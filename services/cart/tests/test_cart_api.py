from decimal import Decimal
from unittest.mock import patch
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from cart.models import Cart, CartItem

User = get_user_model()


class CartAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="buyer", email="buyer@example.com", password="Password123!"
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

    @patch("cart.views.fetch_and_validate_product")
    def test_get_and_add_cart_item(self, mock_fetch):
        mock_fetch.return_value = {
            "id": 101,
            "sku": "LAPTOP-01",
            "name": "Pro Laptop",
            "unit_price": Decimal("1200.00"),
            "stock": 10,
        }

        # 1. GET cart initially empty
        response_get = self.client.get("/api/v1/cart/")
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)
        self.assertEqual(response_get.json()["total_items"], 0)

        # 2. Add item
        add_payload = {"product_id": 101, "quantity": 2}
        response_add = self.client.post("/api/v1/cart/items/", add_payload, format="json")
        self.assertEqual(response_add.status_code, status.HTTP_200_OK)
        data = response_add.json()
        self.assertEqual(data["total_items"], 2)
        self.assertEqual(Decimal(data["subtotal"]), Decimal("2400.00"))

    @patch("cart.views.fetch_and_validate_product")
    def test_update_and_delete_cart_item(self, mock_fetch):
        mock_fetch.return_value = {
            "id": 102,
            "sku": "MOUSE-01",
            "name": "Wireless Mouse",
            "unit_price": Decimal("25.00"),
            "stock": 50,
        }

        cart = Cart.objects.create(user=self.user, status="active")
        item = CartItem.objects.create(
            cart=cart,
            product_id=102,
            product_sku="MOUSE-01",
            product_name="Wireless Mouse",
            unit_price=Decimal("25.00"),
            quantity=1,
        )

        # Update quantity to 4
        patch_response = self.client.patch(f"/api/v1/cart/items/{item.id}/", {"quantity": 4}, format="json")
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)
        self.assertEqual(patch_response.json()["total_items"], 4)
        self.assertEqual(Decimal(patch_response.json()["subtotal"]), Decimal("100.00"))

        # Delete item
        del_response = self.client.delete(f"/api/v1/cart/items/{item.id}/")
        self.assertEqual(del_response.status_code, status.HTTP_200_OK)
        self.assertEqual(del_response.json()["total_items"], 0)

    @patch("cart.views.fetch_and_validate_product")
    def test_clear_cart(self, mock_fetch):
        cart = Cart.objects.create(user=self.user, status="active")
        CartItem.objects.create(
            cart=cart,
            product_id=103,
            product_sku="ITEM-1",
            product_name="Item 1",
            unit_price=Decimal("15.00"),
            quantity=2,
        )

        response = self.client.post("/api/v1/cart/clear/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["total_items"], 0)
