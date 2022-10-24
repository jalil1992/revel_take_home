from typing import Tuple

from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from .models import Vehicle


class VehicleCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = (
            "license_plate",
            "battery_level",
            "in_use",
            "model",
            "location_lat",
            "location_long",
        )

class VehicleReadSerializer(serializers.ModelSerializer):
    location = serializers.SerializerMethodField()
    class Meta:
        model = Vehicle
        fields = (
            "license_plate",
            "battery_level",
            "in_use",
            "model",
            "location",
        )

    @swagger_serializer_method(serializer_or_field=serializers.ListSerializer(child=serializers.FloatField()))
    def get_location(self, obj:Vehicle)->Tuple[float]:
        return obj.location_lat, obj.location_long
