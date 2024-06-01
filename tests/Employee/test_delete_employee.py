import unittest
from unittest.mock import Mock, patch
from fastapi.responses import JSONResponse
import json
import sys
import os
# Add the parent directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..')))
from Controllers.Employee.DeleteEmployee import delete_employee

class TestDeleteEmployee(unittest.TestCase):

    def setUp(self):
        self.mock_connection = Mock()
        self.mock_cursor = Mock()
        self.mock_connection.cursor.return_value = self.mock_cursor

    @patch('Controllers.Employee.DeleteEmployee.connect')
    @patch('Controllers.Employee.DeleteEmployee.disconnect')
    def test_delete_employee_success(self, mock_disconnect, mock_connect):
        employee_id = 'EMP1'

        mock_connect.return_value = self.mock_connection
        self.mock_cursor.fetchall.side_effect = [
            [('EMP1', 'John Doe', 'john@example.com', 'Python, SQL', '1234567890', 0)],  # Employee exists and not assigned to a project
        ]

        response = delete_employee(employee_id)
        self.assertEqual(response.status_code, 200)
        response_content=json.loads(response.body)
        
        self.assertEqual(response_content['message'], 'Employee Deleted Successfully')

    @patch('Controllers.Employee.DeleteEmployee.connect')
    @patch('Controllers.Employee.DeleteEmployee.disconnect')
    def test_delete_employee_not_exists(self, mock_disconnect, mock_connect):
        employee_id = 1

        mock_connect.return_value = self.mock_connection
        self.mock_cursor.fetchall.side_effect = [
            [],  # Employee does not exist
        ]

        response = delete_employee(employee_id)
        self.assertEqual(response.status_code, 404)
        response_content=json.loads(response.body)
        self.assertEqual(response_content['message'], 'Employee Doesnt Exists')

    @patch('Controllers.Employee.DeleteEmployee.connect')
    @patch('Controllers.Employee.DeleteEmployee.disconnect')
    def test_delete_employee_assigned_to_project(self, mock_disconnect, mock_connect):
        employee_id = 1

        mock_connect.return_value = self.mock_connection
        self.mock_cursor.fetchall.side_effect = [
            [(1, 'John Doe', 'john@example.com', 'Python, SQL', '1234567890', 1)],  # Employee exists and is assigned to a project
        ]

        response = delete_employee(employee_id)
        self.assertEqual(response.status_code, 200)
        response_content=json.loads(response.body)
        self.assertEqual(response_content['message'], 'Employee already assigned to a project, Unassign before delete the user')

if __name__ == '__main__':
    unittest.main()
