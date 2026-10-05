from decimal import Decimal
from unittest.mock import patch
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from orders.models import Order, OrderItem, OrderStatus

User = get_user_model()


class CheckoutAndOrdersAPITestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="alice", password="password123")
        self.token1 = Token.objects.create(user=self.user1)

        self.user2 = User.objects.create_user(username="bob", password="password123")
        self.token2 = Token.objects.create(user=self.user2)

        self.valid_address = {
            "shipping_full_name": "Alice Smith",
            "shipping_street_address": "123 Main Street, Apt 4B",
            "shipping_city": "Techville",
            "shipping_state": "California",
            "shipping_postal_code": "90210",
            "shipping_country": "United States",
            "shipping_phone": "+1-555-0199",
        }

    def test_unauthenticated_checkout_denied(self):
        response = self.client.post("/api/v1/checkout/", self.valid_address, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_checkout_invalid_address(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token1.key}")
        invalid_address = {
            "shipping_full_name": "",  # Blank name
            "shipping_city": "Techville",
        }
        response = self.client.post("/api/v1/checkout/", invalid_address, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("shipping_full_name", response.data)

    @patch("orders.views.fetch_user_cart")
    def test_checkout_empty_cart(self, mock_fetch_cart):
        mock_fetch_cart.return_value = {"items": [], "total_items": 0, "subtotal": "0.00"}
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token1.key}")

        response = self.client.post("/api/v1/checkout/", self.valid_address, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("cart", str(response.data))

    @patch("orders.views.fetch_user_cart")
    @patch("orders.views.verify_and_resolve_products")
    def test_checkout_stock_shortage(self, mock_verify, mock_fetch_cart):
        mock_fetch_cart.return_value = {
            "items": [{"product_id": 1, "quantity": 10}],
            "total_items": 1,
        }
        # Simulate Catalogue stock shortage exception raised during re-verification
        from rest_framework.exceptions import ValidationError
        mock_verify.side_effect = ValidationError({"stock": "Stock shortage for 'Widget'. Requested 10, but only 2 available."})

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token1.key}")
        response = self.client.post("/api/v1/checkout/", self.valid_address, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("orders.views.deduct_inventory_stock")
    @patch("orders.views.clear_user_cart")
    @patch("orders.views.verify_and_resolve_products")
    @patch("orders.views.fetch_user_cart")
    def test_checkout_success_creates_pending_order(self, mock_fetch_cart, mock_verify, mock_clear_cart, mock_deduct):
        mock_fetch_cart.return_value = {
            "items": [{"product_id": 1, "quantity": 2, "unit_price": "25.00"}],
            "total_items": 1,
        }
        mock_verify.return_value = [
            {
                "product_id": 1,
                "product_sku": "WDG-001",
                "product_name": "Premium Widget",
                "unit_price": Decimal("25.00"),
                "quantity": 2,
                "line_total": Decimal("50.00"),
            }
        ]

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token1.key}")
        response = self.client.post("/api/v1/checkout/", self.valid_address, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["status"], OrderStatus.PENDING)
        self.assertEqual(response.data["total_amount"], "50.00")
        self.assertEqual(len(response.data["items"]), 1)
        self.assertEqual(response.data["items"][0]["product_name"], "Premium Widget")
        mock_deduct.assert_called_once()

        # Verify DB records
        order = Order.objects.get(id=response.data["id"])
        self.assertEqual(order.user, self.user1)
        self.assertEqual(order.status, OrderStatus.PENDING)
        self.assertEqual(order.items.count(), 1)

        # Verify clear_user_cart was invoked
        mock_clear_cart.assert_called_once()

    def test_order_list_and_detail_ownership_isolation(self):
        # Create order for Alice
        order_alice = Order.objects.create(
            user=self.user1,
            status=OrderStatus.PENDING,
            shipping_full_name="Alice Smith",
            shipping_street_address="123 Main St",
            shipping_city="Techville",
            shipping_state="CA",
            shipping_postal_code="90210",
            shipping_country="USA",
            total_amount=Decimal("100.00"),
        )

        # Bob logs in and checks orders
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token2.key}")
        res_list = self.client.get("/api/v1/orders/")
        self.assertEqual(res_list.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res_list.data), 0)  # Bob sees 0 orders

        res_detail = self.client.get(f"/api/v1/orders/{order_alice.id}/")
        self.assertEqual(res_detail.status_code, status.HTTP_404_NOT_FOUND)  # Access denied for Alice's order
