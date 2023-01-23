import unittest
from unittest.mock import patch

from src.covmatic_robotcontrol.robot_api import RobotManagerHTTP, RobotManagerHTTPException

FAKE_ACTION_ID = "fakeactionid"
FAKE_HOST = "HOST"

ACTION_PICK = {
            "action": "pick",
            "machine": "OT1",
            "position": "SLOT1",
            "plate_name": "REAGENT"
        }

ACTION_ANSWER = {
    "action_id": FAKE_ACTION_ID
}

MALFORMED_ACTION_ANSWER = {
    "wrong": "field"
}

EXPECTED_URL = "http://HOST/action/pick/OT1/SLOT1/REAGENT"

class TestAPI(unittest.TestCase):
    def setUp(self) -> None:
        self._requests_patcher = patch('src.covmatic_robotcontrol.robot_api.requests')
        self._mock_requests = self._requests_patcher.start()
        self._api = RobotManagerHTTP(FAKE_HOST)

    def tearDown(self) -> None:
        self._requests_patcher.stop()


class TestActionRequest(TestAPI):
    def setUp(self) -> None:
        super().setUp()
        self._mock_requests.get.side_effect = [ACTION_ANSWER]

    def test_request_calls_get(self):
        self._api.action_request(ACTION_PICK)
        self._mock_requests.get.assert_called_once()

    def test_request_return_value(self):
        self.assertEqual(FAKE_ACTION_ID, self._api.action_request(ACTION_PICK))

    def test_wrong_answer_raises(self):
        self._mock_requests.get.side_effect = [MALFORMED_ACTION_ANSWER]
        with self.assertRaises(RobotManagerHTTPException):
            self._api.action_request(ACTION_PICK)

    def test_request_url(self):
        self._api.action_request(ACTION_PICK)
        self._mock_requests.get.assert_called_once_with(EXPECTED_URL)

