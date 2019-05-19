import threading

from flask import Flask, request
from flask_cors import CORS
from flask_jsonpify import jsonify
from flask_restful import Api

import data.db as db
from model.camera import Camera
from model.wagon import Wagon


class Api(threading.Thread):
    app = Flask(__name__)
    app_api = Api(app)
    CORS(app)

    def __init__(self, host, port):
        self.host = host
        self.port = port
        threading.Thread.__init__(self)

    def run(self):
        self.app.run(host=self.host, port=self.port)

    @staticmethod
    @app.route('/wagon')
    @app.route('/wagon/')
    def wagon_get_all():
        return jsonify([w.serialize() for w in db.WagonDB.get_all()])

    @staticmethod
    @app.route('/wagon/<wagon_id>')
    @app.route('/wagon/<wagon_id>/')
    def wagon_get_by_id(wagon_id):
        return jsonify([w.serialize() for w in db.WagonDB.get_by_id(wagon_id)])

    @staticmethod
    @app.route('/wagon/camera/<camera_id>')
    @app.route('/wagon/camera/<camera_id>/')
    def wagon_get_by_camera(camera_id):
        return jsonify([w.serialize() for w in db.WagonDB.get_by_camera(camera_id)])

    @staticmethod
    @app.route('/wagon/<wagon_id>/pin/long/<long>/lat/<lat>')
    @app.route('/wagon/<wagon_id>/pin/long/<long>/lat/<lat>/')
    @app.route('/wagon/<wagon_id>/pin/lat/<lat>/long/<long>')
    @app.route('/wagon/<wagon_id>/pin/lat/<lat>/long/<long>/')
    def wagon_pin(wagon_id, long, lat):
        w = Wagon(wagon_id, longitude=long, latitude=lat)
        if db.WagonDB.update_or_add_wagon_coordinates(w):
            return jsonify({'message': 'success'})
        else:
            return jsonify({'message': 'failed to pin wagon'})

    @staticmethod
    @app.route('/wagon/new/<wagon_id>')
    @app.route('/wagon/new/<wagon_id>/')
    def wagon_add(wagon_id):
        w = Wagon(wagon_id)
        if db.WagonDB.add_wagon(w):
            return jsonify({'message': 'success'})
        else:
            return jsonify({'message': 'failed to add wagon'})

    @staticmethod
    @app.route('/wagon/delete/<wagon_id>')
    @app.route('/wagon/delete/<wagon_id>/')
    def wagon_delete(wagon_id):
        w = Wagon(wagon_id)
        if db.WagonDB.delete_wagon(w):
            return jsonify({'message': 'success'})
        else:
            return jsonify({'message': 'failed to delete wagon'})

    @staticmethod
    @app.route('/camera')
    @app.route('/camera/')
    def camera_get_all():
        return jsonify([c.serialize() for c in db.CameraDB.get_all()])

    @staticmethod
    @app.route('/camera/with/wagons')
    @app.route('/camera/with/wagons')
    def camera_get_with_wagons():
        return_list = []
        for cww in db.CameraDB.get_with_wagons():
            return_list.append(cww.serialize())
        return jsonify(return_list)

    @staticmethod
    @app.route('/camera/<camera_id>')
    @app.route('/camera/<camera_id>/')
    def camera_get_by_id(camera_id):
        return jsonify([c.serialize() for c in db.CameraDB.get_by_id(camera_id)])

    @staticmethod
    @app.route('/camera/<camera_id>/description/<description>')
    @app.route('/camera/<camera_id>/description/<description>/')
    def camera_save_description(camera_id, description):
        c = Camera(camera_id, description)
        if db.CameraDB.save_description(c):
            return jsonify({'message': 'success'})
        else:
            return jsonify({'message': 'failed to save description'})

    @staticmethod
    @app.route('/history')
    @app.route('/history/')
    def history_get_all():
        return jsonify([h.serialize() for h in db.HistoryDB.get_all()])

    @staticmethod
    @app.route('/history/recent')
    @app.route('/history/recent/')
    def history_get_recent():
        return jsonify([h.serialize() for h in db.HistoryDB.get_recent()])

    @staticmethod
    @app.route('/history/wagon/<wagon_id>')
    @app.route('/history/wagon/<wagon_id>/')
    def history_get_by_wagon_id(wagon_id):
        return jsonify([h.serialize() for h in db.HistoryDB.get_by_wagon_id(wagon_id)])

    @staticmethod
    @app.route('/history/camera/<camera_id>')
    @app.route('/history/camera/<camera_id>/')
    def history_get_by_camera_id(camera_id):
        return jsonify([h.serialize() for h in db.HistoryDB.get_by_camera_id(camera_id)])

    @staticmethod
    @app.route('/register/wagon/<wagon_id>/camera/<camera_id>')
    @app.route('/register/wagon/<wagon_id>/camera/<camera_id>/')
    def register_wagon_at_camera(wagon_id, camera_id):
        if db.RegisterDB.register(wagon_id, camera_id):
            return jsonify({'message': 'success'})
        else:
            return jsonify({'message': 'failed to register wagon'})

    ''' DATABASE MANAGEMENT'''

    @staticmethod
    @app.route('/db/<action>')
    @app.route('/db/<action>/')
    def manage_database(action):
        if action == "dump":
            db.Database().dump()
        elif action == "create":
            db.Database().create()
        elif action == "seed":
            db.Database().seed()
        else:
            return jsonify({'message': 'incorrect action (dump, create, seed)'})
        return jsonify({'message': 'success'})

    @staticmethod
    @app.route('/shutdown')
    @app.route('/shutdown/')
    def shutdown():
        Api.shutdown_server()
        return jsonify({'message': 'server shutting down'})

    @staticmethod
    def shutdown_server():
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not using werkzeug')
        func()
