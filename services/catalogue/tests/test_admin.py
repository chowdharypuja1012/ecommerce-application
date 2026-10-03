from decimal import Decimal
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from catalogue.models import Category, Product


User = get_user_model()


class CatalogueAdminTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.superuser = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="adminpassword123",
        )
        self.client.login(username="admin", password="adminpassword123")

        self.category = Category.objects.create(
            name="Audio",
            slug="audio",
            description="Sound equipment",
        )
        self.product = Product.objects.create(
            category=self.category,
            name="Wireless Headphones",
            slug="wireless-headphones",
            price=Decimal("199.99"),
            sku="AUDIO-HEADPHONES-01",
            stock=25,
        )

    def test_admin_registration(self):
        self.assertTrue(admin.site.is_registered(Category))
        self.assertTrue(admin.site.is_registered(Product))

    def test_category_admin_changelist_view(self):
        response = self.client.get("/admin/catalogue/category/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Audio")

    def test_product_admin_changelist_view(self):
        response = self.client.get("/admin/catalogue/product/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Wireless Headphones")
        self.assertContains(response, "AUDIO-HEADPHONES-01")
