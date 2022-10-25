
from django.conf import settings
from rest_framework.test import APITransactionTestCase
from vehicles.models import Vehicle


class RevelTestBase(APITransactionTestCase):
    settings.DEBUG = True
    settings.TEST = True

    def setUp(self) -> None:
        self.load_fixtures()
        return super().setUp()

    def load_fixtures(self) -> None:
        from vehicles.data import data
        vehicles = []
        for item in data:
            vehicles.append(Vehicle(
                # id=item['id'],
                license_plate=item['license_plate'],
                battery_level=item['battery_level'],
                in_use=item['in_use'],
                model=item['model'],
                location_lat=item['location'][0],
                location_long=item['location'][1],
            ))
        Vehicle.objects.bulk_create(vehicles)
