import datetime

from common.models import BaseModel
from django.db import models
from django.utils.translation import gettext_lazy as _


class VehicleModelEnum(models.TextChoices):
    NIU = "Niu", _("Niu")
    UNKNOWN = "Unknown", _("Unknown")

class Vehicle(BaseModel):
    license_plate = models.CharField(max_length=255, verbose_name = _(u'License plate'), help_text = _(u'License plat for this vehicle'))
    battery_level= models.IntegerField(default=100, verbose_name = _(u'Battery level'), help_text = _(u'Battery level of this vehicle. Ranges 0 ~ 100.'))
    in_use = models.BooleanField(default=False, verbose_name = _(u'In use'), help_text = _(u'Represents if the vehicle is in use.'))
    model = models.CharField(max_length=255, choices=VehicleModelEnum.choices, default=VehicleModelEnum.UNKNOWN, verbose_name = _(u'Model'), help_text = _(u'The brand model name of this vehicle.'))
    location_lat = models.FloatField(default=0, verbose_name = _(u'Latitude'), help_text = _(u'Current location latitude.'))
    location_long = models.FloatField(default=0, verbose_name = _(u'Longitude'), help_text = _(u'Current location longitude.'))

    def __str__(self):
        """License plate will be used to identify vehicles"""
        return self.license_plate

    @property
    def need_swap_battery(self):
        """Define the status of <need a swap>"""
        return self.battery_level < 10
