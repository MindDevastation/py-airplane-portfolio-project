from rest_framework.routers import DefaultRouter
from django.urls import path

from payment.views import CreateStripePaymentView

router = DefaultRouter()

urlpatterns = [
    path("stripe/", CreateStripePaymentView.as_view(), name="stripe-payment"),
]

app_name = "payment"
