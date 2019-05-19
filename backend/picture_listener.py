import os
from threading import Event

import config
from data import db
from ocr_providers.azure import Azure
from ocr_providers.google import Google


class PictureListener():
    def __init__(self, numbers):
        self.finished = False
        self.interval = 10.0
        self.old_picture_paths = []
        self.new_picture_paths = []
        self.number_of_cameras = numbers
        self.exit = Event()

    def shutdown(self):
        print('[Listener] Deactivated')
        self.finished = True
        self.exit.set()

    def start(self):
        print('[Listener] Activated')
        while not self.finished and not self.exit.is_set():
            self.task()
            self.exit.wait(self.interval)
        else:
            print('[INFO] Quiting the listener')

    def task(self):
        print('[Listener] Processing')
        if os.path.exists(config.SAVE_PATH):
            for file in os.listdir(config.SAVE_PATH):
                filename = os.fsdecode(file)
                if filename.endswith(".jpg"):
                    picture_path = os.path.join(config.SAVE_PATH, filename)
                    if len(self.old_picture_paths) != 0:
                        for path in self.old_picture_paths:
                            if path == picture_path:
                                os.remove(picture_path)
                                picture_path = ''
                        if picture_path is not '':
                            self.new_picture_paths.append(picture_path)
                    else:
                        self.new_picture_paths.append(picture_path)
                else:
                    continue

            if len(self.new_picture_paths) > 0 and config.USE_GOOGLE:
                print('[Listener] Using Google')
                try:
                    google = Google(self.new_picture_paths)
                    if len(google.detected_words) > 0:
                        for word in google.detected_words:
                            with open('detected.txt', 'a+') as f:
                                f.write(
                                    '[GOOGLE] C:{},W:{},T:{} \n'
                                        .format(str(word.get_cam_index()),
                                                word.get_word(),
                                                str(word.get_timestamp()))
                                )
                                db.RegisterDB.register(word.get_word(), word.get_cam_index())
                except Exception as error:
                    print(error)

            if len(self.new_picture_paths) > 0 and config.USE_AZURE:
                print('[Listener] Using Azure')
                try:
                    azure = Azure(self.new_picture_paths)
                    if len(azure.detected_words) > 0:
                        for word in azure.detected_words:
                            with open('detected.txt', 'a+') as f:
                                f.write(
                                    '[AZURE] C:{},W:{},T:{} \n'
                                        .format(str(word.get_cam_index()),
                                                word.get_word(),
                                                str(word.get_timestamp()))
                                )
                                db.RegisterDB.register(word.get_word(), word.get_cam_index())
                except Exception as error:
                    print('[PICTURE LISTENER]', error)

            self.old_picture_paths = self.new_picture_paths
            self.new_picture_paths = []
        else:
            print(config.SAVE_PATH, " doesn't exist")
