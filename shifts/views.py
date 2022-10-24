from django.http import JsonResponse
from rest_framework import permissions, views, viewsets

from shifts.models import Shift

from .serializers import ShiftSerializer


class ShiftViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    http_method_names = ["get", "delete", "post"]
    pagination_class = None
    queryset = Shift.objects.all()
    serializer_class=ShiftSerializer
