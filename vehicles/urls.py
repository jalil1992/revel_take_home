from django.urls import path

from . import views

urlpatterns = [
    path('', views.list_vehicles, name='list_vehicles'),
]
