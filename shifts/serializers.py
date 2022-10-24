from django.utils.translation import gettext_lazy as _
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
