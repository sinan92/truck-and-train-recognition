from unittest import TestCase

from nose.tools import assert_equal

from model.camera import Camera


class TestCamera(TestCase):
    obj = ['2', 'camera 2']
    cam = Camera(1, 'camera 1')

    def test_get_id(self):
        id = self.cam.get_id()
        assert_equal(str(id), '1')

    def test_get_description(self):
        description = self.cam.get_description()
        assert_equal(description, 'camera 1')

    def test_serialize(self):
        cam = Camera.from_json(self.obj)
        cam_serialized = cam.serialize()
        assert_equal(cam_serialized, {'camera_id': '2', 'description': 'camera 2'})
