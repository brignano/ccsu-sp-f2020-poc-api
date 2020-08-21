import json
import os

from flask_restplus import Resource, Namespace, fields, reqparse

api = Namespace('claims', description='Claims related operations', path='/claims')
claim_model = api.model('Claim', {
    'policy_number': fields.String(required=True, description="The policy number making the claim"),
    'location': fields.String(required=True, description="The location of the loss"),
    'category': fields.String(required=True, description="The claim category"),
    'description': fields.String(required=True, description="The claim description"),
})
claim_dao_model = api.model('Claim Dao', {
    'id': fields.Integer(required=True, description="The claim identifier"),
    'policy_number': fields.String(required=True, description="The policy number making the claim"),
    'location': fields.String(required=True, description="The location of the loss"),
    'category': fields.String(required=True, description="The claim category"),
    'description': fields.String(required=True, description="The claim description"),
})

claims_json_path = 'data/claims.json'


def write_json(json_data):
    site_root = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(site_root, claims_json_path)
    with open(json_url, 'w') as file_out:
        json.dump(json_data, file_out)


def read_json():
    site_root = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(site_root, claims_json_path)
    with open(json_url) as file_in:
        return json.load(file_in)


class ClaimDao(object):
    def __init__(self):
        self.counter = 0
        self.claims = read_json()

    def get(self, policy_number=None, category=None):

        results = []

        for claim in self.claims:
            if policy_number is not None and category is not None:
                if claim['policy_number'] == policy_number and claim['category'] == category:
                    results.append(claim)
            elif policy_number is not None and claim['policy_number'] == policy_number:
                results.append(claim)
            elif category is not None and str.lower(claim['category']) == str.lower(category):
                results.append(claim)

        if len(results) == 0:
            api.abort(404, "No claims found")

        return results

    def create(self, data):
        claims_data = self.claims
        claims_data.sort(key=lambda x: x['id'])
        data['id'] = int(claims_data[(len(claims_data)-1)]['id']) + 1
        claims_data.append(data)
        write_json(claims_data)
        return data


@api.route('/all')
class ClaimList(Resource):
    @api.doc('list_claims')
    @api.marshal_list_with(claim_dao_model, mask='')
    def get(self):
        """List all claims"""
        return ClaimDao().claims


@api.route('/')
class Claim(Resource):
    @api.doc('get_claim')
    @api.param('policy_number', 'The policy number of the claim')
    @api.param('category', 'The category of the claim')
    @api.response(404, 'Claim not found')
    @api.marshal_with(claim_dao_model, mask='')
    def get(self):
        """Get claim(s) from the database"""
        policy_number = reqparse.request.args.get('policy_number')
        category = reqparse.request.args.get('category')

        dao = ClaimDao()
        return dao.get(policy_number=policy_number, category=category)

    @api.doc('add_claim')
    @api.expect(claim_model)
    @api.marshal_with(claim_model, mask='')
    def post(self):
        """Add claim to the database"""
        dao = ClaimDao()
        return dao.create(api.payload)
