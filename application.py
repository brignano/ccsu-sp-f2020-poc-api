from flask import Flask
from apis import api
from flask_cors import CORS

application = Flask(__name__)
CORS(application)
api.init_app(application)

if __name__ == "__main__":
    application.run(debug=True)

