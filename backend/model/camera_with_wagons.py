class CameraWithWagons:
    def __init__(self, camera, wagons):
        self.camera = camera
        self.wagons = wagons

    def get_camera(self):
        return self.camera

    def get_wagons(self):
        return self.wagons

    def serialize(self):
        return {
            'camera_id': self.camera.get_id(),
            'description': self.camera.get_description(),
            'connected': self.camera.is_connected(),
            'wagons': [w.serialize() for w in self.wagons]
        }
