from rest_framework.routers import DefaultRouter
from django.urls import path

from payment.views import CreateStripePaymentView, CreatePayPalPaymentView

router = DefaultRouter()

urlpatterns = [
    path("stripe/", CreateStripePaymentView.as_view(), name="stripe-payment"),
    path("paypal/", CreatePayPalPaymentView.as_view(), name="paypal-payment"),
]

app_name = "payment"
