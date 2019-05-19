import time
import unittest

from nose.tools import assert_true, assert_is_not_none, assert_equal, assert_greater

import config
from data import api
from model.wagon import Wagon
from test.api_tests.helper import Helper


class GetApiTests(unittest.TestCase):
    helper = Helper()

    @classmethod
    def setUpClass(cls):
        cls.api_thread = api.Api(config.HOST, cls.helper.get_port())
        cls.api_thread.start()
        api.db.WagonDB.add_wagon(Wagon('HALLO', 0, 0, 0))
        api.db.RegisterDB.register('HALLO', 1)
        time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        cls.helper.shutdown_api()

    def test_request_response(self):
        response = self.helper.get_response('wagon/')
        assert_true(response.ok)

    def test_request_response_is_not_empty(self):
        response = self.helper.get_json_response('wagon/')
        assert_is_not_none(response)

    def test_request_wagon_returns_one_item(self):
        response = self.helper.get_json_response('wagon/HALLO')
        assert_equal(1, len(response))

    def test_one_item_has_same_values_as_posted_json(self):
        response = self.helper.get_json_response('wagon/HALLO')
        assert_equal(1, response[0]['last_camera'])
        assert_equal('HALLO', response[0]['wagon_id'])

    def test_add_wagon_returns_succes(self):
        response = self.helper.get_json_response('wagon/new/1234')
        assert_equal('success', response['message'])

    def test_add_the_same_wagon_returns_failure(self):
        self.helper.get_json_response('wagon/new/1235')
        response = self.helper.get_json_response('wagon/new/1235')
        assert_equal('failed to add wagon', response['message'])

    def test_delete_wagon(self):
        response = self.helper.get_json_response('wagon/delete/1235')
        assert_equal('success', response['message'])

    def test_get_camera(self):
        response = self.helper.get_json_response('camera/0')
        assert_equal(0, response[0]['camera_id'])

    def test_change_camera_description(self):
        response = self.helper.get_json_response('camera/0/description/00')
        assert_equal('success', response['message'])

    def test_get_history(self):
        response = self.helper.get_json_response('history')
        assert_greater(len(response), 0)
