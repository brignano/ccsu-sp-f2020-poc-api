from flask import Flask
from flask_restplus import Api
from .claims import api as claims_api
from .geocode import api as geocode_api


api = Api(version='1.0', title='Claims API',
          description='Enable consumer to interact with (read/write) claims in the database')

api.add_namespace(claims_api, path='/claims')
api.add_namespace(geocode_api, path='/geocode')