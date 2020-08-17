from flask import Flask
from flask_restplus import Api
from .claims import api as claims_api
from .geocode import api as geocode_api


app = Flask(__name__)
api = Api(app, version='1.0', title='Claims API',
          description='Enable consumer to interact with (read/write) claims in the database')

api.add_namespace(claims_api)
api.add_namespace(geocode_api)

