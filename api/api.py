from flask import Flask, jsonify
from flask_restplus import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app, version='1.0', title='Claims API',
          description='Enable consumer to interact with (read/write) claims in the database')

ns = api.namespace('claims', description='Claims operations')

claimList = [
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


class ClaimDAO(object):
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

    def get(self, id):
        for claim in self.claims:
            if claim['id'] == id:
                return todo
        api.abort(404, "Claim {} doesn't exist".format(id))

    def create(self, data):
        claim = data
        claim['id'] = self.counter = self.counter + 1
        self.claims.append(claim)
        return claim

    def update(self, id, data):
        claim = self.get(id)
        claim.update(data)
        return claim

    def delete(self, id):
        claim = self.get(id)
        self.claims.remove(claim)


@ns.route('', endpoint='claims')
class ClaimsApi(Resource):
    @ns.doc(params={
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
            # TODO: update to database SELECT query
            return jsonify(claimList)

        results = []

        # Case 2: only Policy Number is passed - return all claims for said Policy Number
        if policy_number is not None and category is None:
            # TODO: update to database SELECT query
            for claim in claimList:
                if policy_number == claim['policyNumber']: results.append(claim)

        # Case 3: only Category is passed - return all claims listed under said Category
        if policy_number is None and category is not None:
            # TODO: update to database SELECT query
            for claim in claimList:
                if claim['category'] == category:
                    results.append(claim)

        # Case 4: both parameters are passed - return all claims listed under said Category for said Policy Number
        if policy_number is not None and category is not None:
            # TODO: update to database SELECT query
            for claim in claimList:
                if policy_number == claim['policyNumber'] and category == claim['category']:
                    results.append(claim)

        return jsonify(results)

    @ns.doc(params={
        'policyNumber': {'description': 'The policy number', 'required': 'True'},
        'location': {'description': 'Address of the Loss', 'required': 'True'},
        'category': {'description': 'Category of the claim', 'required': 'True'},
        'description': {'description': 'Descrition of the claim', 'required': 'True'},
    })
    def post(self):
        """Insert claim into the database"""
        parser = reqparse.RequestParser()

        parser.add_argument('policyNumber', required=True, dest='policyNumber')
        parser.add_argument('location', required=True, dest='location')
        parser.add_argument('category', required=True, dest='category')
        parser.add_argument('description', required=True, dest='description')

        args = parser.parse_args()
        policyNumber = args['policyNumber']
        location = args['location']
        category = args['category']
        description = args['description']

        # TODO: insert into database
        claimList.append(
            {
                'policyNumber': policyNumber,
                'location': location,
                'category': category,
                'description': description,
            }
        )

        return


if __name__ == '__main__':
    app.run(debug=True)
