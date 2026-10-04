from decimal import Decimal
from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.test import TestCase
from cart.models import Cart, CartItem

User = get_user_model()


class CartModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="cartuser", email="cart@example.com", password="Password123!"
        )

    def test_cart_creation_and_properties(self):
        cart = Cart.objects.create(user=self.user, status="active")
        self.assertEqual(cart.subtotal, Decimal("0.00"))
        self.assertEqual(cart.total_items, 0)

        CartItem.objects.create(
            cart=cart,
            product_id=1,
            product_sku="SKU-1",
            product_name="Product 1",
            unit_price=Decimal("25.00"),
            quantity=2,
        )
        CartItem.objects.create(
            cart=cart,
            product_id=2,
            product_sku="SKU-2",
            product_name="Product 2",
            unit_price=Decimal("10.00"),
            quantity=1,
        )

        cart.refresh_from_db()
        self.assertEqual(cart.total_items, 3)
        self.assertEqual(cart.subtotal, Decimal("60.00"))

    def test_unique_active_cart_constraint(self):
        Cart.objects.create(user=self.user, status="active")
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Cart.objects.create(user=self.user, status="active")
