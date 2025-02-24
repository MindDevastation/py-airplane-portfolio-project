import django_filters

from airport.pagination import PaginationFilter
from station.models import Airport, Route, Airplane, Flight, Order, Ticket

class AirportFilter(django_filters.FilterSet, PaginationFilter):
    name = django_filters.CharFilter(lookup_expr='icontains')
    closest_big_city = django_filters.CharFilter(lookup_expr='icontains')
    page_size = django_filters.NumberFilter(field_name='page_size', method='filter_page_size', required=False,
                                            label="Number of items per page")

    class Meta:
        model = Airport
        fields = ['name', 'closest_big_city']

class RouteFilter(django_filters.FilterSet, PaginationFilter):
    source = django_filters.CharFilter(field_name='source__name', lookup_expr='icontains')
    destination = django_filters.CharFilter(field_name='destination__name', lookup_expr='icontains')
    page_size = django_filters.NumberFilter(field_name='page_size', method='filter_page_size', required=False,
                                            label="Number of items per page")

    class Meta:
        model = Route
        fields = ['source', 'destination']

class AirplaneFilter(django_filters.FilterSet, PaginationFilter):
    name = django_filters.CharFilter(lookup_expr='icontains')
    airplane_type = django_filters.CharFilter(field_name='airplane_type__name', lookup_expr='icontains')
    page_size = django_filters.NumberFilter(field_name='page_size', method='filter_page_size', required=False,
                                            label="Number of items per page")

    class Meta:
        model = Airplane
        fields = ['name', 'airplane_type']

class FlightFilter(django_filters.FilterSet, PaginationFilter):
    departure_time = django_filters.DateTimeFilter(field_name='departure_time', lookup_expr='gte')
    arrival_time = django_filters.DateTimeFilter(field_name='arrival_time', lookup_expr='lte')
    source = django_filters.CharFilter(field_name='route__source__name', lookup_expr='icontains')
    destination = django_filters.CharFilter(field_name='route__destination__name', lookup_expr='icontains')
    page_size = django_filters.NumberFilter(field_name='page_size', method='filter_page_size', required=False,
                                            label="Number of items per page")

    class Meta:
        model = Flight
        fields = ['departure_time', 'arrival_time', 'source', 'destination']

class OrderFilter(django_filters.FilterSet, PaginationFilter):
    user = django_filters.CharFilter(field_name='user__username', lookup_expr='icontains')
    created_at = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    page_size = django_filters.NumberFilter(field_name='page_size', method='filter_page_size', required=False,
                                     label="Number of items per page")



    class Meta:
        model = Order
        fields = ['user', 'created_at']


class TicketFilter(django_filters.FilterSet, PaginationFilter):
    flight = django_filters.CharFilter(field_name='flight__route__source__name', lookup_expr='icontains')
    order_user = django_filters.CharFilter(field_name='order__user__username', lookup_expr='icontains')
    page_size = django_filters.NumberFilter(field_name='page_size', method='filter_page_size', required=False,
                                            label="Number of items per page")

    class Meta:
        model = Ticket
        fields = ['flight', 'order_user']

class PaymentFilter(django_filters.FilterSet, PaginationFilter):
    user = django_filters.CharFilter(field_name='user__username', lookup_expr='icontains')
    created_at = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    amount = django_filters.NumberFilter(field_name='amount', lookup_expr='gte')
    status = django_filters.CharFilter(field_name='status', lookup_expr='icontains')
    page_size = django_filters.NumberFilter(field_name='page_size', method='filter_page_size', required=False,
                                            label="Number of items per page")