from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import PaymentTransaction, PaymentStatus
from .serializers import PaymentTransactionSerializer, PaymentProcessInputSerializer
from .orders_client import notify_order_payment_status


class ProcessPaymentView(APIView):
    """
    POST /api/v1/payments/process/
    Simulates payment execution in sandbox mode without real charges or card storage.
    Enforces idempotency keys and prevents duplicate payment processing.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PaymentProcessInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        order_id = data["order_id"]
        amount = data["amount"]
        idempotency_key = data.get("idempotency_key", "").strip() or None
        simulated_action = data.get("simulated_action", "SUCCESS")
        auth_header = request.headers.get("Authorization")

        # 1. Idempotency Key Check
        if idempotency_key:
            existing = PaymentTransaction.objects.filter(idempotency_key=idempotency_key).first()
            if existing:
                res_serializer = PaymentTransactionSerializer(existing)
                return Response(res_serializer.data, status=status.HTTP_200_OK)

        # 2. Check for prior successful payment for this order
        existing_paid = PaymentTransaction.objects.filter(
            order_id=order_id,
            status=PaymentStatus.SUCCESS
        ).first()
        if existing_paid:
            res_serializer = PaymentTransactionSerializer(existing_paid)
            return Response(res_serializer.data, status=status.HTTP_200_OK)

        # 3. Simulate Payment Sandbox Gateway Execution
        if simulated_action == "SUCCESS":
            payment_status = PaymentStatus.SUCCESS
            status_code = "SIM_200_APPROVED"
            message = "Simulated payment approved by sandbox provider."
        elif simulated_action == "FAIL":
            payment_status = PaymentStatus.FAILED
            status_code = "SIM_402_DECLINED"
            message = "Simulated payment declined by sandbox provider (insufficient funds)."
        else:  # CANCEL
            payment_status = PaymentStatus.CANCELLED
            status_code = "SIM_400_CANCELLED"
            message = "Simulated payment cancelled by user."

        transaction_obj = PaymentTransaction.objects.create(
            user=request.user,
            order_id=order_id,
            idempotency_key=idempotency_key,
            amount=amount,
            currency="USD",
            payment_method="SIMULATED_SANDBOX",
            status=payment_status,
            provider_status_code=status_code,
            provider_message=message,
        )

        # 4. Notify Orders service if payment succeeded
        if payment_status == PaymentStatus.SUCCESS:
            notify_order_payment_status(order_id, "SUCCESS", auth_header=auth_header)

        res_serializer = PaymentTransactionSerializer(transaction_obj)
        return Response(res_serializer.data, status=status.HTTP_200_OK)


class PaymentWebhookCallbackView(APIView):
    """
    POST /api/v1/payments/webhook/
    Handles asynchronous provider webhook callbacks.
    Enforces duplicate callback idempotency.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        tx_ref = request.data.get("transaction_reference")
        new_status = request.data.get("status")

        if not tx_ref or not new_status:
            return Response(
                {"detail": "transaction_reference and status are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        tx = PaymentTransaction.objects.filter(transaction_reference=tx_ref).first()
        if not tx:
            return Response(
                {"detail": f"Transaction reference '{tx_ref}' not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Duplicate Callback Protection: If transaction already processed, ignore duplicate cleanly
        if tx.status in [PaymentStatus.SUCCESS, PaymentStatus.FAILED, PaymentStatus.CANCELLED]:
            return Response({
                "detail": f"Duplicate webhook callback ignored. Transaction '{tx_ref}' is already in status '{tx.status}'.",
                "status": tx.status,
            }, status=status.HTTP_200_OK)

        if new_status in PaymentStatus.values:
            tx.status = new_status
            tx.provider_message = f"Updated via async webhook callback to {new_status}."
            tx.save()

            if new_status == PaymentStatus.SUCCESS:
                notify_order_payment_status(tx.order_id, "SUCCESS")

        res_serializer = PaymentTransactionSerializer(tx)
        return Response(res_serializer.data, status=status.HTTP_200_OK)


class PaymentOrderTransactionsView(APIView):
    """
    GET /api/v1/payments/order/<int:order_id>/
    Returns payment history for a specific user order.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        txs = PaymentTransaction.objects.filter(order_id=order_id, user=request.user)
        serializer = PaymentTransactionSerializer(txs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
