from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from decimal import Decimal
from payment.models import StripePayment, PayPalPayment
from station.models import Order, Flight, Airport, Route, Airplane, AirplaneType
from django.contrib.auth import get_user_model

User = get_user_model()


class PaymentAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

        self.superuser = User.objects.create_superuser(
            username="superuser", password="superpassword"
        )

        response = self.client.post(
            reverse("token-obtain-pair"),
            {"username": "testuser", "password": "testpassword"},
        )
        self.user_token = response.data["access"]

        response = self.client.post(
            reverse("token-obtain-pair"),
            {"username": "superuser", "password": "superpassword"},
        )
        self.superuser_token = response.data["access"]

        airport_1 = Airport.objects.create(name="Airport 1", closest_big_city="City 1")
        airport_2 = Airport.objects.create(name="Airport 2", closest_big_city="City 2")

        route = Route.objects.create(
            source=airport_1, destination=airport_2, distance=100
        )

        airplane_type = AirplaneType.objects.create(name="Boeing 737")

        airplane = Airplane.objects.create(
            name="Boeing 737-800", rows=20, seats_in_row=6, airplane_type=airplane_type
        )

        self.flight = Flight.objects.create(
            route=route,
            airplane=airplane,
            departure_time="2025-02-25T10:00:00Z",
            arrival_time="2025-02-25T12:00:00Z",
        )

        self.order = Order.objects.create(user=self.user, flight=self.flight)

        self.stripe_payment_url = reverse("payment:stripe-payment-list")
        self.paypal_payment_url = reverse("payment:paypal-payment-list")

    def test_update_stripe_payment_status(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.superuser_token)
        stripe_payment = StripePayment.objects.create(
            user=self.user,
            order=self.order,
            amount=Decimal("100.00"),
            currency="usd",
            status="pending",
        )
        url = reverse("payment:stripe-payment-status", kwargs={"pk": stripe_payment.id})

        # Отправка запроса на изменение статуса
        response = self.client.patch(url, {"status": "completed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        stripe_payment.refresh_from_db()
        self.assertEqual(stripe_payment.status, "completed")

    def test_update_paypal_payment_status(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.superuser_token)

        paypal_payment = PayPalPayment.objects.create(
            user=self.user,
            order=self.order,
            amount=Decimal("100.00"),
            currency="usd",
            status="pending",
        )
        url = reverse("payment:paypal-payment-status", kwargs={"pk": paypal_payment.id})
        response = self.client.patch(url, {"status": "completed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        paypal_payment.refresh_from_db()
        self.assertEqual(paypal_payment.status, "completed")

    def test_create_stripe_payment(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.user_token)
        data = {
            "user": self.user.id,
            "order": self.order.id,
            "amount": "100.00",
            "currency": "usd",
        }
        response = self.client.post(self.stripe_payment_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("client_secret", response.data)

    def test_create_paypal_payment(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.user_token)
        data = {
            "user": self.user.id,
            "order": self.order.id,
            "amount": "100.00",
            "currency": "usd",
        }
        response = self.client.post(self.paypal_payment_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("approval_url", response.data)

    def test_create_stripe_payment_invalid_amount(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.user_token
        )  # Токен авторизации
        data = {
            "user": self.user.id,
            "order": self.order.id,
            "amount": "0",
            "currency": "usd",
        }
        response = self.client.post(self.stripe_payment_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Amount must be greater than zero.", str(response.data))

    def test_create_paypal_payment_invalid_amount(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.user_token)
        data = {
            "user": self.user.id,
            "order": self.order.id,
            "amount": "0",
            "currency": "usd",
        }
        response = self.client.post(self.paypal_payment_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Amount must be greater than zero.", str(response.data))

    def test_get_payment_list(self):
        response = self.client.get(reverse("payment:payment-list-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("stripe_payments", response.data)
        self.assertIn("paypal_payments", response.data)
