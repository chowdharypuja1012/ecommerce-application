from decimal import Decimal
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from catalogue.models import Product

User = get_user_model()


class CatalogueAdminPermissionsTestCase(APITestCase):
    def setUp(self):
        # Regular customer (non-staff)
        self.customer = User.objects.create_user(username="regular_customer", password="password123")
        self.customer_token = Token.objects.create(user=self.customer)

        # Admin user (is_staff=True)
        self.admin = User.objects.create_user(username="admin_user", password="password123", is_staff=True)
        self.admin_token = Token.objects.create(user=self.admin)

        self.product = Product.objects.create(
            name="Sample Item",
            slug="sample-item",
            sku="SMP-001",
            price=Decimal("19.99"),
            stock=3,  # Low stock
            is_active=True,
        )

    def test_regular_customer_denied_admin_access(self):
        """
        Verifies that regular customers receive 403 Forbidden on all admin endpoints.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.customer_token.key}")

        # Try to create product
        res1 = self.client.post("/api/v1/catalogue/admin/products/", {"name": "Hack", "sku": "HCK", "price": "1.00"})
        self.assertEqual(res1.status_code, status.HTTP_403_FORBIDDEN)

        # Try to update product stock
        res2 = self.client.patch(f"/api/v1/catalogue/admin/products/{self.product.id}/", {"stock": 100})
        self.assertEqual(res2.status_code, status.HTTP_403_FORBIDDEN)

        # Try to view low stock alerts
        res3 = self.client.get("/api/v1/catalogue/admin/inventory/low-stock/")
        self.assertEqual(res3.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_create_product_success(self):
        """
        Verifies admin user can create a product.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.admin_token.key}")

        payload = {
            "name": "New Admin Product",
            "sku": "ADM-PROD-01",
            "price": "89.99",
            "stock": 25,
            "description": "Created via admin endpoint",
        }
        response = self.client.post("/api/v1/catalogue/admin/products/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["sku"], "ADM-PROD-01")
        self.assertTrue(Product.objects.filter(sku="ADM-PROD-01").exists())

    def test_admin_update_inventory_stock(self):
        """
        Verifies admin user can update stock levels and prices.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.admin_token.key}")

        response = self.client.patch(
            f"/api/v1/catalogue/admin/products/{self.product.id}/",
            {"stock": 50, "price": "24.99"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 50)
        self.assertEqual(self.product.price, Decimal("24.99"))

    def test_admin_low_stock_alerts(self):
        """
        Verifies low stock alert returns products below stock threshold.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.admin_token.key}")

        response = self.client.get("/api/v1/catalogue/admin/inventory/low-stock/?threshold=5")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_low_stock"], 1)
        self.assertEqual(response.data["products"][0]["sku"], "SMP-001")
