from django.urls import path, include
from rest_framework.routers import DefaultRouter
from station.views import AirportViewSet

router = DefaultRouter()
router.register("airports", AirportViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "station"