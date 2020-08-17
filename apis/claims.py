from flask import jsonify
from flask_restplus import Resource, reqparse, Namespace

api = Namespace('claims', description='Claims related operations')


class Claim(object):
    id = ''
    policyNumber = ''
    location = ''
    category = ''
    description = ''


class ClaimDao(object):
    def __init__(self):
        self.counter = 0
        self.claims = [
            {
                "id": 0,
                "policyNumber": "123456",
                "location": "10 Main Street, Farmington, CT, 06032",
                "category": "Property Damage",
                "description": "Car accident",
            },
            {
                "id": 1,
                "policyNumber": "123456",
                "location": "10 Main Street, Farmington, CT, 06032",
                "category": "Bodily Injury",
                "description": "Car accident",
            },
            {
                "id": 2,
                "policyNumber": "987654",
                "location": "10 Main Street, Farmington, CT, 06032",
                "category": "Property Damage",
                "description": "Car accident",
            }
        ]

    def get(self, claim_id) -> Claim:
        for claim in self.claims:
            if claim['id'] == claim_id:
                return claim
        api.abort(404, "Claim {} doesn't exist".format(claim_id))

    def create(self, data):
        claim = data
        claim['id'] = self.counter = self.counter + 1
        self.claims.append(claim)
        return claim

    def update(self, policy_number, data):
        claim = self.get(policy_number)
        claim.update(data)
        return claim

    def delete(self, policy_number):
        claim = self.get(policy_number)
        self.claims.remove(claim)


@api.route('/')
class ClaimsApi(Resource):
    @api.doc(params={
        'policyNumber': 'Policy number',
        'category': 'Claim category'
    })
    def get(self):
        """Get claim(s) from the database"""
        parser = reqparse.RequestParser()

        parser.add_argument('policyNumber', required=False, dest='policyNumber')
        parser.add_argument('category', required=False, dest='category')

        args = parser.parse_args()
        policy_number = args['policyNumber']
        category = args['category']

        # Case 1: both parameters are None - return all claims
        if policy_number is None and category is None:
            return jsonify(ClaimDao())

        results = []

        # Case 2: only Policy Number is passed - return all claims for said Policy Number
        if policy_number is not None and category is None:
            dao = ClaimDao()
            return dao.get(claim_id=policy_number)

        return jsonify(results)

    @api.doc(params={
        'policyNumber': {'description': 'The policy number', 'required': 'True'},
        'location': {'description': 'Address of the Loss', 'required': 'True'},
        'category': {'description': 'Category of the claim', 'required': 'True'},
        'description': {'description': 'Description of the claim', 'required': 'True'},
    })
    def post(self):
        """Insert claim into the database"""
        parser = reqparse.RequestParser()

        parser.add_argument('policyNumber', required=True, dest='policyNumber')
        parser.add_argument('location', required=True, dest='location')
        parser.add_argument('category', required=True, dest='category')
        parser.add_argument('description', required=True, dest='description')

        args = parser.parse_args()
        policy_number = args['policyNumber']
        location = args['location']
        category = args['category']
        description = args['description']

        dao = ClaimDao()

        return dao.create(
            data={
                'policyNumber': policy_number,
                'location': location,
                'category': category,
                'description': description,
            }
        )