from django.http import JsonResponse
from rest_framework import permissions, views, viewsets

from vehicles.data import data
from vehicles.models import Vehicle
from vehicles.serializers import (VehicleCreateSerializer,
                                  VehicleReadSerializer,
                                  VehicleUpdateSerializer)


class VehicleViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    pagination_class = None
    queryset = Vehicle.objects.all()

    def get_serializer_class(self):
        if self.action in ["create"]:
            return VehicleCreateSerializer
        elif self.action in ["update"]:
            return VehicleUpdateSerializer
        return VehicleReadSerializer
