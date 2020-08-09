from flask import Flask, jsonify
from flask_restplus import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

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

@api.route('/claims', endpoint='claims')
class ClaimsApi(Resource):    
    @api.doc(params={
        'policyNumber': 'Policy number',
        'category': 'Claim category'
    })
    def get(self):
        """Get claim(s) from database"""
        parser = reqparse.RequestParser()
        
        parser.add_argument('policyNumber', required=False, dest='policyNumber')
        parser.add_argument('category', required=False, dest='category')

        args = parser.parse_args()
        policyNumber = args['policyNumber']
        category = args['category']

        # Case 1: both parameters are None - return all claims
        if(policyNumber is None and category is None):
            # TODO: update to database SELECT query
            return jsonify(claimList)

        results = []

        # Case 2: only Policy Number is passed - return all claims for said Policy Number
        if(policyNumber is not None and category is None):
            # TODO: update to database SELECT query
            for claim in claimList:
                if(policyNumber == claim['policyNumber']): results.append(claim)
        
        # Case 3: only Category is passed - return all claims listed under said Category
        if(policyNumber is None and category is not None): 
            # TODO: update to database SELECT query
            for claim in claimList:
                if(category == claim['category']): results.append(claim)

        # Case 4: both parameters are passed - return all claims listed under said Category for said Policy Number
        if(policyNumber is not None and category is not None): 
            # TODO: update to database SELECT query
            for claim in claimList:
                if(policyNumber == claim['policyNumber'] and category == claim['category']): results.append(claim)

        return jsonify(results)
        

    @api.doc(params={
        'policyNumber': {'description':'The policy number', 'required': 'True'},
        'location': {'description':'Address of the Loss', 'required': 'True'},
        'category': {'description':'Category of the claim', 'required': 'True'},
        'description': {'description':'Descrition of the claim', 'required': 'True'},
    })
    def post(self):
        """Insert claim into database"""
        parser = reqparse.RequestParser()
        
        parser.add_argument('policyNumber', required=True, dest='policyNumber')
        parser.add_argument('location', required=True, dest='location')
        parser.add_argument('category', required=True, dest='category')
        parser.add_argument('description', required=True, dest='description')

        args = parser.parse_args()
        policyNumber = args['policyNumber']
        location = args['location']
        category = args['category']
        category = args['description']

        # TODO: insert into database
            

api.add_resource(ClaimsApi, '/claims')

if __name__ == '__main__':
    app.run(debug=True)