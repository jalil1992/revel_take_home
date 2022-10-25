from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, views, viewsets
from rest_framework.response import Response
from revel.logger import log
from vehicles.constants import LOW_BATTERY_LEVEL
from vehicles.models import Vehicle

from shifts.models import Shift, ShiftVehicle

from .serializers import ShiftAddVehicleSerializer, ShiftAutoCreateSerializer, ShiftSerializer, ShiftStatusSerializer


class ShiftViewSet(viewsets.ModelViewSet):
    """Generic viewsets for normal CRUD"""

    permission_classes = [permissions.AllowAny]
    http_method_names = ["get", "delete", "post"]
    pagination_class = None
    queryset = Shift.objects.all()
    serializer_class = ShiftSerializer


class ShiftAddVehicleView(views.APIView):
    """Add vehicles to a shift"""

    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        request_body=ShiftAddVehicleSerializer,
        responses={200: ShiftSerializer, 500: "Internal server error"},
    )
    def post(self, request, pk: int, *args, **kwargs):
        shift = get_object_or_404(Shift, pk=pk)

        serializer = ShiftAddVehicleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        vehicle_licenses = serializer.validated_data["vehicles"]

        # get vehicles from license plates
        new_vehicles = []
        for v in vehicle_licenses:
            vehicle: Vehicle = Vehicle.objects.filter(license_plate__iexact=v).first()
            if vehicle is None:
                log.warning(f"Tried to add an unregistered vehicle {v} to the shift {shift}")
                continue  # for now just ignore
            new_vehicles.append(vehicle)

        # add
        shift.add_vehicles(new_vehicles)

        # return shift serialized
        return Response(data=ShiftSerializer(shift).data)


class ShiftStatusView(views.APIView):
    """Query shift status"""

    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        responses={200: ShiftStatusSerializer, 500: "Internal server error"},
    )
    def get(self, request, pk: int, *args, **kwargs):
        shift = get_object_or_404(Shift, pk=pk)

        # return shift serialized
        return Response(data=ShiftStatusSerializer(shift).data)


class ShiftAutoCreateView(views.APIView):
    """Add vehicles automatically"""

    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        request_body=ShiftAutoCreateSerializer,
        responses={200: ShiftSerializer, 500: "Internal server error"},
    )
    def post(self, request, *args, **kwargs):
        print(request)
        serializer = ShiftAutoCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        start_point = (data["start_lat"], data["start_long"])
        count = data["count"]

        # below is assuming the same logic to the property Vehicle.can_be_added_to_shift but using query for performance
        vehicles = list(Vehicle.objects.exclude(in_use=True).filter(battery_level__lt=LOW_BATTERY_LEVEL))

        # sort
        vehicles = sorted(vehicles, key=lambda x: x.distance_to(start_point))

        # choose first {count} vehicles
        vehicles = vehicles[:count]

        # decide the visit order
        # a well-known travelling salesman problem and it's of NP hard
        # so will use a greedy algo that just picks the closest one at each step
        ordered_vehicles = []
        while len(ordered_vehicles) < len(vehicles):
            vehicles = sorted(vehicles, key=lambda x: x.distance_to(start_point))

            ordered_vehicles.append(vehicles[0])
            start_point = vehicles[0].location
            vehicles = vehicles[1:]

        # add to the shift
        shift: Shift = Shift.objects.create()
        shift_vehicles = [
            ShiftVehicle(shift=shift, vehicle=ordered_vehicles[i], order=i) for i in range(len(ordered_vehicles))
        ]
        ShiftVehicle.objects.bulk_create(shift_vehicles)

        # return shift serialized
        return Response(data=ShiftSerializer(shift).data)
