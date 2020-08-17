from flask_restplus import Resource, reqparse, Namespace

api = Namespace('geocode', description='Geocode related operations')


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

        if address is not None:
            return

