from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from station.models import Order, Flight, Airport, Route, Airplane, AirplaneType
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class APITests(TestCase):

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

    def test_get_order_list(self):
        response = self.client.get("/api/station/orders/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_get_flight_list(self):
        response = self.client.get("/api/station/flight/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_create_order(self):
        data = {"user": self.user.id, "flight": self.flight.id}
        response = self.client.post("/api/station/orders/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["user"], self.user.id)
        self.assertEqual(response.data["flight"], self.flight.id)

    def test_update_flight_status(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        data = {"status": "delayed"}
        response = self.client.patch(
            f"/api/station/flight/{self.flight.id}/", data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_superuser_update_flight_status(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.superuser_token}")
        data = {"status": "delayed"}
        response = self.client.patch(
            f"/api/station/flight/{self.flight.id}/", data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "delayed")

    def test_unauthorized_user_update_flight_status(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        data = {"status": "delayed"}
        response = self.client.patch(
            f"/api/station/flight/{self.flight.id}/", data, format="json"
        )
        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN
        )  # Ожидаем ошибку доступа
