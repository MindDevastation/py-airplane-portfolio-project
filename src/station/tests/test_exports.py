from django.contrib.auth.models import User

from django.test import TestCase
from django.urls import reverse
from station.models import Order, Flight, Route, Airport, Airplane, AirplaneType


class ExportTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="testuser@example.com"
        )
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

    def test_order_excel_export(self):
        response = self.client.get(reverse("order-excel-export"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response["Content-Type"],
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        self.assertIn("orders_report.xlsx", response["Content-Disposition"])
        self.assertTrue(response.content.startswith(b"PK"))

    def test_order_pdf_export(self):
        response = self.client.get(reverse("order-pdf-export"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/pdf")
        self.assertIn("orders_report.pdf", response["Content-Disposition"])
        self.assertTrue(response.content.startswith(b"%PDF"))

    def test_order_csv_export(self):
        response = self.client.get(reverse("order-csv-export"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/csv")
        self.assertIn("orders_report.csv", response["Content-Disposition"])
        self.assertTrue(response.content.startswith(b"Order ID"))
