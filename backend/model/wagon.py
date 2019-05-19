class Wagon:
    def __init__(self, wagon_id, last_camera=0, last_timestamp=None, latitude=0, longitude=0):
        self.wagon_id = wagon_id
        self.last_camera = last_camera
        self.last_timestamp = last_timestamp
        self.latitude = latitude
        self.longitude = longitude

    def get_id(self):
        return self.wagon_id

    def get_last_camera(self):
        return self.last_camera

    def get_last_timestamp(self):
        return self.last_timestamp

    def get_latitude(self):
        return self.latitude

    def get_longitude(self):
        return self.longitude

    @staticmethod
    def from_json(json_object):
        return Wagon(json_object[0], json_object[1], json_object[2], json_object[3], json_object[4])

    def serialize(self):
        return {
            'wagon_id': self.wagon_id,
            'last_camera': self.last_camera,
            'last_timestamp': self.last_timestamp,
            'latitude': self.latitude,
            'longitude': self.longitude,
        }
