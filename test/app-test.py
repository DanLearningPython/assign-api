from app import connection_string, app
import unittest
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from helpers import courses_to_json

from model import *


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
        data = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 404)




if __name__ == '__main__':
    unittest.main()
