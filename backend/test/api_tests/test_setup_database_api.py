import time
import unittest

from nose.tools import assert_equal

import config
from data import api
from test.api_tests.helper import Helper


class SetupDatabaseApiTests(unittest.TestCase):
    helper = Helper()

    @classmethod
    def setUpClass(cls):
        cls.api_thread = api.Api(config.HOST, cls.helper.get_port())
        cls.api_thread.start()
        time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        cls.helper.shutdown_api()

    def test_setup_database(self):
        response = self.helper.get_json_response('db/dump')
        assert_equal('success', response['message'])

        response = self.helper.get_json_response('db/create')
        assert_equal('success', response['message'])

        response = self.helper.get_json_response('db/seed')
        assert_equal('success', response['message'])

    def test_wrong_action_database(self):
        response = self.helper.get_json_response('db/dup')
        assert_equal('incorrect action (dump, create, seed)', response['message'])
