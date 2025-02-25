"""
URL configuration for airport project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from station.views import (
    OrderExcelExportView,
    OrderPDFExportView,
    OrderCSVExportView,
    send_test_email,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/station/", include("station.urls", namespace="station")),
    path("api/payment/", include("payment.urls", namespace="payment")),
    path("api/token/", TokenObtainPairView.as_view(), name="token-obtain-pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path(
        "api/order-excel-export/",
        OrderExcelExportView.as_view(),
        name="order-excel-export",
    ),
    path(
        "api/order-pdf-export/", OrderPDFExportView.as_view(), name="order-pdf-export"
    ),
    path(
        "api/order-csv-export/", OrderCSVExportView.as_view(), name="order-csv-export"
    ),
    path("api/send-test-email/", send_test_email, name="send-test-email"),
]
