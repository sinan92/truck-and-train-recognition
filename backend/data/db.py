import datetime
import os
from sqlite3 import OperationalError

from sqlalchemy import create_engine

import config as config
from model.camera import Camera
from model.camera_with_wagons import CameraWithWagons
from model.history import History
from model.wagon import Wagon

db_connect = create_engine(config.DB_CONNECTION)


class WagonDB:
    @staticmethod
    def get_all():
        conn = db_connect.connect()
        query = conn.execute("SELECT * FROM WAGONS;")
        return WagonDB.__create_objects(query)

    @staticmethod
    def get_by_id(wagon_id):
        conn = db_connect.connect()
        query = conn.execute("SELECT * FROM WAGONS WHERE wagon_id = '{0}';".format(wagon_id))
        return WagonDB.__create_objects(query)

    @staticmethod
    def get_by_camera(camera_id):
        conn = db_connect.connect()
        query = conn.execute("SELECT * FROM WAGONS WHERE last_camera_id = '{0}';".format(camera_id))
        return WagonDB.__create_objects(query)

    @staticmethod
    def update_or_add_wagon_coordinates(wagon):
        conn = db_connect.connect()

        wagon_id = wagon.get_id()
        longitude = wagon.get_longitude()
        latitude = wagon.get_latitude()

        count = [i for i in
                 conn.execute("SELECT COUNT(*) FROM WAGONS WHERE wagon_id = '{0}';".format(wagon_id))
                     .cursor.fetchall()][0][0]

        if count is 0:
            WagonDB.add_wagon(wagon)

        count = [i for i in
                 conn.execute("SELECT COUNT(*) FROM WAGONS WHERE wagon_id = '{0}';".format(wagon_id))
                     .cursor.fetchall()][0][0]

        if count is 1:
            try:
                conn.execute("UPDATE WAGONS SET longitude = '{0}' WHERE wagon_id = '{1}';".format(longitude, wagon_id))
                conn.execute("UPDATE WAGONS SET latitude = '{0}' WHERE wagon_id = '{1}';".format(latitude, wagon_id))
                return True
            except ImportError:
                return False
        else:
            return False

    @staticmethod
    def update_last_camera_id(wagon):
        conn = db_connect.connect()

        wagon_id = wagon.get_id()
        last_camera_id = wagon.get_last_camera()
        last_timestamp = wagon.get_last_timestamp()

        count = [i for i in
                 conn.execute("SELECT COUNT(*) FROM WAGONS WHERE wagon_id = '{0}';".format(wagon_id))
                     .cursor.fetchall()][0][0]
        if count is 1:
            try:
                conn.execute(
                    "UPDATE WAGONS SET last_camera_id = '{0}' WHERE wagon_id = '{1}';".format(last_camera_id, wagon_id))
                conn.execute(
                    "UPDATE WAGONS SET last_timestamp = '{0}' WHERE wagon_id = '{1}';".format(last_timestamp, wagon_id))
                return True
            except ImportError:
                return False
        else:
            return False

    @staticmethod
    def add_wagon(wagon):
        conn = db_connect.connect()

        wagon_id = wagon.get_id()

        count = [i for i in
                 conn.execute("SELECT COUNT(*) FROM WAGONS WHERE wagon_id = '{0}';".format(wagon_id))
                     .cursor.fetchall()][0][0]
        if count is 0:
            try:
                conn.execute(
                    "INSERT INTO WAGONS (wagon_id) VALUES ('{0}');".format(wagon_id))
                return True
            except ImportError:
                return False
        else:
            return False

    @staticmethod
    def delete_wagon(wagon):
        conn = db_connect.connect()

        wagon_id = wagon.get_id()

        count = [i for i in
                 conn.execute("SELECT COUNT(*) FROM WAGONS WHERE wagon_id = '{0}';".format(wagon_id))
                     .cursor.fetchall()][0][0]
        if count is 1:
            try:
                conn.execute(
                    "DELETE FROM WAGONS WHERE wagon_id = {0};".format(wagon_id))
                return True
            except ImportError:
                return False
        else:
            return True

    @staticmethod
    def __create_objects(query):
        return_list = []
        for wagon in [i for i in query.cursor.fetchall()]:
            return_list.append(Wagon.from_json(wagon))
        return return_list


class CameraDB:
    @staticmethod
    def get_all():
        conn = db_connect.connect()
        query = conn.execute("SELECT * FROM CAMERAS;")
        return CameraDB.__create_objects(query)

    @staticmethod
    def get_by_id(camera_id):
        conn = db_connect.connect()
        query = conn.execute("SELECT * FROM CAMERAS WHERE camera_id = '{0}';".format(camera_id))
        return CameraDB.__create_objects(query)

    @staticmethod
    def get_with_wagons():
        list = []
        for c in CameraDB.get_all():
            co = CameraWithWagons(c, WagonDB.get_by_camera(c.get_id()))
            list.append(co)
        return list

    @staticmethod
    def save_description(camera):
        conn = db_connect.connect()

        camera_id = camera.get_id()
        camera_description = camera.get_description()

        count = [i for i in
                 conn.execute("SELECT COUNT(*) FROM CAMERAS WHERE camera_id = '{0}';".format(camera_id))
                     .cursor.fetchall()][0][0]
        if count is 1:
            try:
                conn.execute(
                    "UPDATE CAMERAS SET description = '{0}' WHERE camera_id = '{1}';".format(camera_description,
                                                                                             camera_id))
                return True
            except ImportError:
                return False
        else:
            try:
                conn.execute(
                    "INSERT INTO CAMERAS (camera_id, description) VALUES ('{0}','{1}');".format(camera_id,
                                                                                                camera_description))
                return True
            except ImportError:
                return False

    @staticmethod
    def connect(camera_id):
        conn = db_connect.connect()

        count = [i for i in
                 conn.execute("SELECT COUNT(*) FROM CAMERAS WHERE camera_id = '{0}';".format(camera_id))
                     .cursor.fetchall()][0][0]
        if count is 1:
            try:
                conn.execute(
                    "UPDATE CAMERAS SET connected = 'true' WHERE camera_id = '{1}';".format(camera_id))
                return True
            except ImportError:
                return False
        else:
            return False

    @staticmethod
    def disconnect(camera_id):
        conn = db_connect.connect()

        count = [i for i in
                 conn.execute("SELECT COUNT(*) FROM CAMERAS WHERE camera_id = '{0}';".format(camera_id))
                     .cursor.fetchall()][0][0]
        if count is 1:
            try:
                conn.execute(
                    "UPDATE CAMERAS SET connected = 'false' WHERE camera_id = '{1}';".format(camera_id))
                return True
            except ImportError:
                return False
        else:
            return False

    @staticmethod
    def __create_objects(query):
        return_list = []
        for camera in [i for i in query.cursor.fetchall()]:
            return_list.append(Camera.from_json(camera))
        return return_list


class HistoryDB:
    @staticmethod
    def get_all():
        conn = db_connect.connect()
        query = conn.execute("SELECT * FROM HISTORY;")
        return HistoryDB.__create_objects(query)

    @staticmethod
    def get_recent():
        conn = db_connect.connect()
        query = conn.execute("SELECT * FROM HISTORY LIMIT 10 OFFSET (SELECT COUNT(*) FROM HISTORY)-10;")
        return HistoryDB.__create_objects(query)

    @staticmethod
    def get_by_wagon_id(wagon_id):
        conn = db_connect.connect()
        query = conn.execute("SELECT * FROM HISTORY WHERE wagon_id = '{0}';".format(wagon_id))
        return HistoryDB.__create_objects(query)

    @staticmethod
    def get_by_camera_id(camera_id):
        conn = db_connect.connect()
        query = conn.execute("SELECT * FROM HISTORY WHERE camera_id = '{0}';".format(camera_id))
        return HistoryDB.__create_objects(query)

    @staticmethod
    def add_item(history):
        conn = db_connect.connect()

        wagon_id = history.wagon_id
        camera_id = history.camera_id
        timestamp = history.timestamp

        try:
            conn.execute(
                "INSERT INTO HISTORY (wagon_id, camera_id, timestamp) VALUES ('{0}',{1},'{2}');".format(wagon_id,
                                                                                                        camera_id,
                                                                                                        timestamp))
            return True
        except ImportError:
            return False

    @staticmethod
    def __create_objects(query):
        return_list = []
        for history in [i for i in query.cursor.fetchall()]:
            return_list.append(History.from_json(history))
        return return_list


class RegisterDB:
    @staticmethod
    def register(wagon_id, camera_id):
        current_camera = WagonDB.get_by_id(wagon_id)[0].get_last_camera()
        if current_camera is not None and int(current_camera) is int(camera_id):
            return True
        else:
            w = Wagon(wagon_id, camera_id, datetime.datetime.now())
            h = History(wagon_id, camera_id, datetime.datetime.now())
            if WagonDB.update_last_camera_id(w) and HistoryDB.add_item(h):
                return True
            else:
                return False


class Database:
    @staticmethod
    def dump():
        file = open(os.path.join(config.DATA_DIR, 'scripts/db-dump.sql'), 'r')
        Database.__process(file)

    @staticmethod
    def create():
        file = open(os.path.join(config.DATA_DIR, 'scripts/db-create.sql'), 'r')
        Database.__process(file)

    @staticmethod
    def seed():
        file = open(os.path.join(config.DATA_DIR, 'scripts/db-seed.sql'), 'r')
        Database.__process(file)

    @staticmethod
    def __process(file):
        sql_commands = file.read().split(';')
        file.close()

        for command in sql_commands:
            try:
                conn = db_connect.connect()
                conn.execute(command)
            except OperationalError as msg:
                print("Command skipped: ", msg)


if config.DB_DUMP:
    Database().dump()
if config.DB_CREATE:
    Database().create()
if config.DB_SEED:
    Database().seed()
