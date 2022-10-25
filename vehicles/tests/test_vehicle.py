
import json

from common.tests import RevelTestBase
from vehicles.models import Vehicle


class TestVehicle(RevelTestBase):
    def setUp(self) -> None:
        super().setUp()

    def test_list_vehicles(self):
        """Test listing all vehicles"""
        response = self.client.get("/vehicles/")
        self.assertEquals(response.status_code, 200)
        vehicles = response.json()
        self.assertTrue(len(vehicles) > 0)

    def test_create_vehicle(self):
        """Test creating a vehicle"""
        data = {
            "license_plate":"TEST001",
            "model":"Niu",
            "location_lat":42.356,
            "location_long":32.302,
        }
        response = self.client.post("/vehicles/", data)
        self.assertEquals(response.status_code, 201)
        new_vehicle = response.json()
        self.assertTrue(json.dumps(new_vehicle) == '{"license_plate": "TEST001", "battery_level": 100, "in_use": false, "model": "Niu", "location_lat": 42.356, "location_long": 32.302}')

    def test_update_vehicle(self):
        """Test updating a vehicle"""
        new_vehicle = Vehicle.objects.create(license_plate='TEST002', model='Niu', location_lat=38.32, location_long=-23.35)
        data = {
            "location_lat":42.356,
            "location_long":32.302,
            "in_use":True,
            "battery_level":58,
        }
        response = self.client.put(f"/vehicles/{new_vehicle.id}/", data)
        self.assertEquals(response.status_code, 200)
        response = self.client.get(f"/vehicles/{new_vehicle.id}/")
        self.assertEquals(response.status_code, 200)
        self.assertTrue(json.dumps(response.json()) == '{"license_plate": "TEST002", "battery_level": 58, "in_use": true, "model": "Niu", "location": [42.356, 32.302]}')
        response = self.client.delete(f"/vehicles/{new_vehicle.id}/")
        self.assertEquals(response.status_code, 204)
