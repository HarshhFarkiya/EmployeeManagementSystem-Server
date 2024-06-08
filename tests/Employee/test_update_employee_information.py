import unittest
from unittest.mock import Mock, patch
from fastapi.responses import JSONResponse
import json
import sys
import os
# Add the parent directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..')))
# Assuming the update_employee_information function is in a module named 'employee'
from Controllers.Employee.UpdateEmployee import update_employee_information

class TestUpdateEmployeeInformation(unittest.TestCase):

    def setUp(self):
        self.mock_connection = Mock()
        self.mock_cursor = Mock()
        self.mock_connection.cursor.return_value = self.mock_cursor

    @patch('Controllers.Employee.UpdateEmployee.connect')
    @patch('Controllers.Employee.UpdateEmployee.disconnect')
    def test_update_employee_information_success(self, mock_disconnect, mock_connect):
        employee = {
            'employee_id': 1,
            'name': 'John Doe',
            'email': 'john@example.com',
            'phone': '1234567890',
            'skills': 'Python, SQL',
            'experience_years': 5
        }

        mock_connect.return_value = self.mock_connection
        self.mock_cursor.fetchall.return_value = [(1,)]

        response = update_employee_information(employee)
        self.assertEqual(response.status_code, 200)
        response_content = json.loads(response.body)
        self.assertEqual(response_content['message'], 'Profile Updated successfully')

    @patch('Controllers.Employee.UpdateEmployee.connect')
    @patch('Controllers.Employee.UpdateEmployee.disconnect')
    def test_update_employee_information_missing_parameters(self, mock_disconnect, mock_connect):
        employee = {
            'employee_id': 'EMP1',
            'name': 'John Doe',
            'email': 'john@example.com',
            'phone': '1234567890',
            'skills': 'Python, SQL',
        }

        mock_connect.return_value = self.mock_connection

        response = update_employee_information(employee)
        self.assertEqual(response.status_code, 422)
        response_content = json.loads(response.body)
        self.assertEqual(response_content['message'], 'Missing required parameters')

    @patch('Controllers.Employee.UpdateEmployee.connect')
    @patch('Controllers.Employee.UpdateEmployee.disconnect')
    def test_update_employee_information_employee_not_exists(self, mock_disconnect, mock_connect):
        employee = {
            'employee_id': 1,
            'name': 'John Doe',
            'email': 'john@example.com',
            'phone': '1234567890',
            'skills': 'Python, SQL',
            'experience_years': 5
        }

        mock_connect.return_value = self.mock_connection
        self.mock_cursor.fetchall.return_value = []

        response = update_employee_information(employee)
        self.assertEqual(response.status_code, 404)  # This should be a different status code
        response_content=json.loads(response.body)
        self.assertEqual(response_content['message'], 'Employee Id doesnt exists')

    @patch('Controllers.Employee.UpdateEmployee.connect')
    @patch('Controllers.Employee.UpdateEmployee.disconnect')
    def test_update_employee_information_internal_server_error(self, mock_disconnect, mock_connect):
        employee = {
            'employee_id': 1,
            'name': 'John Doe',
            'email': 'john@example.com',
            'phone': '1234567890',
            'skills': 'Python, SQL',
            'experience_years': 5
        }

        mock_connect.return_value = self.mock_connection
        self.mock_cursor.fetchall.side_effect = Exception('Database error')

        with self.assertRaises(Exception) as context:
            update_employee_information(employee)

        self.assertTrue('Internal Server Error' in str(context.exception))

if __name__ == '__main__':
    unittest.main()
