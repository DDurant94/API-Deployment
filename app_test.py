import unittest
import json
from unittest.mock import patch, MagicMock
from faker import Faker
from app import app, Sum

class TestSumEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.faker = Faker()

    @patch('app.db.session.add')
    @patch('app.db.session.commit')
    @patch('app.Sum.query.filter_by')
    def test_get_sums_by_invalid_result(self, mock_filter_by, mock_commit, mock_add):
        mock_filter_by.return_value.first.return_value = None
        response = self.app.get('/sum/result/invalid')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"error": "Invalid result value"})

    @patch('app.db.session.add')
    @patch('app.db.session.commit')
    @patch('app.Sum.query.filter_by')
    def test_sum_endpoint(self, mock_filter_by, mock_commit, mock_add):
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
        
        mock_sum = MagicMock()
        mock_sum.result = num1 + num2
        mock_filter_by.return_value.first.return_value = mock_sum

        sum_entry = Sum.query.filter_by(num1=num1, num2=num2).first()
        self.assertIsNotNone(sum_entry)
        self.assertEqual(sum_entry.result, num1 + num2)

    @patch('app.db.session.execute')
    def test_find_all(self, mock_execute):
        mock_sum = MagicMock()
        mock_sum.num1 = self.faker.random_int(min=1, max=100)
        mock_sum.num2 = self.faker.random_int(min=1, max=100)
        mock_sum.result = mock_sum.num1 + mock_sum.num2
        mock_execute.return_value.scalars.return_value = [mock_sum]

        response = self.app.get('/sum')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertEqual(len(response_data), 1)
        self.assertEqual(response_data[0]['result'], mock_sum.result)

    @patch('app.db.session.execute')
    def test_get_sums_by_result(self, mock_execute):
        result = self.faker.random_int(min=1, max=200)
        mock_sum = MagicMock()
        mock_sum.result = result
        mock_execute.return_value.scalars.return_value = [mock_sum]

        response = self.app.get(f'/sum/result/{result}')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertEqual(len(response_data), 1)
        self.assertEqual(response_data[0]['result'], result)

if __name__ == '__main__':
    unittest.main()