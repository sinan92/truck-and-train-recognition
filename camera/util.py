import cv2
import base64


def image_to_string(image):
    encoded, buffer = cv2.imencode('.jpg', image)
    return base64.b64encode(buffer)
