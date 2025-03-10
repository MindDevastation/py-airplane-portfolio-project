from django.test import TestCase
from django.core import mail
from rest_framework_simplejwt.tokens import RefreshToken

from station.models import Order, Flight, Airport, Route, AirplaneType, Airplane
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from station.signals import send_order_confirmation_email, send_flight_status_update
from rest_framework.test import APIClient


class SignalTests(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="password"
        )

        self.superuser = User.objects.create_superuser(
            username="superuser", email="superuser@example.com", password="password"
        )

        self.user_token = self.get_jwt_token(self.user)
        self.superuser_token = self.get_jwt_token(self.superuser)

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.user_token}")

        origin_airport = Airport.objects.create(
            name="Origin Airport", closest_big_city="Origin City"
        )
        destination_airport = Airport.objects.create(
            name="Destination Airport", closest_big_city="Destination City"
        )
        self.route = Route.objects.create(
            source=origin_airport, destination=destination_airport, distance=1000
        )
        self.airplane_type = AirplaneType.objects.create(name="Airplane Type")
        self.airplane = Airplane.objects.create(
            name="Origin Airplane",
            rows=10,
            seats_in_row=5,
            airplane_type=self.airplane_type,
        )
        self.flight = Flight.objects.create(
            route=self.route,
            airplane=self.airplane,
            departure_time="2025-05-01 10:00:00",
            arrival_time="2025-05-01 12:00:00",
        )
        self.order1 = Order.objects.create(user=self.user, flight=self.flight)
        self.order2 = Order.objects.create(user=self.user, flight=self.flight)

    def get_jwt_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def test_send_order_confirmation_email(self):
        post_save.connect(send_order_confirmation_email, sender=Order)
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(
            mail.outbox[0].subject, f"Order #{self.order1.id} Confirmation"
        )
        self.assertIn(self.order1.user.email, mail.outbox[0].to)

    def test_send_flight_status_update(self):
        post_save.connect(send_flight_status_update, sender=Flight)
        self.flight.save()
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(
            mail.outbox[0].subject, f"Flight {self.flight.id} Status Update"
        )
        self.assertIn(self.user.email, mail.outbox[0].to)
