from app import app
import json
import unittest


class HomeTestCase(unittest.TestCase):

    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='application/json')
        data = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)

        self.assertEqual(data, {'assign': 'api'})


if __name__ == '__main__':
    unittest.main()
