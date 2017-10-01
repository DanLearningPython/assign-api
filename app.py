from flask import Flask
from flask_restful import Resource, Api
from functools import wraps
from models import *
from helpers import courses_to_json
import json

app = Flask(__name__)

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
        app_name = {'assign': 'api'}
        return app_name


class CourseApi(Resource):


    @require_api_token
    def get(self):
        course_session = session()

        courses = course_session.query(Course, Semester).join(Semester, Course.semester_id == Semester.id).all()
        #print (courses.statement)
        courses_json = courses_to_json(courses)
        course_session.close()

        return courses_json





api.add_resource(Home, '/')
api.add_resource(CourseApi, '/courses')


if __name__ == '__main__':
    app.run(debug=True)