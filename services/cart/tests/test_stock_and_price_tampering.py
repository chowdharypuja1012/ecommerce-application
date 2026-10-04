from decimal import Decimal
from unittest.mock import patch
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIClient
from cart.models import Cart, CartItem
from cart.catalogue_service import fetch_and_validate_product

User = get_user_model()


class CartSecurityAndValidationTest(TestCase):
    def setUp(self):
        self.client_a = APIClient()
        self.user_a = User.objects.create_user(
            username="usera", email="usera@example.com", password="Password123!"
        )
        self.token_a = Token.objects.create(user=self.user_a)
        self.client_a.credentials(HTTP_AUTHORIZATION=f"Token {self.token_a.key}")

        self.client_b = APIClient()
        self.user_b = User.objects.create_user(
            username="userb", email="userb@example.com", password="Password123!"
        )
        self.token_b = Token.objects.create(user=self.user_b)
        self.client_b.credentials(HTTP_AUTHORIZATION=f"Token {self.token_b.key}")

    @patch("cart.views.fetch_and_validate_product")
    def test_price_tampering_is_ignored(self, mock_fetch):
        mock_fetch.return_value = {
            "id": 200,
            "sku": "EXPENSIVE-01",
            "name": "Expensive Gadget",
            "unit_price": Decimal("999.99"),  # Real price from Catalogue
            "stock": 10,
        }

        # Attempt price tampering by sending fake unit_price: 1.00
        payload = {
            "product_id": 200,
            "quantity": 1,
            "unit_price": "1.00",  # Fake price!
        }
        response = self.client_a.post("/api/v1/cart/items/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        item = CartItem.objects.get(cart__user=self.user_a, product_id=200)
        self.assertEqual(item.unit_price, Decimal("999.99"))
        self.assertNotEqual(item.unit_price, Decimal("1.00"))

    @patch("cart.views.fetch_and_validate_product")
    def test_stock_exceeded_returns_400(self, mock_fetch):
        mock_fetch.side_effect = ValidationError({"quantity": "Requested quantity (20) exceeds available stock (5)."})

        payload = {"product_id": 201, "quantity": 20}
        response = self.client_a.post("/api/v1/cart/items/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("quantity", response.json())

    def test_negative_quantity_returns_400(self):
        payload = {"product_id": 202, "quantity": -5}
        response = self.client_a.post("/api/v1/cart/items/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_strict_cart_item_ownership(self):
        cart_a = Cart.objects.create(user=self.user_a, status="active")
        item_a = CartItem.objects.create(
            cart=cart_a,
            product_id=300,
            product_sku="SKU-A",
            product_name="User A Item",
            unit_price=Decimal("50.00"),
            quantity=1,
        )

        # User B tries to update User A's cart item -> 403 Forbidden
        url = f"/api/v1/cart/items/{item_a.id}/"
        response_patch = self.client_b.patch(url, {"quantity": 10}, format="json")
        self.assertEqual(response_patch.status_code, status.HTTP_403_FORBIDDEN)

        # User B tries to delete User A's cart item -> 403 Forbidden
        response_del = self.client_b.delete(url)
        self.assertEqual(response_del.status_code, status.HTTP_403_FORBIDDEN)

        # Verify User A's item is untouched
        item_a.refresh_from_db()
        self.assertEqual(item_a.quantity, 1)
