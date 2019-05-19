import time
import unittest

from nose.tools import assert_equal

import config
from data import api
from model.wagon import Wagon
from test.api_tests.helper import Helper


class WagonTestCase(unittest.TestCase):
    wagon = Wagon('1234', '1')
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

    def test_get_wagon_id(self):
        id = '1234'
        assert_equal(self.wagon.get_id(), id)

    def test_get_last_camera(self):
        camera = '1'
        assert_equal(self.wagon.get_last_camera(), camera)

    def test_get_longitude(self):
        longitude = 0
        assert_equal(self.wagon.get_longitude(), longitude)

    def test_get_latitude(self):
        latitude = 0
        assert_equal(self.wagon.get_latitude(), latitude)
