import csv

import openpyxl
from django.core.mail import send_mail
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from rest_framework import viewsets
from django.contrib.auth.models import User
from django.db.models import Prefetch
from rest_framework.views import APIView

from airport.filters import AirportFilter, RouteFilter, FlightFilter, OrderFilter, TicketFilter
from airport.pagination import ExtendedPagination
from airport.permissions import UserPermission
from station.models import Airport, Route, Airplane, AirplaneType, Crew, Flight, Order, Ticket
from station.serializers import (
    AirportSerializer, AirportListSerializer, AirportDetailSerializer,
    RouteSerializer, RouteListSerializer, RouteDetailSerializer,
    AirplaneTypeSerializer, AirplaneTypeListSerializer, AirplaneTypeDetailSerializer,
    AirplaneSerializer, AirplaneListSerializer, AirplaneDetailSerializer,
    CrewSerializer, CrewListSerializer, CrewDetailSerializer,
    FlightSerializer, FlightListSerializer, FlightDetailSerializer,
    UserSerializer, UserListSerializer, UserDetailSerializer,
    OrderSerializer, OrderListSerializer, OrderDetailSerializer,
    TicketSerializer, TicketListSerializer, TicketDetailSerializer
)

class BaseViewSet(viewsets.ModelViewSet):
    """
    A base ViewSet for all objects that automatically selects a serializer depending on the action.
    """
    def get_serializer_class(self):
        serializer_map = {
            'list': self.list_serializer_class,
            'retrieve': self.detail_serializer_class
        }
        return serializer_map.get(self.action, self.default_serializer_class)

class AirportViewSet(BaseViewSet):
    queryset = Airport.objects.all().prefetch_related(
        Prefetch('departures', queryset=Route.objects.select_related('destination')),
        Prefetch('arrivals', queryset=Route.objects.select_related('source'))
    )
    default_serializer_class = AirportSerializer
    list_serializer_class = AirportListSerializer
    detail_serializer_class = AirportDetailSerializer
    pagination_class = ExtendedPagination
    filterset_class = AirportFilter
    search_fields = ["name", "closest_big_city"]
    ordering_fields = ['name', 'closest_big_city']
    ordering = ['name']

class RouteViewSet(BaseViewSet):
    queryset = Route.objects.all().select_related('source', 'destination')
    default_serializer_class = RouteSerializer
    list_serializer_class = RouteListSerializer
    detail_serializer_class = RouteDetailSerializer
    pagination_class = ExtendedPagination
    filterset_class = RouteFilter
    search_fields = ["source__name", "destination__name"]
    ordering_fields = ['source__name', 'destination__name']
    ordering = ['source__name']

class AirplaneTypeViewSet(BaseViewSet):
    queryset = AirplaneType.objects.all()
    default_serializer_class = AirplaneTypeSerializer
    list_serializer_class = AirplaneTypeListSerializer
    detail_serializer_class = AirplaneTypeDetailSerializer
    pagination_class = ExtendedPagination
    filterset_class = AirportFilter
    search_fields = ["name"]
    ordering_fields = ['name']
    ordering = ['name']

class AirplaneViewSet(BaseViewSet):
    queryset = Airplane.objects.all().select_related('airplane_type')
    default_serializer_class = AirplaneSerializer
    list_serializer_class = AirplaneListSerializer
    detail_serializer_class = AirplaneDetailSerializer
    pagination_class = ExtendedPagination
    search_fields = ["name", "airplane_type__name"]
    ordering_fields = ['name', 'airplane_type__name']
    ordering = ['name']

class CrewViewSet(BaseViewSet):
    queryset = Crew.objects.all()
    default_serializer_class = CrewSerializer
    list_serializer_class = CrewListSerializer
    detail_serializer_class = CrewDetailSerializer
    pagination_class = ExtendedPagination
    search_fields = ["first_name", "last_name"]
    ordering_fields = ['first_name', 'last_name']
    ordering = ['last_name']

class FlightViewSet(BaseViewSet):
    queryset = Flight.objects.all().select_related('route', 'airplane').prefetch_related(
        Prefetch('crew', queryset=Crew.objects.all())
    )
    default_serializer_class = FlightSerializer
    list_serializer_class = FlightListSerializer
    detail_serializer_class = FlightDetailSerializer
    pagination_class = ExtendedPagination
    filterset_class = FlightFilter
    search_fields = ['route__source__name', 'route__destination__name', 'departure_time', 'arrival_time']
    ordering_fields = ['departure_time', 'arrival_time']
    ordering = ['departure_time']

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = ExtendedPagination
    permission_classes = [UserPermission]
    search_fields = ['username', "email", "first_name", "last_name"]
    ordering_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['username']

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return User.objects.none()
        if user.is_staff or user.is_superuser:
            return User.objects.all()
        return User.objects.filter(id=user.id)

    def get_serializer_class(self):
        serializer_map = {
            'list': UserListSerializer,
            'retrieve': UserDetailSerializer
        }
        return serializer_map.get(self.action, UserSerializer)

class OrderViewSet(BaseViewSet):
    queryset = Order.objects.all().select_related('user')
    default_serializer_class = OrderSerializer
    list_serializer_class = OrderListSerializer
    detail_serializer_class = OrderDetailSerializer
    pagination_class = ExtendedPagination
    filterset_class = OrderFilter
    search_fields = ["created_at", "user__username"]
    ordering_fields = ["created_at", "user__username"]
    # ordering = ['created_at']

class TicketViewSet(BaseViewSet):
    queryset = Ticket.objects.all().select_related('order', 'flight').prefetch_related(
        Prefetch('order__user', queryset=User.objects.all())
    )
    default_serializer_class = TicketSerializer
    list_serializer_class = TicketListSerializer
    detail_serializer_class = TicketDetailSerializer
    pagination_class = ExtendedPagination
    filterset_class = TicketFilter
    search_fields = ["order__created_at", "order__user__username"]
    ordering_fields = ["order__created_at", "order__user__username"]
    ordering = ['order__created_at']

# Export files

class OrderExcelExportView(APIView):
    def get(self, request, *args, **kwargs):
        orders = Order.objects.all()

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Orders Report"

        ws.append(['Order ID', 'User', 'Created At'])

        for order in orders:
            created_at = order.created_at.replace(tzinfo=None) if order.created_at else None
            ws.append([order.id, order.user.username, created_at])

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="orders_report.xlsx"'

        wb.save(response)
        return response


class OrderPDFExportView(APIView):
    def get(self, request, *args, **kwargs):
        orders = Order.objects.all()

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="orders_report.pdf"'

        p = canvas.Canvas(response, pagesize=letter)
        width, height = letter

        p.setFont("Helvetica-Bold", 16)
        p.drawString(200, height - 40, "Orders Report")

        p.setFont("Helvetica", 12)
        p.drawString(50, height - 80, "Order ID")
        p.drawString(150, height - 80, "User")
        p.drawString(250, height - 80, "Created At")
        # p.drawString(350, height - 80, "Status")

        y_position = height - 100
        for order in orders:
            p.drawString(50, y_position, str(order.id))
            p.drawString(150, y_position, order.user.username)
            p.drawString(250, y_position, str(order.created_at))
            # p.drawString(350, y_position, order.status)
            y_position -= 20

        p.showPage()
        p.save()

        return response


class OrderCSVExportView(APIView):
    def get(self, request, *args, **kwargs):
        orders = Order.objects.all()

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="orders_report.csv"'

        writer = csv.writer(response)

        writer.writerow(['Order ID', 'User', 'Created At'])

        for order in orders:
            writer.writerow([order.id, order.user.username, order.created_at])

        return response

# Test Mailing

def send_test_email(request):
    send_mail(
        'Test Email Subject',
        'Here is the message body.',
        'from@example.com',
        ['to@example.com'],
        fail_silently=False,
    )
    return HttpResponse("Test email sent!")
