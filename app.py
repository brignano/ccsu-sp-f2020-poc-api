from flask import Flask
from apis import api
from flask_cors import CORS

app = Flask(__name__)
api.init_app(app)
CORS(app)
app.run(debug=True)

