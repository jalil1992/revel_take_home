
import json

from common.tests import RevelTestBase
from shifts.models import Shift
from vehicles.models import Vehicle


class TestShift(RevelTestBase):
    def setUp(self) -> None:
        super().setUp()

    def test_list_shifts(self):
        """Test listing all shifts"""
        response = self.client.get("/shifts/")
        self.assertEquals(response.status_code, 200)
        vehicles = response.json()
        self.assertTrue(len(vehicles) > 0)
