from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase
from catalogue.models import Category, Product


class CategoryModelTest(TestCase):
    def test_category_creation_and_str(self):
        category = Category.objects.create(
            name="Electronics",
            slug="electronics",
            description="Gadgets and devices",
        )
        self.assertEqual(str(category), "Electronics")
        self.assertTrue(category.is_active)
        self.assertIsNotNone(category.created_at)
        self.assertIsNotNone(category.updated_at)

    def test_category_unique_name_and_slug(self):
        Category.objects.create(name="Books", slug="books")
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Category.objects.create(name="Books", slug="books-2")

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Category.objects.create(name="Other Books", slug="books")


class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Smartphones",
            slug="smartphones",
        )

    def test_product_creation_and_str(self):
        product = Product.objects.create(
            category=self.category,
            name="Pro Phone 15",
            slug="pro-phone-15",
            description="Flagship smartphone",
            price=Decimal("999.99"),
            sku="PHONE-15-PRO",
            stock=50,
            image_url="https://example.com/phone.jpg",
        )
        self.assertEqual(str(product), "Pro Phone 15 (PHONE-15-PRO)")
        self.assertEqual(product.category, self.category)
        self.assertTrue(product.is_active)
        self.assertEqual(product.price, Decimal("999.99"))
        self.assertEqual(product.stock, 50)

    def test_product_negative_price_validation(self):
        product = Product(
            name="Invalid Price Item",
            slug="invalid-price-item",
            price=Decimal("-10.00"),
            sku="INV-PRICE-1",
            stock=10,
        )
        with self.assertRaises(ValidationError):
            product.full_clean()

    def test_product_negative_stock_validation(self):
        product = Product(
            name="Invalid Stock Item",
            slug="invalid-stock-item",
            price=Decimal("19.99"),
            sku="INV-STOCK-1",
            stock=-5,
        )
        with self.assertRaises(ValidationError):
            product.full_clean()

    def test_product_sku_uniqueness(self):
        Product.objects.create(
            name="Item A",
            slug="item-a",
            price=Decimal("10.00"),
            sku="SKU-UNIQUE",
        )
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Product.objects.create(
                    name="Item B",
                    slug="item-b",
                    price=Decimal("15.00"),
                    sku="SKU-UNIQUE",
                )

    def test_product_slug_uniqueness(self):
        Product.objects.create(
            name="Item One",
            slug="item-slug-unique",
            price=Decimal("10.00"),
            sku="SKU-1",
        )
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Product.objects.create(
                    name="Item Two",
                    slug="item-slug-unique",
                    price=Decimal("15.00"),
                    sku="SKU-2",
                )
