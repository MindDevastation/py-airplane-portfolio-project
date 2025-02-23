from django.shortcuts import render
from rest_framework import viewsets

from station.models import Airport, Route, Airplane, AirplaneType
from station.serializers import AirportSerializer, AirportListSerializer, AirportDetailSerializer, RouteSerializer, \
    RouteListSerializer, RouteDetailSerializer, AirplaneTypeSerializer, AirplaneTypeListSerializer, \
    AirplaneTypeDetailSerializer, AirplaneSerializer, AirplaneListSerializer, AirplaneDetailSerializer


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
