import argparse

import cv2
import zmq
from zmq.backend.cython.constants import PUB

from cam import Cam
from constants import PORT, SERVER_ADDRESS, CAM_URL
from util import image_to_string


class Streamer:
    def __init__(self, camera, server_address=SERVER_ADDRESS, port=PORT):
        """Creates socket and connects to address. Default address is localhost. Default port is 5555."""
        self.cam = camera
        print("Connecting to", server_address, "at", port)
        context = zmq.Context()
        self.footage_socket = context.socket(PUB)
        self.footage_socket.connect('tcp://' + server_address + ':' + port)
        self.keep_running = True

    def start(self):
        """Starts the cam and sends the stream"""
        print("Streaming Started.\nPress Ctrl + C to exit.")
        self.cam.start()
        self.keep_running = True

        while self.footage_socket and self.keep_running and self.cam.is_running():
            try:
                frame = self.cam.current_frame
                image_as_string = image_to_string(frame)
                self.footage_socket.send(image_as_string)
            except KeyboardInterrupt:
                self.keep_running = False
                cv2.destroyAllWindows()
        else:
            self.stop()
            cv2.destroyAllWindows()
            print("Streaming Stopped.")

    def stop(self):
        self.footage_socket.send_string("STREAMSTOPPED")
        self.keep_running = False
        self.cam.shut_down()


def main():
    """Initializes a camera. Initializes a streamer. Opens the camera when using the "start" method.
    When the streamer is started, it gets the frames from the camera and sends it to the server."""
    cam_url = CAM_URL
    port = PORT
    server_address = SERVER_ADDRESS

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--server', required=False)
    parser.add_argument('-p', '--port', required=False)
    parser.add_argument('-c', '--cam', required=False)
    args = parser.parse_args()

    if args.port:
        port = args.port
    if args.server:
        server_address = args.server
    if args.cam:
        cam_url = args.cam

    cam = Cam(cam_url)
    streamer = Streamer(cam, server_address, port)
    streamer.start()


if __name__ == '__main__':
    main()
