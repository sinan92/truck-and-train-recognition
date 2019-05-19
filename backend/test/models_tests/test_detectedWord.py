from unittest import TestCase

from nose.tools import assert_equal

from model.detected_word import DetectedWord


class TestDetectedWord(TestCase):
    dw = DetectedWord('0', 'WORD')

    def test_get_cam_index(self):
        index = self.dw.get_cam_index()
        assert_equal(index, '0')

    def test_get_word(self):
        word = self.dw.get_word()
        assert_equal(word, 'WORD')
