import math
from typing import Tuple

from common.models import BaseModel
from django.db import models
from django.utils.translation import gettext_lazy as _

from vehicles.constants import LOW_BATTERY_LEVEL


class VehicleModelEnum(models.TextChoices):
    NIU = "Niu", _("Niu")
    UNKNOWN = "Unknown", _("Unknown")


class Vehicle(BaseModel):
    license_plate = models.CharField(
        max_length=255, verbose_name=_("License plate"), help_text=_("License plat for this vehicle"), db_index=True
    )
    battery_level = models.IntegerField(
        default=100, verbose_name=_("Battery level"), help_text=_("Battery level of this vehicle. Ranges 0 ~ 100.")
    )
    in_use = models.BooleanField(
        default=False, verbose_name=_("In use"), help_text=_("Represents if the vehicle is in use.")
    )
    model = models.CharField(
        max_length=255,
        choices=VehicleModelEnum.choices,
        default=VehicleModelEnum.UNKNOWN,
        verbose_name=_("Model"),
        help_text=_("The brand model name of this vehicle."),
    )
    location_lat = models.FloatField(default=0, verbose_name=_("Latitude"), help_text=_("Current location latitude."))
    location_long = models.FloatField(
        default=0, verbose_name=_("Longitude"), help_text=_("Current location longitude.")
    )

    def __str__(self):
        """License plate will be used to identify vehicles"""
        return self.license_plate

    @property
    def need_swap_battery(self) -> bool:
        """Define the status of <need a swap>"""
        return self.battery_level < LOW_BATTERY_LEVEL

    @property
    def can_be_added_to_shift(self) -> bool:
        """Assume some logic here, only if the vehicle is running out of battery and it's not in use I assumt it can be added to a shift"""
        return not self.in_use and self.need_swap_battery

    @property
    def location(self) -> Tuple[float, float]:
        return (self.location_lat, self.location_long)

    def distance_to(self, p: Tuple[float, float]) -> float:
        """Distance to a point"""
        return math.dist(self.location, p)
