import datetime

from common.models import BaseModel
from django.db import models
from django.utils.translation import gettext_lazy as _
from vehicles.models import Vehicle


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
