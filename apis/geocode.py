import os
import requests
from flask import jsonify
from flask_restplus import Resource, reqparse, Namespace

api = Namespace('geocode', description='Geocode related operations', path='/geocode')
base_url = 'https://maps.googleapis.com/maps/api/geocode/json'


@api.route('/')
class GeocodeApi(Resource):
    @api.doc(params={
        'address': 'Address for geocoding',
    })
    def get(self):
        """Get latitude and longitude of address"""
        parser = reqparse.RequestParser()

        parser.add_argument('address', required=True, dest='address')

        args = parser.parse_args()
        address = args['address']
        api_key = os.environ.get('GOOGLE_API_KEY')
        params = {'address': address, 'key': api_key}

        if address is not None:
            r = requests.get(url=base_url, params=params)
            data = r.json()
            latitude = data['results'][0]['geometry']['location']['lat']
            longitude = data['results'][0]['geometry']['location']['lng']
            return jsonify(latitude=latitude, longitude=longitude)
