import datetime

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    created_at = models.DateTimeField(db_index=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

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

class Shift(BaseModel):
    shift_date = models.DateField(default=datetime.date.today, verbose_name = _(u'Shift date'), help_text = _(u'Date for this shift.'))
    employee = models.IntegerField(default=0, verbose_name = _(u'Employee'), help_text = _(u'Employee (ID) responsible for this shift.')) # supposed to be foreign key to the employee model
    vehicles = models.ManyToManyField(Vehicle, through = 'ShiftVehicle', blank=True, related_name="shifts", verbose_name = _(u'Vehicles'), help_text = _(u'Vehicles of this shift.'))

    def __str__(self):
        return f'Shift #{self.id} of #{self.employee} ({self.shift_date.strftime("%m-%d-%Y %a")})'


class ShiftVehicle(models.Model):
    vehicle = models.ForeignKey(Vehicle, verbose_name = _(u'Vehicle'), help_text = _(u'Vehicle is assigned to this shift.'), on_delete=models.CASCADE)
    shift = models.ForeignKey(Shift, verbose_name = _(u'Shift'), help_text = _(u'Vehicle is assigned to this shift.'), on_delete=models.CASCADE)
    order = models.IntegerField(verbose_name = _(u'Order'), help_text = _(u'What order to visit vehicles for this shift.'))

    class Meta:
        verbose_name = _(u"Shift Vehicle Mapping")
        verbose_name_plural = _(u"Shift Vehicle Mappings")
        ordering = ['order',]
