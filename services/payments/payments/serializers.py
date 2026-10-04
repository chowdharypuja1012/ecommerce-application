from rest_framework import serializers
from .models import PaymentTransaction, PaymentStatus


class PaymentTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentTransaction
        fields = [
            "id",
            "order_id",
            "transaction_reference",
            "idempotency_key",
            "amount",
            "currency",
            "payment_method",
            "status",
            "provider_status_code",
            "provider_message",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields


class PaymentProcessInputSerializer(serializers.Serializer):
    order_id = serializers.IntegerField(required=True)
    amount = serializers.DecimalField(max_digits=12, decimal_places=2, required=True)
    idempotency_key = serializers.CharField(max_length=64, required=False, allow_blank=True, default="")
    simulated_action = serializers.ChoiceField(
        choices=["SUCCESS", "FAIL", "CANCEL"],
        default="SUCCESS",
        required=False
    )
