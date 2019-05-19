import time
from threading import Thread, ThreadError

import cv2

from constants import RESOLUTION_W, RESOLUTION_H, BLACK_SCREEN_URL


class Cam:
    # add username & password if it's authorized
    def __init__(self, url):
        self.url = url
        self.video = cv2.VideoCapture(url)
        self.thread_cancelled = False
        self.thread = Thread(target=self.run)
        self.thread.daemon = True
        self.current_frame = self.get_frame()

    def __del__(self):
        self.video.release()

    def start(self):
        self.thread.start()

    def is_running(self):
        return self.thread.isAlive()

    def shut_down(self):
        print("Closing Cam", self.url)
        self.thread_cancelled = True
        # block while waiting for thread to terminate
        while self.thread.isAlive():
            time.sleep(1)
        return True

    def run(self):
        while not self.thread_cancelled:
            frame = None
            try:
                frame = self.get_frame()
                frame = cv2.resize(frame, (RESOLUTION_W, RESOLUTION_H))
                self.current_frame = frame
            except ThreadError:
                self.thread_cancelled = True
            except Exception:
                # frame = self.get_black_screen()
                self.thread_cancelled=True

    def get_frame(self):
        ret1, frame = self.video.read()
        return frame

    def get_black_screen(self):
        image = cv2.imread(BLACK_SCREEN_URL)
        return image
