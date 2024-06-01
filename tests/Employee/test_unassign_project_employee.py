import unittest
from unittest.mock import Mock, patch
from fastapi.responses import JSONResponse
import sys
import os
import json
# Add the parent directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..')))
from Controllers.Employee.UnassignProject import unassign_project_employee

class TestUnassignProjectEmployee(unittest.TestCase):

    def setUp(self):
        self.mock_connection = Mock()
        self.mock_cursor = Mock()
        self.mock_connection.cursor.return_value = self.mock_cursor

    @patch('Controllers.Employee.UnassignProject.connect')
    @patch('Controllers.Employee.UnassignProject.disconnect')
    def test_unassign_project_employee_success(self, mock_disconnect, mock_connect):
        employee = {'employee_id': 1}
        
        mock_connect.return_value = self.mock_connection
        self.mock_cursor.fetchall.side_effect = [
            [('1', 'project_id')],  # Employee details: assigned to project
             [(1,)],  # Project exists
        ]
        self.mock_cursor.fetchone.side_effect = [
            ['[1,2,3]'],  # Existing employees in the project
        ]
        
        response = unassign_project_employee(employee)
        self.assertEqual(response.status_code, 200)
        response_content=json.loads(response.body)
        self.assertEqual(response_content['message'], 'Project Unssigned Successfully')

    @patch('Controllers.Employee.UnassignProject.connect')
    @patch('Controllers.Employee.UnassignProject.disconnect')
    def test_unassign_project_employee_missing_parameters(self, mock_disconnect, mock_connect):
        employee = {}

        mock_connect.return_value = self.mock_connection
        
        response = unassign_project_employee(employee)
        self.assertEqual(response.status_code, 422)
        response_content=json.loads(response.body)
        self.assertEqual(response_content['message'], 'Missing Parameters')

    @patch('Controllers.Employee.UnassignProject.connect')
    @patch('Controllers.Employee.UnassignProject.disconnect')
    def test_unassign_project_employee_not_exists(self, mock_disconnect, mock_connect):
        employee = {'employee_id': 1}
        
        mock_connect.return_value = self.mock_connection
        self.mock_cursor.fetchall.side_effect = [
            [],  # Employee does not exist
        ]

        response = unassign_project_employee(employee)
        self.assertEqual(response.status_code, 404)
        response_content=json.loads(response.body)
        self.assertEqual(response_content['message'], "Employee Doesn't Exists, Please Provide a Valid Employee Id")

    @patch('Controllers.Employee.UnassignProject.connect')
    @patch('Controllers.Employee.UnassignProject.disconnect')
    def test_unassign_project_employee_already_unassigned(self, mock_disconnect, mock_connect):
        employee = {'employee_id': 1}
        
        mock_connect.return_value = self.mock_connection
        self.mock_cursor.fetchall.side_effect = [
            [(0, 'project_id')],  # Employee details: assigned to project
             [(1,)],  # Project exists
        ]
        self.mock_cursor.fetchone.side_effect = [
            ['[1,2,3]'],  # Existing employees in the project
        ]

        response = unassign_project_employee(employee)
        self.assertEqual(response.status_code, 409)
        response_content=json.loads(response.body)
        self.assertEqual(response_content['message'], "Employee is Already Unassigned")

    @patch('Controllers.Employee.UnassignProject.connect')
    @patch('Controllers.Employee.UnassignProject.disconnect')
    def test_unassign_project_employee_project_not_exists(self, mock_disconnect, mock_connect):
        employee = {'employee_id': 1}
        
        mock_connect.return_value = self.mock_connection
        self.mock_cursor.fetchall.side_effect = [
            [('1', 'project_id')],  # Employee details: assigned to project
             [],  # Project exists
        ]
        self.mock_cursor.fetchone.side_effect = [
            ['[1,2,3]'],  # Existing employees in the project
        ]

        response = unassign_project_employee(employee)
        self.assertEqual(response.status_code, 404)
        response_content=json.loads(response.body)
        self.assertEqual(response_content['message'], "Project Doesn't Exists, Please Provide a Valid Active Project Id")

if __name__ == '__main__':
    unittest.main()
