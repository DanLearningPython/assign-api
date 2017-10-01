from flask import Flask
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from config import *
from model import *

app = Flask(__name__)
connection_string = "mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}"\
            .format(db_user=mysql_user, db_password=mysql_password, db_host=mysql_host, db_name=mysql_database)
app.config['SQLALCHEMY_DATABASE_URI'] = connection_string
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
api = Api(app , catch_all_404s=True)


def require_api_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        print (args, kwargs)
        return f(*args, **kwargs)

    return decorated


class Home(Resource):

    @require_api_token
    def get(self):
        courses = Course.query.all()
        for course in courses:
            print(course.course_name)
        app_name = {'assign': 'api'}
        return app_name


api.add_resource(Home, '/')



if __name__ == '__main__':
    app.run(debug=True)