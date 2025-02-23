from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import viewsets

from airport.permissions import UserPermission
from station.models import Airport, Route, Airplane, AirplaneType, Crew, Flight, Order, Ticket
from station.serializers import AirportSerializer, AirportListSerializer, AirportDetailSerializer, RouteSerializer, \
    RouteListSerializer, RouteDetailSerializer, AirplaneTypeSerializer, AirplaneTypeListSerializer, \
    AirplaneTypeDetailSerializer, AirplaneSerializer, AirplaneListSerializer, AirplaneDetailSerializer, CrewSerializer, \
    CrewListSerializer, CrewDetailSerializer, FlightSerializer, FlightListSerializer, FlightDetailSerializer, \
    UserSerializer, UserListSerializer, \
    UserDetailSerializer, OrderSerializer, OrderListSerializer, OrderDetailSerializer, TicketSerializer, \
    TicketListSerializer, TicketDetailSerializer


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return AirportListSerializer
        elif self.action == 'retrieve':
            return AirportDetailSerializer
        else:
            return AirportSerializer

class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return RouteListSerializer
        elif self.action == 'retrieve':
            return RouteDetailSerializer
        else:
            return RouteSerializer

class AirplaneTypeViewSet(viewsets.ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return AirplaneTypeListSerializer
        elif self.action == 'retrieve':
            return AirplaneTypeDetailSerializer
        else:
            return AirplaneTypeSerializer

class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return AirplaneListSerializer
        elif self.action == 'retrieve':
            return AirplaneDetailSerializer
        else:
            return AirplaneSerializer

class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return CrewListSerializer
        elif self.action == 'retrieve':
            return CrewDetailSerializer
        else:
            return CrewSerializer

class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return FlightListSerializer
        elif self.action == 'retrieve':
            return FlightDetailSerializer
        else:
            return FlightSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [UserPermission]

    def get_queryset(self):
        if self.action == 'list':
            return User.objects.all()
        if self.request.user.is_authenticated:
            return User.objects.filter(id=self.request.user.id)
        return User.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return UserListSerializer
        elif self.action == 'retrieve':
            return UserDetailSerializer
        else:
            return UserSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return OrderListSerializer
        elif self.action == 'retrieve':
            return OrderDetailSerializer
        else:
            return OrderSerializer

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return TicketListSerializer
        elif self.action == 'retrieve':
            return TicketDetailSerializer
        else:
            return TicketSerializer
