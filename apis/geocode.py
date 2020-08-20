import os
import requests
from flask import jsonify
from flask_restplus import Resource, reqparse, Namespace

api = Namespace('geocode', description='Geocode related operations', path='/geocode')
base_url = 'https://maps.googleapis.com/maps/api/geocode/json'


@api.route('/')
class GeocodeApi(Resource):
    @api.doc(params={
        'location': 'Location to be geocoded',
    })
    def get(self):
        """Get latitude and longitude of address"""
        location = reqparse.request.args.get('location')
        api_key = os.environ.get('GOOGLE_API_KEY')
        params = {'address': location, 'key': api_key}

        if location is not None:
            r = requests.get(url=base_url, params=params)
            data = r.json()
            latitude = data['results'][0]['geometry']['location']['lat']
            longitude = data['results'][0]['geometry']['location']['lng']
            return jsonify(latitude=latitude, longitude=longitude)
