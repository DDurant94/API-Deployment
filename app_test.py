import unittest
import json
from unittest.mock import patch, MagicMock
from faker import Faker
from app import app, Sum

def mock_sum_data():
    mock_return_data = MagicMock(spec=Sum)
    mock_return_data.id = 1
    mock_return_data.num1 = 40
    mock_return_data.num2 = 10
    mock_return_data.result = mock_return_data.num1 + mock_return_data.num2
    return mock_return_data

class TestSumEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    def test_sum_endpoint(self):
        input = mock_sum_data()  
        data = {
            'num1': input.num1,
            'num2': input.num2
        }
        
        response = self.app.post('/sum', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['result'], input.result)

if __name__ == '__main__':
    unittest.main()