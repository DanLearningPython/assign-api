from app import app
import unittest
import json
from helpers import courses_to_json

from models import *


class GeneralTestCases(unittest.TestCase):

    def test_index(self):

        tester = app.test_client(self)
        response = tester.get('/', content_type='application/json')
        data = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, {'assign': 'api'})

    def test_404(self):

        tester = app.test_client(self)
        response = tester.get('/thisbetternotexistorsomethingisreallyreallywrong', content_type='application/json')

        self.assertEqual(response.status_code, 404)


class CourseTestCase(unittest.TestCase):

    engine = create_engine(connection_string)
    Session = sessionmaker(bind=engine)
    session = Session()
    client = app.test_client()

    def setUp(self):

        semester = Semester()
        semester.season = 'Fall'
        semester.year = 2017
        self.session.add(semester)
        self.session.commit()
        self.semester = semester

        course = Course()
        course.course_name = "Test Course"
        course.semester_id = semester.id
        self.session.add(course)
        self.session.commit()
        self.course = course

    def test_index(self):

        courses = self.session.query(Course).all()
        courses_json = courses_to_json(courses)

        response = self.client.get('/courses', content_type='application/json')
        data = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)

        self.assertEqual(data, courses_json)

    def tearDown(self):

        # ensure there are no pending transactions
        self.session.commit()
        self.session.delete(self.course)
        self.session.commit()
        self.session.delete(self.semester)
        self.session.commit()


class AssignmentTestCase(unittest.TestCase):

    engine = create_engine(connection_string)
    Session = sessionmaker(bind=engine)
    session = Session()
    client = app.test_client()

    def setUp(self):

        semester = Semester()
        semester.season = 'Fall'
        semester.year = 2017
        self.session.add(semester)
        self.session.commit()
        self.semester = semester

        course = Course()
        course.course_name = "Test Course"
        course.semester_id = semester.id
        self.session.add(course)
        self.session.commit()
        self.course = course

    def test_post(self):

        test_assignment = {
            "name" : "test_assignment_name",
            "description" : "description for test assignment",
            "course_id" : self.course.id,
            "due_date" : "2017-10-11 10:10:10"
        }
        headers = {'Content-type': 'application/json'}

        post_resp = self.client.post('/assignment', data=json.dumps(test_assignment, default=str), headers=headers)
        post_data = json.loads(post_resp.get_data())

        self.assertGreaterEqual(post_data['assignment_id'], 0)
        self.assignment_id = post_data['assignment_id']

        get_resp = self.client.get('/assignment/{id}'.format(id=str(self.assignment_id)), content_type='application/json')
        get_data = json.loads(get_resp.get_data())

        self.assertEqual(get_resp.status_code, 200)
        self.assertEqual(test_assignment['name'], get_data['name'])

    def tearDown(self):

        # ensure there are no pending transactions
        # TODO look into session leakage
        self.session.commit()

        if self.assignment_id > 0:
            test_assignment = self.session.query(Assignment).get(self.assignment_id)
            self.session.delete(test_assignment)
            self.session.commit()

        self.session.delete(self.course)
        self.session.commit()
        self.session.delete(self.semester)
        self.session.commit()


if __name__ == '__main__':
    unittest.main()
