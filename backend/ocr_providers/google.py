import io

from google.cloud import vision

from model.detected_word import DetectedWord


class Google:
    def __init__(self, paths):
        self.client = vision.ImageAnnotatorClient()
        self.paths = paths
        self.detected_words = []
        self.detect()

    def detect(self):
        self.detected_words = []
        for path in self.paths:
            with io.open(path, 'rb') as image_file:
                content = image_file.read()

            image = vision.types.Image(content=content)

            response = self.client.text_detection(image=image)
            texts = response.text_annotations
            cam_index = path.split('-')
            cam_index = cam_index[len(cam_index)-1].split('.')
            for text in texts:
                word = DetectedWord(cam_index[0] , text.description)
                if word.get_word() not in self.detected_words and "\n" not in text.description:
                    self.detected_words.append(word)
