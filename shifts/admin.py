from django.contrib import admin

from shifts.models import Shift, ShiftVehicle


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

