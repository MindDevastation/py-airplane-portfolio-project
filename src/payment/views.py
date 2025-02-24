import paypalrestsdk
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
import stripe
from django.conf import settings

from payment.models import PayPalPayment, StripePayment
from payment.serializers import StripePaymentSerializer, PayPalPaymentSerializer, StripePaymentStatusUpdateSerializer, \
    PayPalPaymentStatusUpdateSerializer


class PaymentViewSet(viewsets.GenericViewSet):
    def list(self, request):
        stripe_payments = StripePayment.objects.all()
        paypal_payments = PayPalPayment.objects.all()

        stripe_serializer = StripePaymentSerializer(stripe_payments, many=True)
        paypal_serializer = PayPalPaymentSerializer(paypal_payments, many=True)

        return Response({
            "stripe_payments": stripe_serializer.data,
            "paypal_payments": paypal_serializer.data
        }, status=status.HTTP_200_OK)

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

class StripePaymentViewSet(viewsets.ModelViewSet):
    queryset = StripePayment.objects.all()
    serializer_class = StripePaymentSerializer

    def update_status(self, request, pk=None):
        payment = self.get_object()
        serializer = StripePaymentStatusUpdateSerializer(payment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PayPalPaymentViewSet(viewsets.ModelViewSet):
    queryset = PayPalPayment.objects.all()
    serializer_class = PayPalPaymentSerializer

    def update_status(self, request, pk=None):
        payment = self.get_object()
        serializer = PayPalPaymentStatusUpdateSerializer(payment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
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

class PayPalPaymentSuccessView(APIView):
    def get(self, request):
        payment_id = request.GET.get("paymentId")
        payer_id = request.GET.get("PayerID")

        if payment_id and payer_id:
            payment = paypalrestsdk.Payment.find(payment_id)
            if payment.execute({"payer_id": payer_id}):
                paypal_payment = PayPalPayment.objects.get(payment_id=payment_id)
                paypal_payment.status = "completed"
                paypal_payment.save()
                return Response({"status": "Payment completed successfully!"})
            else:
                return Response({"error": "Payment execution failed"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Missing payment or payer ID"}, status=status.HTTP_400_BAD_REQUEST)

class PayPalPaymentCancelView(APIView):
    def get(self, request):
        return Response({"status": "Payment was canceled"}, status=status.HTTP_200_OK)
