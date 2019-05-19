import datetime


class DetectedWord:
    def __init__(self, cam_index, word):
        self.cam_index = cam_index
        self.word = word

    def get_cam_index(self):
        return self.cam_index

    def get_word(self):
        return self.word

    def get_timestamp(self):
        return datetime.datetime.now()

    def print(self):
        print('Cam: {}'.format(self.cam_index))
        print('Word: {}'.format(self.word))
