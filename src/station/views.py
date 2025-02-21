from django.shortcuts import render
from rest_framework import viewsets

from station.models import Airport
from station.serializers import AirportSerializer, AirportListSerializer, AirportDetailSerializer


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
