import unittest
import json
from unittest.mock import patch
from faker import Faker
from app import app, db, Sum

class TestSumEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.faker = Faker()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    @patch('app.Sum.query.filter_by')
    def test_get_sums_by_invalid_result(self, mock_filter_by):
        mock_filter_by.return_value.first.return_value = None
        response = self.app.get('/sum/result/invalid')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"error": "Invalid result value"})

    def test_sum_endpoint(self):
        num1 = self.faker.random_int(min=1, max=100)
        num2 = self.faker.random_int(min=1, max=100)
        data = {
            'num1': num1,
            'num2': num2
        }
        response = self.app.post('/sum', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['result'], num1 + num2)
        
        with app.app_context():
            sum_entry = Sum.query.filter_by(num1=num1, num2=num2).first()
            self.assertIsNotNone(sum_entry)
            self.assertEqual(sum_entry.result, num1 + num2)

if __name__ == '__main__':
    unittest.main()