from django.urls import path, include
from rest_framework.routers import DefaultRouter
from station.views import (
    AirportViewSet,
    RouteViewSet,
    AirplaneTypeViewSet,
    AirplaneViewSet,
    CrewViewSet,
    FlightViewSet,
    UserViewSet,
    OrderViewSet,
    TicketViewSet,
)

router = DefaultRouter()
router.register("airports", AirportViewSet)
router.register("routes", RouteViewSet)
router.register("airplane-types", AirplaneTypeViewSet)
router.register("airplanes", AirplaneViewSet)
router.register("crew", CrewViewSet)
router.register("flight", FlightViewSet)
router.register("users", UserViewSet)
router.register("orders", OrderViewSet)
router.register("tickets", TicketViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "station"
