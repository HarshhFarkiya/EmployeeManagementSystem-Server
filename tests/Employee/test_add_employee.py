import unittest
from unittest.mock import Mock, patch
from fastapi.responses import JSONResponse
import sys
import os
# Add the parent directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..')))
from Models.Employee.EmployeeModel import Employee
from Controllers.Employee.Employee import add_employee  
import json;
class TestAddEmployee(unittest.TestCase):

    def setUp(self):
        self.mock_connection = Mock()
        self.mock_cursor = Mock()
        self.mock_connection.cursor.return_value = self.mock_cursor

    @patch('Controllers.Employee.Employee.connect')
    @patch('Controllers.Employee.Employee.disconnect')
    @patch('Controllers.Employee.Employee.bcrypt.hashpw')
    def test_add_employee_success(self, mock_hashpw, mock_disconnect, mock_connect):
        employee = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'skills': 'Python, SQL',
            'phone': '1234567890',
            'experience_years': 5
        }

        mock_connect.return_value = self.mock_connection
        self.mock_cursor.fetchall.side_effect = [[(1,)], []]
        mock_hashpw.return_value = b'hashed_password'
        self.mock_connection.converter.escape.return_value = 'hashed_password'

        response = add_employee(employee)
        self.assertEqual(response.status_code, 200)
        response_content=json.loads(response.body)
        self.assertEqual(response_content['message'], 'User Added Successfully')

    @patch('Controllers.Employee.Employee.connect')
    @patch('Controllers.Employee.Employee.disconnect')
    def test_add_employee_missing_parameters(self, mock_disconnect, mock_connect):
        employee = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'skills': 'Python, SQL'
        }

        mock_connect.return_value = self.mock_connection

        response = add_employee(employee)
        self.assertEqual(response.status_code, 422)
        response_content = json.loads(response.body)
        self.assertEqual(response_content['message'], 'Missing Parameters')

    @patch('Controllers.Employee.Employee.connect')
    @patch('Controllers.Employee.Employee.disconnect')
    def test_add_employee_already_exists(self, mock_disconnect, mock_connect):
        employee = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'skills': 'Python, SQL',
            'phone': '1234567890',
            'experience_years': 5
        }

        mock_connect.return_value = self.mock_connection
        self.mock_cursor.fetchall.side_effect = [[(1,)], [(1,)]]

        response = add_employee(employee)
        print(response)
        self.assertEqual(response.status_code, 409)
        response_content = json.loads(response.body)
        self.assertEqual(response_content['message'], 'Employee already exists')

if __name__ == '__main__':
    unittest.main()
