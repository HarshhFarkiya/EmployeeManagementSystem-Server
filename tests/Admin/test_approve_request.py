import unittest
from unittest.mock import Mock, patch
from fastapi.responses import JSONResponse
import json
import sys
import os
# Add the parent directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from Controllers.Admin.ApproveRequest import approve_request  # Replace 'Controllers.Admin.ApproveRequest' with the actual module name

class TestApproveRequest(unittest.TestCase):

    def setUp(self):
        self.mock_connection = Mock()
        self.mock_cursor = Mock()
        self.mock_connection.cursor.return_value = self.mock_cursor

    @patch('Controllers.Admin.ApproveRequest.connect')  # Replace 'Controllers.Admin.ApproveRequest' with the actual module name
    @patch('Controllers.Admin.ApproveRequest.disconnect')  # Replace 'Controllers.Admin.ApproveRequest' with the actual module name
    def test_approve_request_success(self, mock_disconnect, mock_connect):
        project = {
            'manager_id': '1',
            'project_id': 'PRJ1',
            'resource_id': 'EMP1'
        }

        mock_connect.return_value = self.mock_connection
        self.mock_cursor.fetchall.side_effect = [
            [(1,)],  # Request exists
            [(1,)],  # Project exists
            [(0,)],  # Employee exists
            [('[1]',)],      # Employee not assigned
            [(1,)],  # Manager exists for the project
        ]
        self.mock_cursor.fetchone.side_effect = [
            ('[]',),  # Previous employees list
        ]

        response = approve_request(project)
        self.assertEqual(response.status_code, 200)
        response_content = json.loads(response.body)
        self.assertEqual(response_content['message'], 'Request Approved')

    @patch('Controllers.Admin.ApproveRequest.connect')
    @patch('Controllers.Admin.ApproveRequest.disconnect')
    def test_approve_request_missing_parameters(self, mock_disconnect, mock_connect):
        project = {
            'manager_id': 'MGR1',
            'project_id': 'PRJ1'
        }

        mock_connect.return_value = self.mock_connection

        response = approve_request(project)
        self.assertEqual(response.status_code, 422)
        response_content = json.loads(response.body)
        self.assertEqual(response_content['message'], 'Missing Parameters')

    @patch('Controllers.Admin.ApproveRequest.connect')
    @patch('Controllers.Admin.ApproveRequest.disconnect')
    def test_approve_request_doesnt_exist(self, mock_disconnect, mock_connect):
        project = {
            'manager_id': 'MGR1',
            'project_id': 'PRJ1',
            'resource_id': 'EMP1'
        }

        mock_connect.return_value = self.mock_connection
        self.mock_cursor.fetchall.side_effect = [
            [],  # Request does not exist
        ]

        response = approve_request(project)
        self.assertEqual(response.status_code, 404)
        response_content = json.loads(response.body)
        self.assertEqual(response_content['message'], 'Request Doesnt Exists/Inactive')

    @patch('Controllers.Admin.ApproveRequest.connect')
    @patch('Controllers.Admin.ApproveRequest.disconnect')
    def test_approve_request_project_not_found(self, mock_disconnect, mock_connect):
        project = {
            'manager_id': 'MGR1',
            'project_id': 'PRJ1',
            'resource_id': 'EMP1'
        }

        mock_connect.return_value = self.mock_connection
        self.mock_cursor.fetchall.side_effect = [
            [(1,)],  # Request exists
            [],      # Project does not exist
        ]

        response = approve_request(project)
        self.assertEqual(response.status_code, 404)
        response_content = json.loads(response.body)
        self.assertEqual(response_content['message'], 'Project Doesn\'t Exists, Please Provide a Valid Active Project Id')

    @patch('Controllers.Admin.ApproveRequest.connect')
    @patch('Controllers.Admin.ApproveRequest.disconnect')
    def test_approve_request_employee_not_found(self, mock_disconnect, mock_connect):
        project = {
            'manager_id': 'MGR1',
            'project_id': 'PRJ1',
            'resource_id': 'EMP1'
        }

        mock_connect.return_value = self.mock_connection
        self.mock_cursor.fetchall.side_effect = [
            [(1,)],  # Request exists
            [(1,)],  # Project exists
            [],      # Employee does not exist
        ]

        response = approve_request(project)
        self.assertEqual(response.status_code, 404)
        response_content = json.loads(response.body)
        self.assertEqual(response_content['message'], 'Employee Doesn\'t Exists, Please Provide a Valid Employee Id')

    @patch('Controllers.Admin.ApproveRequest.connect')
    @patch('Controllers.Admin.ApproveRequest.disconnect')
    def test_approve_request_employee_already_assigned(self, mock_disconnect, mock_connect):
        project = {
            'manager_id': 'MGR1',
            'project_id': 'PRJ1',
            'resource_id': 'EMP1'
        }

        mock_connect.return_value = self.mock_connection
        self.mock_cursor.fetchall.side_effect = [
            [(1,)],  # Request exists
            [(1,)],  # Project exists
            [(1,)],  # Employee exists
            [(1,)],  # Employee already assigned
        ]

        response = approve_request(project)
        self.assertEqual(response.status_code, 200)
        response_content = json.loads(response.body)
        self.assertEqual(response_content['message'], 'Employee Already Assgined')

    @patch('Controllers.Admin.ApproveRequest.connect')
    @patch('Controllers.Admin.ApproveRequest.disconnect')
    def test_approve_request_manager_not_found(self, mock_disconnect, mock_connect):
        project = {
            'manager_id': 'MGR1',
            'project_id': 'PRJ1',
            'resource_id': 'EMP1'
        }

        mock_connect.return_value = self.mock_connection
        self.mock_cursor.fetchall.side_effect = [
            [(1,)],  # Request exists
            [(1,)],  # Project exists
            [(0,)],  # Employee exists
            [],      # Employee not assigned
        ]

        response = approve_request(project)
        self.assertEqual(response.status_code, 404)
        response_content = json.loads(response.body)
        self.assertEqual(response_content['message'], 'Unable To Assigned Employee, Manager Doesn\'t Exists')

    @patch('Controllers.Admin.ApproveRequest.connect')
    @patch('Controllers.Admin.ApproveRequest.disconnect')
    def test_approve_request_internal_error(self, mock_disconnect, mock_connect):
        project = {
            'manager_id': 'MGR1',
            'project_id': 'PRJ1',
            'resource_id': 'EMP1'
        }

        mock_connect.return_value = self.mock_connection
        self.mock_cursor.fetchall.side_effect = Exception("Some database error")

        with self.assertRaises(Exception) as context:
            approve_request(project)
        
        self.assertTrue('Internal Server Error' in str(context.exception))

if __name__ == '__main__':
    unittest.main()
