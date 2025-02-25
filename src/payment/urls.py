from rest_framework.routers import DefaultRouter
from django.urls import path, include

from payment.views import CreateStripePaymentView, CreatePayPalPaymentView, PaymentViewSet, StripePaymentViewSet, \
    PayPalPaymentViewSet

router = DefaultRouter()

router.register("payment-list", PaymentViewSet, basename="payment-list")
router.register('stripe-payments', StripePaymentViewSet, basename="stripe-payments")
router.register('paypal-payments', PayPalPaymentViewSet, basename="paypal-payments")
router.register("paypal", CreatePayPalPaymentView, basename="paypal-payment"),
router.register("stripe", CreateStripePaymentView, basename="stripe-payment"),

urlpatterns = [
    path("", include(router.urls)),
    path('stripe/<int:pk>/status/', StripePaymentViewSet.as_view({'patch': 'update_status'}), name='stripe-payment-status'),
    path('paypal/<int:pk>/status/', PayPalPaymentViewSet.as_view({'patch': 'update_status'}), name='paypal-payment-status'),
]

app_name = "payment"
