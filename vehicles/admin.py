from django.contrib import admin
from revel.logger import log

from .models import Shift, ShiftVehicle, Vehicle


@admin.action(description="Load fixtures")
def load_fixtures(modeladmin, request, queryset):
    """Load vehicle data from data.py"""
    try:
        from .data import data
        vehicles = []
        for item in data:
            vehicles.append(Vehicle(
                # id=item['id'],
                license_plate=item['license_plate'],
                battery_level=item['battery_level'],
                in_use=item['in_use'],
                model=item['model'],
                location_lat=item['location'][0],
                location_long=item['location'][1],
            ))
        Vehicle.objects.bulk_create(vehicles)
    except Exception as e:
        log.exception(str(e))

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "license_plate",
        "battery_level",
        "in_use",
        "model",
        "location_lat",
        "location_long",
        "shift",
        "created_at",
        "updated_at",
    )
    list_filter = ["in_use", "model"]
    actions = [load_fixtures]

    def shift(self, obj: Vehicle):
        shift = obj.shifts.order_by('-updated_at').first()
        return shift

class ShiftVehicleInLine(admin.TabularInline):
    model = ShiftVehicle
    extra = 1


@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "shift_date",
        "employee",
        "created_at",
        "updated_at",

    )
    list_filter = ["shift_date", "employee"]

