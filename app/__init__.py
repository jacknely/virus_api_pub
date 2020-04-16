from flask import Flask
from flask_restful import Api
from flask_restful_swagger import swagger

from .virus import VirusMongo

mongo = VirusMongo()
api = swagger.docs(Api(), apiVersion="1", api_spec_url="/api/spec")


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    api.init_app(app)
    mongo.init_app(app)

    return app
