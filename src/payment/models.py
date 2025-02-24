import paypalrestsdk
import stripe
from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model

from station.models import Order

User = get_user_model()

class BasePayment(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("failed", "Failed"),
        ("canceled", "Canceled"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="stripe_payments")
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default="USD")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class StripePayment(BasePayment):
    stripe_payment_intent_id = models.CharField(max_length=255, blank=True, null=True)

    def create_payment_intent(self):
        try:
            stripe.api_key = settings.STRIPE_SECRET_KEY

            intent = stripe.PaymentIntent.create(
                amount=int(self.amount * 100),
                currency=self.currency.lower(),
                metadata={"order_id": self.order.id},
            )

            self.stripe_payment_intent_id = intent["id"]
            self.save()
            return intent
        except stripe.error.StripeError as e:
            raise ValueError(f"Stripe error occurred: {e.user_message}")

class PayPalPayment(BasePayment):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="paypal_payments")
    payment_id = models.CharField(max_length=255, unique=True, blank=True, null=True)
    payer_id = models.CharField(max_length=255, blank=True, null=True)

    def create_payment(self):
        try:
            paypalrestsdk.configure({
                "mode": settings.PAYPAL_MODE,
                "client_id": settings.PAYPAL_CLIENT_ID,
                "client_secret": settings.PAYPAL_SECRET,
            })

            payment = paypalrestsdk.Payment({
                "intent": "sale",
                "payer": {"payment_method": "paypal"},
                "transactions": [{
                    "amount": {"total": str(self.amount), "currency": self.currency},
                    "description": "Payment for order"
                }],
                "redirect_urls": {
                    "return_url": "http://127.0.0.1:8000/api/payments/paypal/success/",
                    "cancel_url": "http://127.0.0.1:8000/api/payments/paypal/cancel/"
                }
            })

            if payment.create():
                self.payment_id = payment.id
                self.save()
                for link in payment.links:
                    if link.rel == "approval_url":
                        return link.href
            else:
                raise ValueError(f"PayPal payment creation failed: {payment.error}")
        except Exception as e:
            raise ValueError(f"Error occurred during PayPal payment creation: {str(e)}")
