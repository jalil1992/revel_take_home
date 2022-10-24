from django.urls import include, path
from rest_framework import routers

from .views import ShiftViewSet

router = routers.DefaultRouter()
router.register("", ShiftViewSet, "shifts")

urlpatterns = [
    path("", include(router.urls)),
    # path("<int:pk>/add-vehicle/", views.ShiftAddVehicleView.as_view(), name="shift_add_vehicle"),
    # path("<int:pk>/check-status/", views.ShiftStatusView.as_view(), name="shift_check_status"),
    # path("auto-create/", views.ShiftAutoCreateView.as_view(), name="shift_auto_create"),
]
