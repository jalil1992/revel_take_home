from django.urls import include, path
from rest_framework import routers

from .views import ShiftViewSet

router = routers.DefaultRouter()
router.register("", ShiftViewSet, "shifts")

urlpatterns = [
    path("", include(router.urls)),
]
