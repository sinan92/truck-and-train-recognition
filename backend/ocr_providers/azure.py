import time

import requests


class Azure:

    def __init__(self, paths):
        self.paths = paths
        self.ocr_url = self.set_ocr_url()
        self.image_data = self.read_images(self.paths)
        self.subscription_key = "e4763182f36d4dc6997b3e19785397aa"
        self.detected_words = []
        self.begin()

    def begin(self):
        self.detected_words = []
        image_data = self.read_images(self.paths)
        for image in image_data:
            self.make_prediction(image, self.ocr_url)
            time.sleep(1)

    def set_ocr_url(self):
        vision_base_url = "https://westeurope.api.cognitive.microsoft.com/vision/v2.0/"
        analyze_url = vision_base_url + "ocr"
        return analyze_url

    def read_images(self, image_paths):
        image_data = []
        for image_path in image_paths:
            image_data.append(open(image_path, "rb").read())
        return image_data

    def make_prediction(self, image_data, analyze_url):
        print('[INFO] AZURE make_prediction url: {}'.format(analyze_url))
        headers = {'Ocp-Apim-Subscription-Key': self.subscription_key,
                   'Content-Type': 'application/octet-stream'}
        params = {'language': 'unk', 'detectOrientation': 'true'}
        response = requests.post(analyze_url, headers=headers, params=params, data=image_data)
        response.raise_for_status()
        analyis = response.json()
        self.log(analyis)

    def log(self, analysis):
        print('[INFO] AZURE log size: {}'.format(len(analysis["regions"])))
        if len(analysis["regions"]) > 0:
            line_infos = [region["lines"] for region in analysis["regions"]]
            word_infos = []
            for line in line_infos:
                print("[INFO] azure detected Line : {}".format(line))
                for word_metadata in line:
                    for word_info in word_metadata["words"]:
                        word_infos.append(word_info['text'])

            for word in word_infos:
                self.detected_words.append(word)
