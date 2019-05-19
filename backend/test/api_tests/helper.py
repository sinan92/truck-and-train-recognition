import json

import requests

import config


class Helper:
    def __init__(self):
        self.port = config.test_ports.pop(0)
        config.clean_database_on_startup = True

    def get_response(self, url_suffix):
        response = requests.get('{0}:{1}/{2}'.format(config.api_url, self.port, url_suffix))
        return response

    def get_json_response(self, url_suffix):
        response = self.get_response(url_suffix)
        string = response.content.decode('utf-8')
        return json.loads(string)

    def get_port(self):
        return self.port

    def shutdown_api(self):
        self.get_response("shutdown")
        config.test_ports.append(self.port)
