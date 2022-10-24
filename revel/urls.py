from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view


from rest_framework import routers

from vehicles.views import VehicleViewSet

router = routers.DefaultRouter()
router.register("vehicles", VehicleViewSet, "vehicles")

urlpatterns = [
    path("", include(router.urls)),
    path('vehicles/', include('vehicles.urls')),
    path('shifts/', include('shifts.urls')),
    re_path(r"^admin/", admin.site.urls),  # admin
]


# open api, limit views on production mode
openapi_info = openapi.Info(title="Revel API", default_version="v1", description="Documentation of API for Revel")
schema_view = get_schema_view(
    openapi_info,
    public=True,
    permission_classes=[],
)
urlpatterns += [
    re_path(r"^swagger(?P<format>\.json|\.yaml)$", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    re_path(r"^swagger/$", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    re_path(r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
