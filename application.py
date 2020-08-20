from flask import Flask
from apis import api

application = Flask(__name__)
api.init_app(application)

if __name__ == "__main__":
    application.run(debug=True)

