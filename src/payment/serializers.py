from rest_framework import serializers
from payment.models import StripePayment, PayPalPayment

class StripePaymentSerializer(serializers.ModelSerializer):
    client_secret = serializers.SerializerMethodField()

    class Meta:
        model = StripePayment
        fields = "__all__"
        read_only_fields = ("id", "status", "stripe_payment_intent_id", )

    def validate(self, data):
        if data["amount"] <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return data

    def get_client_secret(self, obj):
        return obj.stripe_payment_intent_id

    def create(self, validated_data):
        payment = StripePayment.objects.create(**validated_data)
        intent = payment.create_payment_intent()
        return payment

class PayPalPaymentSerializer(serializers.ModelSerializer):
    payment_id = serializers.CharField(required=False, read_only=True)

    class Meta:
        model = PayPalPayment
        fields = "__all__"
        read_only_fields = ["payment_id", "status", "payer_id"]

    def validate(self, data):
        if data["amount"] <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return data

class StripePaymentStatusListSerializer(serializers.ModelSerializer):
    class Meta:
        model = StripePayment
        fields = "__all__"

class StripePaymentStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StripePayment
        fields = ['status']
        read_only_fields = ['stripe_payment_intent_id']

class PayPalPaymentStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayPalPayment
        fields = ['status']
