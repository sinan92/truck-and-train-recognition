import unittest

from test.api_tests.test_get_api import GetApiTests
from test.api_tests.test_setup_database_api import SetupDatabaseApiTests
from test.models_tests.test_camera import TestCamera
from test.models_tests.test_detectedWord import TestDetectedWord
from test.models_tests.test_wagon_model import WagonTestCase


def create_test_suites():
    suite = unittest.TestSuite()
    suite.addTest(SetupDatabaseApiTests('test_setup_database'))
    suite.addTest(SetupDatabaseApiTests('test_wrong_action_database'))
    suite.addTest(GetApiTests('test_request_response'))
    suite.addTest(GetApiTests('test_request_response_is_not_empty'))
    suite.addTest(GetApiTests('test_request_wagon_returns_one_item'))
    suite.addTest(GetApiTests('test_one_item_has_same_values_as_posted_json'))
    suite.addTest(GetApiTests('test_add_wagon_returns_succes'))
    suite.addTest(GetApiTests('test_delete_wagon'))
    suite.addTest(GetApiTests('test_get_camera'))
    suite.addTest(GetApiTests('test_change_camera_description'))
    suite.addTest(GetApiTests('test_get_history'))
    suite.addTest(WagonTestCase('test_get_wagon_id'))
    suite.addTest(WagonTestCase('test_get_last_camera'))
    suite.addTest(WagonTestCase('test_get_longitude'))
    suite.addTest(WagonTestCase('test_get_latitude'))
    suite.addTest(TestCamera('test_get_id'))
    suite.addTest(TestCamera('test_get_description'))
    suite.addTest(TestCamera('test_serialize'))
    suite.addTest(TestDetectedWord('test_get_cam_index'))
    suite.addTest(TestDetectedWord('test_get_word'))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(create_test_suites())
