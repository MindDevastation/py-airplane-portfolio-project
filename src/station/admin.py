from django.contrib import admin
from import_export import resources
from import_export.admin import ExportMixin

from station.models import (
    Airport,
    Route,
    AirplaneType,
    Airplane,
    Crew,
    Flight,
    Order,
    Ticket
)

admin.site.register(Airport)
admin.site.register(Route)
admin.site.register(AirplaneType)
admin.site.register(Airplane)
admin.site.register(Crew)
admin.site.register(Flight)
admin.site.register(Ticket)

class OrderResource(resources.ModelResource):
    class Meta:
        model = Order
        fields = ('id', 'user__username', 'created_at')
        export_order = ('id', 'user__username', 'created_at')

@admin.register(Order)
class OrderAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = OrderResource
