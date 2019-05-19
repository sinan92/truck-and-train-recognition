class Camera:
    def __init__(self, camera_id, description, connected):
        self.camera_id = camera_id
        self.description = description
        self.connected = connected

    def get_id(self):
        return self.camera_id

    def get_description(self):
        return self.description

    def is_connected(self):
        return self.connected

    @staticmethod
    def from_json(json_object):
        return Camera(json_object[0], json_object[1], json_object[2])

    def serialize(self):
        return {
            'camera_id': self.camera_id,
            'description': self.description,
            'connected': self.connected,
        }
