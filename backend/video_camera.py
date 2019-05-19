import os
import time
from threading import Thread, ThreadError

import cv2

import config


class VideoCamera:
    def __init__(self, number):
        self.index = number
        self.video = cv2.VideoCapture(number)
        self.fps = self.video.get(cv2.CAP_PROP_FPS)
        self.current_state = None
        self.previous_state = None
        self.description = ''
        self.thread = Thread(target=self.run)
        self.thread.daemon = True
        self.thread_cancelled = False
        if not self.video.isOpened():
            raise ValueError('Camera ' + str(number) + ' not found.')

    def get_frame(self):
        ret, frame = self.video.read()
        frame = cv2.resize(frame, (500, 300))
        return frame

    def take_and_save_pictures(self):
        print("Taking pictures from Camera {}".format(self.index))
        if not os.path.exists(config.SAVE_PATH):
            os.makedirs(config.SAVE_PATH)

        save_place = os.path.join(config.SAVE_PATH, '{}-{}.jpg'.format(time.time(), self.index))
        cv2.imwrite(save_place, self.get_frame())

    def check_for_taking_pictures_conditions(self):
        if self.previous_state and not self.current_state:
            self.take_and_save_pictures()

    def update_state(self, state):
        self.previous_state = self.current_state
        self.current_state = state
        self.check_for_taking_pictures_conditions()

    def show(self, frame):
        cv2.imshow('Train detection Camera {}'.format(self.index), frame)

    def stop(self):
        print('Stopping Camera{}'.format(self.index))
        self.video.release()
        self.thread_cancelled = True

    def run(self):
        while not self.thread_cancelled:
            try:
                frame = self.get_frame()
                self.show(frame)
            except ThreadError:
                self.thread_cancelled = True
