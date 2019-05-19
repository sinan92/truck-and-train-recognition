from data import db


class History:
    def __init__(self, wagon_id, camera_id, timestamp):
        self.wagon_id = wagon_id
        self.camera_id = camera_id
        self.timestamp = timestamp

    def get_wagon_id(self):
        return self.wagon_id

    def get_camera_id(self):
        return self.camera_id

    def get_timestamp(self):
        return self.timestamp

    @staticmethod
    def from_json(json_object):
        return History(json_object[0], json_object[1], json_object[2])

    def serialize(self):
        return {
            'wagon_id': self.wagon_id,
            'camera_id': self.camera_id,
            'description': db.CameraDB.get_by_id(self.camera_id)[0].get_description(),
            'timestamp': self.timestamp,
        }
