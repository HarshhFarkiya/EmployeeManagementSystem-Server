import unittest
from unittest.mock import Mock, patch
from fastapi.responses import JSONResponse
import json
import sys
import os
# Add the parent directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..')))
# Assuming the assign_project_employee function is in a module named 'project'
from Controllers.Employee.AssignProject import assign_project_employee

class TestAssignProjectEmployee(unittest.TestCase):

    def setUp(self):
        self.mock_connection = Mock()
        self.mock_cursor = Mock()
        self.mock_connection.cursor.return_value = self.mock_cursor

    @patch('Controllers.Employee.AssignProject.connect')
    @patch('Controllers.Employee.AssignProject.disconnect')
    def test_assign_project_employee_success(self, mock_disconnect, mock_connect):
        project = {
            'employee_id': 'EMP1',
            'project_id': 'PRJ1'
        }

        mock_connect.return_value = self.mock_connection
        self.mock_cursor.fetchall.side_effect = [[(1,)],[('0',)],[('[]',)]]
        response = assign_project_employee(project)
        self.assertEqual(response.status_code, 200)
        response_content = json.loads(response.body)
        self.assertEqual(response_content['message'], 'Project Assigned Successfully')

    @patch('Controllers.Employee.AssignProject.connect')
    @patch('Controllers.Employee.AssignProject.disconnect')
    def test_assign_project_employee_missing_parameters(self, mock_disconnect, mock_connect):
        project = {
            'employee_id': 'EMP1'
        }

        mock_connect.return_value = self.mock_connection

        response = assign_project_employee(project)
        self.assertEqual(response.status_code, 422)
        response_content = json.loads(response.body)
        self.assertEqual(response_content['message'], 'Missing Parameters')

    @patch('Controllers.Employee.AssignProject.connect')
    @patch('Controllers.Employee.AssignProject.disconnect')
    def test_assign_project_employee_project_not_exists(self, mock_disconnect, mock_connect):
        project = {
            'employee_id': 'EMP1',
            'project_id': 'PRJ1'
        }

        mock_connect.return_value = self.mock_connection
        self.mock_cursor.fetchall.return_value = []

        response = assign_project_employee(project)
        self.assertEqual(response.status_code, 404)
        response_content = json.loads(response.body)
        self.assertEqual(response_content['message'], "Project Doesn't Exists, Please Provide a Valid Active Project Id")

    # Add similar test methods for other scenarios...

if __name__ == '__main__':
    unittest.main()
