from threading import Event

from data.db import CameraDB


class DescriptionUpdater():
    def __init__(self, cameras_list):
        self.finished = False
        self.camera_list = cameras_list
        self.interval = 5.0
        self.exit = Event()

    def shutdown(self):
        """Stop this thread"""
        print('[INFO] Description Updater is DEACTIVATED')
        self.finished = True
        self.exit.set()

    def start(self):
        print('[INFO] Description Updater is ACTIVATED')
        while not self.finished and not self.exit.is_set():
            self.task()
            self.exit.wait(self.interval)
        else:
            print('[INFO] Quiting the Description Updater')

    def task(self):
        for camera in self.camera_list:
            cam = CameraDB.get_by_id(camera.index)
            camera.description = cam[0].get_description()
