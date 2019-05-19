import base64

import cv2
import numpy as np


def string_to_image(string):
    img = base64.b64decode(string)
    npimg = np.fromstring(img, dtype=np.uint8)
    return cv2.imdecode(npimg, 1)
