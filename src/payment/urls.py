from rest_framework.routers import DefaultRouter
from django.urls import path, include

from payment.views import CreateStripePaymentView, CreatePayPalPaymentView, PaymentViewSet

router = DefaultRouter()

router.register("payment-list", PaymentViewSet, basename="payment-list")

urlpatterns = [
    path("stripe/", CreateStripePaymentView.as_view(), name="stripe-payment"),
    path("paypal/", CreatePayPalPaymentView.as_view(), name="paypal-payment"),
    path("", include(router.urls)),
]

app_name = "payment"
