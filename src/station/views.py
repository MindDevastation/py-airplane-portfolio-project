from rest_framework import viewsets, filters
from django.contrib.auth.models import User
from django.db.models import Prefetch

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
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ["name", "closest_big_city"]
    ordering_fields = ['name', 'closest_big_city']
    ordering = ['name']

class RouteViewSet(BaseViewSet):
    queryset = Route.objects.all().select_related('source', 'destination')
    default_serializer_class = RouteSerializer
    list_serializer_class = RouteListSerializer
    detail_serializer_class = RouteDetailSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ["source__name", "destination__name"]
    ordering_fields = ['source__name', 'destination__name']
    ordering = ['source__name']

class AirplaneTypeViewSet(BaseViewSet):
    queryset = AirplaneType.objects.all()
    default_serializer_class = AirplaneTypeSerializer
    list_serializer_class = AirplaneTypeListSerializer
    detail_serializer_class = AirplaneTypeDetailSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ["name"]
    ordering_fields = ['name']
    ordering = ['name']

class AirplaneViewSet(BaseViewSet):
    queryset = Airplane.objects.all().select_related('airplane_type')
    default_serializer_class = AirplaneSerializer
    list_serializer_class = AirplaneListSerializer
    detail_serializer_class = AirplaneDetailSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ["name", "airplane_type__name"]
    ordering_fields = ['name', 'airplane_type__name']
    ordering = ['name']

class CrewViewSet(BaseViewSet):
    queryset = Crew.objects.all()
    default_serializer_class = CrewSerializer
    list_serializer_class = CrewListSerializer
    detail_serializer_class = CrewDetailSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
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
    filter_backends = (filters.OrderingFilter, filters.SearchFilter)
    search_fields = ['route__source__name', 'route__destination__name', 'departure_time', 'arrival_time']
    ordering_fields = ['departure_time', 'arrival_time']
    ordering = ['departure_time']

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [UserPermission]
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
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
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ["created_at", "user__username"]
    ordering_fields = ["created_at", "user__username"]
    ordering = ['created_at']

class TicketViewSet(BaseViewSet):
    queryset = Ticket.objects.all().select_related('order', 'flight').prefetch_related(
        Prefetch('order__user', queryset=User.objects.all())
    )
    default_serializer_class = TicketSerializer
    list_serializer_class = TicketListSerializer
    detail_serializer_class = TicketDetailSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ["order__created_at", "order__user__username"]
    ordering_fields = ["order__created_at", "order__user__username"]
    ordering = ['order__created_at']
