from decimal import Decimal
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from catalogue.models import Category, Product


class CatalogueAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create Active Categories
        self.cat_electronics = Category.objects.create(
            name="Electronics",
            slug="electronics",
            description="Electronic devices",
            is_active=True,
        )
        self.cat_books = Category.objects.create(
            name="Books",
            slug="books",
            description="Printed books",
            is_active=True,
        )

        # Create Inactive Category
        self.cat_inactive = Category.objects.create(
            name="Archived Category",
            slug="archived-category",
            description="Inactive category",
            is_active=False,
        )

        # Create Active Products
        self.prod_laptop = Product.objects.create(
            category=self.cat_electronics,
            name="Gaming Laptop",
            slug="gaming-laptop",
            description="High performance gaming laptop",
            price=Decimal("1200.00"),
            sku="LAPTOP-GAMING-01",
            stock=10,
            is_active=True,
        )
        self.prod_mouse = Product.objects.create(
            category=self.cat_electronics,
            name="Wireless Mouse",
            slug="wireless-mouse",
            description="Ergonomic wireless mouse",
            price=Decimal("25.50"),
            sku="MOUSE-WIRELESS-01",
            stock=100,
            is_active=True,
        )
        self.prod_book = Product.objects.create(
            category=self.cat_books,
            name="Python Programming Guide",
            slug="python-programming-guide",
            description="Comprehensive Python book",
            price=Decimal("45.00"),
            sku="BOOK-PYTHON-01",
            stock=30,
            is_active=True,
        )

        # Create Inactive Product
        self.prod_inactive = Product.objects.create(
            category=self.cat_electronics,
            name="Discontinued Gadget",
            slug="discontinued-gadget",
            description="Old gadget",
            price=Decimal("9.99"),
            sku="GADGET-OLD-01",
            stock=0,
            is_active=False,
        )

    # -------------------------------------------------------------------------
    # 1. Category Endpoint Tests
    # -------------------------------------------------------------------------
    def test_category_list_returns_only_active(self):
        response = self.client.get("/api/v1/categories/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        names = [c["name"] for c in data]
        self.assertIn("Books", names)
        self.assertIn("Electronics", names)
        self.assertNotIn("Archived Category", names)

    def test_category_detail_success(self):
        response = self.client.get("/api/v1/categories/electronics/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["slug"], "electronics")
        self.assertEqual(data["name"], "Electronics")

    def test_category_detail_inactive_returns_404(self):
        response = self.client.get("/api/v1/categories/archived-category/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # -------------------------------------------------------------------------
    # 2. Product List & Pagination Tests
    # -------------------------------------------------------------------------
    def test_product_list_returns_paginated_active_products(self):
        response = self.client.get("/api/v1/products/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        self.assertIn("count", data)
        self.assertIn("total_pages", data)
        self.assertIn("current_page", data)
        self.assertIn("results", data)
        self.assertEqual(data["count"], 3)  # Only 3 active products

        skus = [p["sku"] for p in data["results"]]
        self.assertIn("LAPTOP-GAMING-01", skus)
        self.assertIn("MOUSE-WIRELESS-01", skus)
        self.assertIn("BOOK-PYTHON-01", skus)
        self.assertNotIn("GADGET-OLD-01", skus)

    def test_empty_product_list(self):
        Product.objects.all().delete()
        response = self.client.get("/api/v1/products/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["count"], 0)
        self.assertEqual(data["results"], [])

    def test_product_list_custom_page_size(self):
        response = self.client.get("/api/v1/products/?page_size=2")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data["results"]), 2)
        self.assertEqual(data["total_pages"], 2)

    # -------------------------------------------------------------------------
    # 3. Product Detail Tests
    # -------------------------------------------------------------------------
    def test_product_detail_by_slug(self):
        response = self.client.get("/api/v1/products/gaming-laptop/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["slug"], "gaming-laptop")
        self.assertEqual(data["price"], "1200.00")
        self.assertEqual(data["category"]["slug"], "electronics")

    def test_product_detail_inactive_returns_404(self):
        response = self.client.get("/api/v1/products/discontinued-gadget/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_product_detail_nonexistent_returns_404(self):
        response = self.client.get("/api/v1/products/non-existent-item/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # -------------------------------------------------------------------------
    # 4. Search & Filter Tests
    # -------------------------------------------------------------------------
    def test_product_search_filter(self):
        response = self.client.get("/api/v1/products/?search=gaming")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["results"][0]["slug"], "gaming-laptop")

    def test_product_category_filter(self):
        response = self.client.get("/api/v1/products/?category=electronics")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["count"], 2)
        skus = [p["sku"] for p in data["results"]]
        self.assertIn("LAPTOP-GAMING-01", skus)
        self.assertIn("MOUSE-WIRELESS-01", skus)

    def test_product_price_range_filter(self):
        response = self.client.get("/api/v1/products/?min_price=20.00&max_price=50.00")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["count"], 2)
        skus = [p["sku"] for p in data["results"]]
        self.assertIn("MOUSE-WIRELESS-01", skus)
        self.assertIn("BOOK-PYTHON-01", skus)
        self.assertNotIn("LAPTOP-GAMING-01", skus)

    # -------------------------------------------------------------------------
    # 5. Invalid Filter Input Validation (400 Bad Request)
    # -------------------------------------------------------------------------
    def test_invalid_min_price_returns_400(self):
        response = self.client.get("/api/v1/products/?min_price=-50")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = response.json()
        self.assertIn("error", data)
        self.assertIn("min_price", data["details"])

    def test_non_numeric_price_returns_400(self):
        response = self.client.get("/api/v1/products/?max_price=abc")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = response.json()
        self.assertIn("error", data)
        self.assertIn("max_price", data["details"])

    # -------------------------------------------------------------------------
    # 6. Sorting Tests
    # -------------------------------------------------------------------------
    def test_product_sorting_price_asc(self):
        response = self.client.get("/api/v1/products/?ordering=price")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()["results"]
        prices = [Decimal(p["price"]) for p in results]
        self.assertEqual(prices, [Decimal("25.50"), Decimal("45.00"), Decimal("1200.00")])

    def test_product_sorting_price_desc(self):
        response = self.client.get("/api/v1/products/?ordering=-price")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()["results"]
        prices = [Decimal(p["price"]) for p in results]
        self.assertEqual(prices, [Decimal("1200.00"), Decimal("45.00"), Decimal("25.50")])
