import datetime
from typing import List

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

    def add_vehicles(self, vehicles:List[Vehicle])->int:
        """Add vehicles to the end of the shift and return the shift size"""
        # get the last order
        orders = self.vehicles.all().values_list('order', flat=True)
        max_order = max(orders)

        # add vehicle one by one to the end of the shift
        new_shift_vehicles = []
        v:Vehicle
        for v in vehicles:
            if v.can_be_added_to_shift:
                continue # <- possible consideration: might need to check if vehicle is in use, if it needs swap ...

            new_shift_vehicles.append(
                ShiftVehicle(shift=self, vehicle=v, order = max_order)
            )
            max_order += 1

        # bulk create
        ShiftVehicle.objects.bulk_create(new_shift_vehicles)

        return self.vehicles.all().count()

    @property
    def finished_vehicles(self)->List[str]:
        return [v.license_plate for v in self.vehicles.all() if not v.need_swap_battery]

    @property
    def is_completed(self)->bool:
        finished = self.finished_vehicles
        return len(finished) == self.vehicles.all().count()


class ShiftVehicle(models.Model):
    vehicle = models.ForeignKey(Vehicle, verbose_name = _(u'Vehicle'), help_text = _(u'Vehicle is assigned to this shift.'), on_delete=models.CASCADE)
    shift = models.ForeignKey(Shift, verbose_name = _(u'Shift'), help_text = _(u'Vehicle is assigned to this shift.'), on_delete=models.CASCADE)
    order = models.IntegerField(verbose_name = _(u'Order'), help_text = _(u'What order to visit vehicles for this shift.'))

    class Meta:
        verbose_name = _(u"Shift Vehicle Mapping")
        verbose_name_plural = _(u"Shift Vehicle Mappings")
        ordering = ['order',]
