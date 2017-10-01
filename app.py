from flask import Flask, request
from flask_restful import Resource, Api, reqparse, abort
from functools import wraps
from models import *
from helpers import *
import json
import datetime


app = Flask(__name__)

api = Api(app, catch_all_404s=True)


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


class AssignmentCreateApi(Resource):

    @require_api_token
    def post(self):

        assignment_session = session()
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help='Assignment name cannot be blank')
        parser.add_argument('description', type=str, required=True, help='Assignment description cannot be blank')
        parser.add_argument('course_id', type=int, required=True, help='Course id cannot be blank')
        parser.add_argument('due_date', type=valid_date, required=True)

        args = parser.parse_args()
        print(args)

        assignment = Assignment()
        assignment.name = args.name
        assignment.description = args.description
        assignment.course_id = args.course_id
        assignment.due_date = args.due_date

        assignment_session.add(assignment)
        assignment_session.commit()
        assignment_id = assignment.id

        assignment_session.close()
        assignment_ref = {'assignment_id': assignment_id}

        return assignment_ref


class AssignmentApi(Resource):

    @require_api_token
    def get(self, assignment_id):

        assignment_session = session()
        assignment = assignment_session.query(Assignment).get(assignment_id)

        if assignment is None:
            abort(404, error="assignment {} not found".format(assignment_id))

        assignment_json = assignment_to_json(assignment)

        return assignment_json





api.add_resource(Home, '/')
api.add_resource(CourseApi, '/courses')
api.add_resource(AssignmentCreateApi, '/assignment')
api.add_resource(AssignmentApi, '/assignment/<assignment_id>')


if __name__ == '__main__':
    app.run(debug=True)