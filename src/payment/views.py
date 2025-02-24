import paypalrestsdk
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import stripe
from django.conf import settings

# Stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

class CreateStripePaymentView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            amount = request.data.get("amount")
            currency = request.data.get("currency", "usd")

            if not amount:
                return Response({"error": "Amount is required"}, status=status.HTTP_400_BAD_REQUEST)

            payment_intent = stripe.PaymentIntent.create(
                amount=int(amount * 100),
                currency=currency,
                payment_method_types=["card"],
            )

            return Response({"client_secret": payment_intent.client_secret}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
