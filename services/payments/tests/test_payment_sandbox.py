from decimal import Decimal
from unittest.mock import patch
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from payments.models import PaymentTransaction, PaymentStatus

User = get_user_model()


class PaymentSandboxAPITestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="alice", password="password123")
        self.token1 = Token.objects.create(user=self.user1)

    def test_unauthenticated_payment_denied(self):
        payload = {"order_id": 10, "amount": "99.99"}
        response = self.client.post("/api/v1/payments/process/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch("payments.views.notify_order_payment_status")
    def test_simulated_payment_success_path(self, mock_notify):
        mock_notify.return_value = True
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token1.key}")

        payload = {
            "order_id": 101,
            "amount": "149.99",
            "simulated_action": "SUCCESS",
        }
        response = self.client.post("/api/v1/payments/process/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], PaymentStatus.SUCCESS)
        self.assertTrue(response.data["transaction_reference"].startswith("PAY-SIM-"))

        # Verify notify_order_payment_status was invoked
        mock_notify.assert_called_once_with(101, "SUCCESS", auth_header=f"Token {self.token1.key}")

    def test_simulated_payment_failure_path(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token1.key}")

        payload = {
            "order_id": 102,
            "amount": "299.00",
            "simulated_action": "FAIL",
        }
        response = self.client.post("/api/v1/payments/process/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], PaymentStatus.FAILED)
        self.assertIn("declined", response.data["provider_message"].lower())

    def test_simulated_payment_cancel_path(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token1.key}")

        payload = {
            "order_id": 103,
            "amount": "50.00",
            "simulated_action": "CANCEL",
        }
        response = self.client.post("/api/v1/payments/process/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], PaymentStatus.CANCELLED)

    @patch("payments.views.notify_order_payment_status")
    def test_payment_idempotency_key(self, mock_notify):
        mock_notify.return_value = True
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token1.key}")

        payload = {
            "order_id": 104,
            "amount": "75.00",
            "idempotency_key": "IDEM-KEY-9999",
            "simulated_action": "SUCCESS",
        }

        # First execution
        res1 = self.client.post("/api/v1/payments/process/", payload, format="json")
        self.assertEqual(res1.status_code, status.HTTP_200_OK)
        tx_ref_1 = res1.data["transaction_reference"]

        # Second execution with exact same idempotency_key
        res2 = self.client.post("/api/v1/payments/process/", payload, format="json")
        self.assertEqual(res2.status_code, status.HTTP_200_OK)
        tx_ref_2 = res2.data["transaction_reference"]

        # Must return the exact same transaction without duplicate charge
        self.assertEqual(tx_ref_1, tx_ref_2)
        self.assertEqual(PaymentTransaction.objects.filter(idempotency_key="IDEM-KEY-9999").count(), 1)

    @patch("payments.views.notify_order_payment_status")
    def test_duplicate_webhook_callback_ignored(self, mock_notify):
        tx = PaymentTransaction.objects.create(
            user=self.user1,
            order_id=200,
            amount=Decimal("120.00"),
            status=PaymentStatus.SUCCESS,
            provider_status_code="SIM_200_OK",
        )

        payload = {
            "transaction_reference": tx.transaction_reference,
            "status": "SUCCESS",
        }
        # Send webhook callback for already COMPLETED transaction
        response = self.client.post("/api/v1/payments/webhook/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Duplicate webhook callback ignored", response.data["detail"])

    def test_no_card_data_stored_in_schema(self):
        """
        Security check: verifies PaymentTransaction model does NOT have fields for card number, CVV, or pin.
        """
        field_names = [f.name for f in PaymentTransaction._meta.get_fields()]
        self.assertNotIn("card_number", field_names)
        self.assertNotIn("cvv", field_names)
        self.assertNotIn("card_cvv", field_names)
        self.assertNotIn("pin", field_names)
        self.assertNotIn("expiry", field_names)
