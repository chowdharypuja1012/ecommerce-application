from decimal import Decimal
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from orders.models import Order, OrderItem, OrderStatus

User = get_user_model()


class OrdersAdminPermissionsTestCase(APITestCase):
    def setUp(self):
        # Regular customer
        self.customer = User.objects.create_user(username="regular_customer", password="password123")
        self.customer_token = Token.objects.create(user=self.customer)

        # Admin user
        self.admin = User.objects.create_user(username="admin_user", password="password123", is_staff=True)
        self.admin_token = Token.objects.create(user=self.admin)

        self.order1 = Order.objects.create(
            user=self.customer,
            status=OrderStatus.PAID,
            shipping_full_name="Regular Customer",
            shipping_street_address="123 Main St",
            shipping_city="City",
            shipping_state="ST",
            shipping_postal_code="12345",
            shipping_country="Country",
            total_amount=Decimal("200.00"),
        )

    def test_regular_customer_denied_admin_access(self):
        """
        Verifies regular customer receives 403 Forbidden when calling admin endpoints.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.customer_token.key}")

        res1 = self.client.get("/api/v1/orders/admin/all/")
        self.assertEqual(res1.status_code, status.HTTP_403_FORBIDDEN)

        res2 = self.client.get("/api/v1/orders/admin/metrics/")
        self.assertEqual(res2.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_get_all_orders_and_filter(self):
        """
        Verifies admin can view all customer orders across the platform.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.admin_token.key}")

        response = self.client.get("/api/v1/orders/admin/all/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        res_filtered = self.client.get("/api/v1/orders/admin/all/?status=PENDING")
        self.assertEqual(res_filtered.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res_filtered.data), 0)

    def test_admin_view_metrics(self):
        """
        Verifies admin metrics endpoint calculates total revenue and order status breakdown.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.admin_token.key}")

        response = self.client.get("/api/v1/orders/admin/metrics/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_orders"], 1)
        self.assertEqual(response.data["total_revenue"], "200.00")
        self.assertEqual(response.data["orders_by_status"]["PAID"], 1)
