from django.urls import include, path
from rest_framework import routers

from vehicles.views import VehicleViewSet

router = routers.DefaultRouter()
router.register("", VehicleViewSet, "vehicles")

urlpatterns = [
    path("", include(router.urls)),
]
