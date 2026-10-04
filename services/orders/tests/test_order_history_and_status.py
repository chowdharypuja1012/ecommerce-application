from decimal import Decimal
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from orders.models import Order, OrderItem, OrderStatus

User = get_user_model()


class OrderHistoryAndStatusTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="alice", password="password123")
        self.token1 = Token.objects.create(user=self.user1)

        self.user2 = User.objects.create_user(username="bob", password="password123")
        self.token2 = Token.objects.create(user=self.user2)

        self.order1 = Order.objects.create(
            user=self.user1,
            status=OrderStatus.PENDING,
            shipping_full_name="Alice Smith",
            shipping_street_address="123 Main St",
            shipping_city="Techville",
            shipping_state="CA",
            shipping_postal_code="90210",
            shipping_country="USA",
            total_amount=Decimal("150.00"),
        )
        self.item1 = OrderItem.objects.create(
            order=self.order1,
            product_id=55,
            product_sku="HEADPHONES-01",
            product_name="Wireless Noise Cancelling Headphones",
            unit_price=Decimal("150.00"),
            quantity=1,
        )

    def test_purchase_time_snapshot_preservation(self):
        """
        Verifies purchase-time product name and unit price snapshot is preserved
        even if Catalogue price changes in the future.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token1.key}")
        response = self.client.get(f"/api/v1/orders/{self.order1.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        item_data = response.data["items"][0]
        self.assertEqual(item_data["product_name"], "Wireless Noise Cancelling Headphones")
        self.assertEqual(item_data["unit_price"], "150.00")

    def test_valid_status_transitions(self):
        """
        Tests valid status progression: PENDING -> PAID -> SHIPPED -> DELIVERED.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token1.key}")

        # 1. PENDING -> PAID
        res1 = self.client.patch(f"/api/v1/orders/{self.order1.id}/status/", {"status": "PAID"}, format="json")
        self.assertEqual(res1.status_code, status.HTTP_200_OK)
        self.assertEqual(res1.data["status"], OrderStatus.PAID)

        # 2. PAID -> SHIPPED
        res2 = self.client.patch(f"/api/v1/orders/{self.order1.id}/status/", {"status": "SHIPPED"}, format="json")
        self.assertEqual(res2.status_code, status.HTTP_200_OK)
        self.assertEqual(res2.data["status"], OrderStatus.SHIPPED)

        # 3. SHIPPED -> DELIVERED
        res3 = self.client.patch(f"/api/v1/orders/{self.order1.id}/status/", {"status": "DELIVERED"}, format="json")
        self.assertEqual(res3.status_code, status.HTTP_200_OK)
        self.assertEqual(res3.data["status"], OrderStatus.DELIVERED)

    def test_invalid_status_transitions(self):
        """
        Verifies illegal transitions (e.g. DELIVERED -> PENDING) return 400 Bad Request.
        """
        self.order1.status = OrderStatus.DELIVERED
        self.order1.save()

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token1.key}")

        # Attempt DELIVERED -> PENDING
        response = self.client.patch(f"/api/v1/orders/{self.order1.id}/status/", {"status": "PENDING"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid status transition", str(response.data))

    def test_customer_cancel_pending_order(self):
        """
        Verifies customer can cancel a PENDING order.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token1.key}")
        response = self.client.post(f"/api/v1/orders/{self.order1.id}/cancel/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], OrderStatus.CANCELLED)

    def test_customer_cannot_cancel_shipped_order(self):
        """
        Verifies customer cannot cancel a SHIPPED order.
        """
        self.order1.status = OrderStatus.SHIPPED
        self.order1.save()

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token1.key}")
        response = self.client.post(f"/api/v1/orders/{self.order1.id}/cancel/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid status transition", str(response.data))
