from email.policy import default

from django.utils.translation import gettext_lazy as _
from drf_yasg import openapi
from rest_framework import serializers
from vehicles.serializers import VehicleReadSerializer

from .models import Shift


class ShiftSerializer(serializers.ModelSerializer):
    vehicles = serializers.StringRelatedField(many=True, read_only=True, help_text=_("Vehicles to visit in order. License plates are used to identify vehicles."))
    class Meta:
        model = Shift
        fields = (
            "shift_date",
            "employee",
            "vehicles"
        )

class ShiftAddVehicleSerializer(serializers.Serializer):
    vehicles = serializers.ListSerializer(child=serializers.CharField(), help_text=_("Vehicles to add to the shift, appended to the shift in the given order. License plates are used to identify vehicles."))

class ShiftStatusSerializer(serializers.ModelSerializer):
    is_completed = serializers.ReadOnlyField(help_text=_("If this shift is completed for its vehicles."))
    finished_vehicles = serializers.ReadOnlyField(help_text=_("Vehicles that swap has been finished"))
    class Meta:
        model=Shift

        fields = (
            "is_completed",
            "finished_vehicles",
        )

        swagger_schema_fields = {
            "type": openapi.TYPE_OBJECT,
            "title": "ShiftStatus",
            "properties": {
                "is_completed": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description=_("If this shift is completed for its vehicles.")
                ),
                "finished_vehicles": openapi.Schema(
                    type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING),description=_("Vehicles that swap has been finished")
                ),
            },
         }

class ShiftAutoCreateSerializer(serializers.Serializer):
    start_lat = serializers.FloatField(help_text=_("Latitude of a start point"), required=True)
    start_long = serializers.FloatField(help_text=_("Longitude of a start point"), required=True)
    count = serializers.FloatField(help_text=_("Number of vehicles to add. 20 by default."), required=False, default=20)

