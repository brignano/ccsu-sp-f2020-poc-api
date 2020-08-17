from flask_restplus import Resource, Namespace, fields, reqparse

api = Namespace('claims', description='Claims related operations', path='/claims')
claim_model = api.model('Claim', {
    'id': fields.String(required=True, description="The claim identifier"),
    'policy_number': fields.String(required=True, description="The policy number making the claim"),
    'location': fields.String(required=True, description="The location of the loss"),
    'category': fields.String(required=True, description="The claim category"),
    'description': fields.String(required=True, description="The claim description"),
})


class ClaimDao(object):
    def __init__(self):
        self.counter = 0
        self.claims = [
            {
                "id": 0,
                "policy_number": "123456",
                "location": "10 Main Street, Farmington, CT, 06032",
                "category": "Property Damage",
                "description": "Car accident",
            },
            {
                "id": 1,
                "policy_number": "123456",
                "location": "10 Main Street, Farmington, CT, 06032",
                "category": "Bodily Injury",
                "description": "Car accident",
            },
            {
                "id": 2,
                "policy_number": "987654",
                "location": "10 Main Street, Farmington, CT, 06032",
                "category": "Property Damage",
                "description": "Car accident",
            }
        ]

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
        claim = data
        claim['id'] = self.counter = self.counter + 1
        self.claims.append(claim)
        return claim


@api.route('/all')
class ClaimList(Resource):
    @api.doc('list_claims')
    @api.marshal_list_with(claim_model, mask='')
    def get(self):
        """List all claims"""
        return ClaimDao().claims


@api.route('/')
@api.param('policy_number', 'The claim policy number')
@api.param('category', 'The claim category')
@api.response(404, 'Claim not found')
class Claim(Resource):
    @api.doc('get_claim')
    @api.marshal_with(claim_model, mask='')
    def get(self):
        """Get claim(s) from the database"""
        policy_number = reqparse.request.args.get('policy_number')
        category = reqparse.request.args.get('category')

        dao = ClaimDao()
        return dao.get(policy_number=policy_number, category=category)
