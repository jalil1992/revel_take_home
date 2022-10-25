import json
import math
from random import shuffle

from common.tests import RevelTestBase
from django.urls import reverse
from shifts.models import Shift
from vehicles.models import Vehicle


class TestShift(RevelTestBase):
    def setUp(self) -> None:
        super().setUp()

    def test_general_shifts(self):
        """Test create/list/retrieve shifts"""
        # reset
        Shift.objects.all().delete()

        # create
        data = {"shift_date": "2022-10-27", "employee": 100}
        response = self.client.post("/shifts/generic/", data)
        self.assertEquals(response.status_code, 201)
        self.assertTrue(json.dumps(response.json()) == '{"shift_date": "2022-10-27", "employee": 100, "vehicles": []}')

        # list
        response = self.client.get("/shifts/generic/")
        self.assertEquals(response.status_code, 200)
        self.assertTrue(
            json.dumps(response.json()) == '[{"shift_date": "2022-10-27", "employee": 100, "vehicles": []}]'
        )

        # retrieve
        shift: Shift = Shift.objects.all().first()
        response = self.client.get(f"/shifts/generic/{shift.id}/")
        self.assertEquals(response.status_code, 200)
        self.assertTrue(json.dumps(response.json()) == '{"shift_date": "2022-10-27", "employee": 100, "vehicles": []}')

        # delete
        response = self.client.delete(f"/shifts/generic/{shift.id}/")
        self.assertEquals(response.status_code, 204)

    def test_add_vehicles_manual(self):
        """Test add vehicles to a shift manually"""
        # reset
        Shift.objects.all().delete()

        # create
        data = {"shift_date": "2022-10-27", "employee": 100}
        response = self.client.post("/shifts/generic/", data)
        self.assertEquals(response.status_code, 201)

        # prepare data
        shift: Shift = Shift.objects.all().first()
        vehicles = Vehicle.objects.filter(in_use=False, battery_level__lt=20)
        vehicle_licenses = [v.license_plate for v in vehicles]
        data = {"vehicles": vehicle_licenses}

        # add
        response = self.client.post(reverse("shift_add_vehicle", args=[shift.id]), data)
        self.assertEquals(response.status_code, 200)
        self.assertTrue(response.json()["vehicles"] == vehicle_licenses)

        # check status
        response = self.client.get(reverse("shift_check_status", args=[shift.id]))
        self.assertEquals(response.status_code, 200)
        self.assertTrue(json.dumps(response.json()) == '{"is_completed": false, "finished_vehicles": []}')

        # complete swap for the first two
        response = self.client.put(f"/vehicles/{vehicles[0].id}/", {"battery_level": 100})
        response = self.client.put(f"/vehicles/{vehicles[1].id}/", {"battery_level": 100})

        # check status
        response = self.client.get(reverse("shift_check_status", args=[shift.id]))
        self.assertEquals(response.status_code, 200)
        self.assertTrue(response.json()["finished_vehicles"] == vehicle_licenses[:2])

        # complete all
        for v in vehicles[2:]:
            response = self.client.put(f"/vehicles/{v.id}/", {"battery_level": 100})
            self.assertEquals(response.status_code, 200)

        # check status
        response = self.client.get(reverse("shift_check_status", args=[shift.id]))
        self.assertEquals(response.status_code, 200)
        self.assertTrue(response.json()["is_completed"] == True)

    def test_add_vehicles_auto(self):
        """Test add vehicles to a shift automatically"""
        # reset
        Shift.objects.all().delete()
        Vehicle.objects.all().delete()

        # create 100 vehicles, 20 lying on the spiral of radius 20, 80 lying on the circle of radius 30
        start_point = (43.54, 34.52)

        vehicles = []
        for i in range(20):
            x = start_point[0] + (20 + i) * math.cos(2 * math.pi * i / 20)
            y = start_point[1] + (20 + i) * math.sin(2 * math.pi * i / 20)
            vehicles.append(
                Vehicle(
                    license_plate=f"RANGE_20_{i}",
                    battery_level=0,
                    in_use=False,
                    location_lat=x,
                    location_long=y,
                )
            )

        for i in range(80):
            x = start_point[0] + 80 * math.cos(2 * math.pi * i / 80)
            y = start_point[1] + 80 * math.sin(2 * math.pi * i / 80)
            vehicles.append(
                Vehicle(
                    license_plate=f"RANGE_80_{i}",
                    battery_level=0,
                    in_use=False,
                    location_lat=x,
                    location_long=y,
                )
            )

        shuffle(vehicles)  # shuffle the vehicles to check if we get consistent results
        Vehicle.objects.bulk_create(vehicles)

        # auto create, should use the vehicles on the circle of radius 20
        data = {
            "start_lat": start_point[0],
            "start_long": start_point[1],
            "count": 20,
        }
        response = self.client.post(reverse("shift_auto_create"), data)
        self.assertEquals(response.status_code, 200)
        self.assertTrue(
            response.json()["vehicles"]
            == [
                "RANGE_20_0",
                "RANGE_20_1",
                "RANGE_20_2",
                "RANGE_20_3",
                "RANGE_20_4",
                "RANGE_20_5",
                "RANGE_20_6",
                "RANGE_20_7",
                "RANGE_20_8",
                "RANGE_20_9",
                "RANGE_20_10",
                "RANGE_20_11",
                "RANGE_20_12",
                "RANGE_20_13",
                "RANGE_20_14",
                "RANGE_20_15",
                "RANGE_20_16",
                "RANGE_20_17",
                "RANGE_20_18",
                "RANGE_20_19",
            ]
        )
