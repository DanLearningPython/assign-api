from flask import Flask
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import *

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)


class Home(Resource):
    def get(self):

        app_name = {'assign': 'api'}

        return app_name

api.add_resource(Home, '/')

if __name__ == '__main__':
    app.run(debug=True)