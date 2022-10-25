from django.urls import include, path
from rest_framework import routers

from .views import ShiftAddVehicleView, ShiftAutoCreateView, ShiftStatusView, ShiftViewSet

router = routers.DefaultRouter()
router.register("", ShiftViewSet, "shifts")

urlpatterns = [
    path("generic/", include(router.urls)),
    path(
        "manage/",
        include(
            [
                path("auto-create/", ShiftAutoCreateView.as_view(), name="shift_auto_create"),
                path(
                    "add-vehicle/<int:pk>/",
                    ShiftAddVehicleView.as_view(),
                    name="shift_add_vehicle",
                ),
                path(
                    "check-status/<int:pk>/",
                    ShiftStatusView.as_view(),
                    name="shift_check_status",
                ),
            ]
        ),
    ),
]
