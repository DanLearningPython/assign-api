from flask import Flask
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)


class Home(Resource):
    def get(self):

        app_name = {'assign': 'api'}

        return app_name

api.add_resource(Home, '/')

if __name__ == '__main__':
    app.run(debug=True)