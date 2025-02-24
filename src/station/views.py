from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User

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
    queryset = Airport.objects.all()
    default_serializer_class = AirportSerializer
    list_serializer_class = AirportListSerializer
    detail_serializer_class = AirportDetailSerializer

class RouteViewSet(BaseViewSet):
    queryset = Route.objects.all()
    default_serializer_class = RouteSerializer
    list_serializer_class = RouteListSerializer
    detail_serializer_class = RouteDetailSerializer

class AirplaneTypeViewSet(BaseViewSet):
    queryset = AirplaneType.objects.all()
    default_serializer_class = AirplaneTypeSerializer
    list_serializer_class = AirplaneTypeListSerializer
    detail_serializer_class = AirplaneTypeDetailSerializer

class AirplaneViewSet(BaseViewSet):
    queryset = Airplane.objects.all()
    default_serializer_class = AirplaneSerializer
    list_serializer_class = AirplaneListSerializer
    detail_serializer_class = AirplaneDetailSerializer

class CrewViewSet(BaseViewSet):
    queryset = Crew.objects.all()
    default_serializer_class = CrewSerializer
    list_serializer_class = CrewListSerializer
    detail_serializer_class = CrewDetailSerializer

class FlightViewSet(BaseViewSet):
    queryset = Flight.objects.all()
    default_serializer_class = FlightSerializer
    list_serializer_class = FlightListSerializer
    detail_serializer_class = FlightDetailSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [UserPermission]

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
    queryset = Order.objects.all()
    default_serializer_class = OrderSerializer
    list_serializer_class = OrderListSerializer
    detail_serializer_class = OrderDetailSerializer

class TicketViewSet(BaseViewSet):
    queryset = Ticket.objects.all()
    default_serializer_class = TicketSerializer
    list_serializer_class = TicketListSerializer
    detail_serializer_class = TicketDetailSerializer
