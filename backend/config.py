import os
import yaml

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
SAVE_PATH = os.path.join(ROOT_DIR, 'images', 'detected_trains')
MODEL_PATH = os.path.join(ROOT_DIR, 'trained-model', 'export', 'output_inference_graph_v1.pb',
                          'frozen_inference_graph.pb')

USE_GOOGLE = True
GOOGLE_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
GOOGLE_CREDENTIALS_PATH = os.path.join(ROOT_DIR, 'resources', 'google_credentials.json')
USE_AZURE = False


CONFIG = yaml.safe_load(open(os.path.join(ROOT_DIR, 'resources', 'config.yml')))

PROFILE = os.getenv('PROFILE15', 'dev')
print('Loading settings for: {0}'.format(PROFILE))

DATA_DIR = os.path.join(ROOT_DIR, CONFIG[PROFILE].get('data-dir'))
DB_CONNECTION = (CONFIG[PROFILE].get('database')).format(ROOT_DIR=ROOT_DIR, DATA_DIR=DATA_DIR)

HOST = CONFIG[PROFILE].get('host')
PORT = CONFIG[PROFILE].get('port')

db_setup = CONFIG[PROFILE].get('database-setup')
DB_DUMP = 'DUMP' in db_setup
DB_CREATE = 'CREATE' in db_setup
DB_SEED = 'SEED' in db_setup

STREAM_ADDRESS = '127.0.0.1'
STREAM_PORT = '5555'

RESOLUTION_H = 320
RESOLUTION_W = 320

# TEST
api_url = 'http://localhost'
api_port = '5002'

clean_database_on_startup = True

test_ports = [5000, 5004, 5005, 5006, 5007, 5008, 5009]
