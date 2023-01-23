import unittest

from src.covmatic_robotcontrol.robot_station import RobotStationABC


class FakeStation(RobotStationABC):
    def _tipracks(self) -> dict:
        return {}


class TestStation(unittest.TestCase):
    def test_station_run(self):
        station = FakeStation(ot_name="OT1")
        station.simulate()

