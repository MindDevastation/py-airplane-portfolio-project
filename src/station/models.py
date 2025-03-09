from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Airport(models.Model):
    name = models.CharField(max_length=255)
    closest_big_city = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Route(models.Model):
    source = models.ForeignKey(
        Airport, on_delete=models.CASCADE, related_name="departures"
    )
    destination = models.ForeignKey(
        Airport, on_delete=models.CASCADE, related_name="arrivals"
    )
    distance = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.source} -> {self.destination}"


class AirplaneType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Airplane(models.Model):
    name = models.CharField(max_length=255)
    rows = models.PositiveIntegerField()
    seats_in_row = models.PositiveIntegerField()
    airplane_type = models.ForeignKey(
        AirplaneType, on_delete=models.CASCADE, related_name="airplane_type"
    )

    def __str__(self):
        return self.name


class Crew(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Flight(models.Model):
    STATUS_CHOICES = [
        ("on_time", "On Time"),
        ("delayed", "Delayed"),
        ("cancelled", "Cancelled"),
        ("completed", "Completed"),
    ]

    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name="flight")
    airplane = models.ForeignKey(
        Airplane, on_delete=models.CASCADE, related_name="flight"
    )
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    crew = models.ManyToManyField(Crew, related_name="flights")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="on_time")

    def __str__(self):
        return f"Flight {self.id}: {self.route} - Status: {self.get_status_display()}"

    def get_users(self):
        return self.orders.values_list("user", flat=True)


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    flight = models.ForeignKey(Flight, related_name="orders", on_delete=models.CASCADE)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"


class Ticket(models.Model):
    row = models.PositiveIntegerField()
    seat = models.PositiveIntegerField()
    flight = models.ForeignKey(
        Flight, on_delete=models.CASCADE, related_name="flight_tickets"
    )
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_tickets"
    )

    def __str__(self):
        return f"Ticket {self.id} for Flight {self.flight.id}"


# Logging


class ActionLog(models.Model):
    ACTION_CHOICES = [
        ("created", "Created"),
        ("updated", "Updated"),
        ("deleted", "Deleted"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="actions"
    )
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="action_logs",
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} {self.action} {self.content_type} (ID: {self.object_id}) at {self.timestamp}"
