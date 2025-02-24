import paypalrestsdk
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import stripe
from django.conf import settings

from payment.serializers import StripePaymentSerializer, PayPalPaymentSerializer

# Stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

class CreateStripePaymentView(APIView):
    def post(self, request):
        serializer = StripePaymentSerializer(data=request.data)

        if serializer.is_valid():
            try:
                payment = serializer.save()

                intent = payment.create_payment_intent()

                return Response({"client_secret": intent["client_secret"]}, status=status.HTTP_201_CREATED)

            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# PayPal

paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_SECRET,
})


class CreatePayPalPaymentView(APIView):
    def post(self, request):
        serializer = PayPalPaymentSerializer(data=request.data)

        if serializer.is_valid():
            try:
                payment = serializer.save()

                approval_url = payment.create_payment()

                return Response({"approval_url": approval_url}, status=status.HTTP_201_CREATED)

            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
