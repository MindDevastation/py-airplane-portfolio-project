from rest_framework import serializers
from payment.models import StripePayment, PayPalPayment

class StripePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StripePayment
        fields = "__all__"

    def validate(self, data):
        if data["amount"] <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return data

class PayPalPaymentSerializer(serializers.ModelSerializer):
    payment_id = serializers.CharField(required=False)

    class Meta:
        model = PayPalPayment
        fields = "__all__"

    def validate(self, data):
        if data["amount"] <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return data
