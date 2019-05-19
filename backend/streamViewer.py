import argparse

import cv2
import numpy as np
import zmq
from zmq.backend.cython.constants import SUB, SUBSCRIBE, UNSUBSCRIBE

import config
from utilities.string_to_image_converter import string_to_image


class StreamViewer:
    def __init__(self, stream_address, port):
        context = zmq.Context()
        self.footage_socket = context.socket(SUB)
        self.footage_socket.bind('tcp://' + stream_address + ':' + port)
        self.footage_socket.setsockopt_string(SUBSCRIBE, np.unicode(''))
        self.current_frame = None
        self.keep_running = True

    def receive_stream(self):
        """Displays stream"""
        self.keep_running = True
        while self.footage_socket and self.keep_running:
            try:
                frame = self.footage_socket.recv_string()
                if frame == "STREAMSTOPPED":
                    cv2.destroyAllWindows()
                    self.keep_running = False
                    break
                self.current_frame = string_to_image(frame)
                cv2.imshow("Stream", self.current_frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.stop()
            except KeyboardInterrupt:
                self.stop()
                cv2.destroyAllWindows()
        print("Streaming Stopped")

    def stop(self):
        self.keep_running = False
        self.footage_socket.setsockopt_string(UNSUBSCRIBE, np.unicode(''))


def main():
    port = config.STREAM_PORT
    address = config.STREAM_ADDRESS

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--stream', required=False)
    parser.add_argument('-p', '--port', required=False)
    args = parser.parse_args()

    if args.port:
        port = args.port
    if args.stream:
        address = args.stream

    stream_viewer = StreamViewer(address, port)
    stream_viewer.receive_stream()


if __name__ == '__main__':
    main()
