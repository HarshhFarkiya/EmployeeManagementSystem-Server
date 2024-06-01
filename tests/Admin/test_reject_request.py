import unittest
from unittest.mock import Mock, patch
from fastapi.responses import JSONResponse
import json
import sys
import os
# Add the parent directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from Controllers.Admin.RejectRequest import reject_request  # Replace 'Controllers.Admin.RejectRequest' with the actual module name

class TestRejectRequest(unittest.TestCase):

    def setUp(self):
        self.mock_connection = Mock()
        self.mock_cursor = Mock()
        self.mock_connection.cursor.return_value = self.mock_cursor

    @patch('Controllers.Admin.RejectRequest.connect')  # Replace 'Controllers.Admin.RejectRequest' with the actual module name
    @patch('Controllers.Admin.RejectRequest.disconnect')  # Replace 'Controllers.Admin.RejectRequest' with the actual module name
    def test_reject_request_success(self, mock_disconnect, mock_connect):
        project = {
            'manager_id': 'MGR1',
            'project_id': 'PRJ1',
            'resource_id': 'EMP1'
        }

        mock_connect.return_value = self.mock_connection
        self.mock_cursor.fetchall.side_effect = [
            [(1,)],  # Request exists
        ]

        response = reject_request(project)
        self.assertEqual(response.status_code, 200)
        response_content = json.loads(response.body)
        self.assertEqual(response_content['message'], 'Request Rejected')

    @patch('Controllers.Admin.RejectRequest.connect')
    @patch('Controllers.Admin.RejectRequest.disconnect')
    def test_reject_request_missing_parameters(self, mock_disconnect, mock_connect):
        project = {
            'manager_id': 'MGR1',
            'project_id': 'PRJ1'
        }

        mock_connect.return_value = self.mock_connection

        response = reject_request(project)
        self.assertEqual(response.status_code, 422)
        response_content = json.loads(response.body)
        self.assertEqual(response_content['message'], 'Missing Parameters')

    @patch('Controllers.Admin.RejectRequest.connect')
    @patch('Controllers.Admin.RejectRequest.disconnect')
    def test_reject_request_doesnt_exist(self, mock_disconnect, mock_connect):
        project = {
            'manager_id': 'MGR1',
            'project_id': 'PRJ1',
            'resource_id': 'EMP1'
        }

        mock_connect.return_value = self.mock_connection
        self.mock_cursor.fetchall.side_effect = [
            [],  # Request does not exist
        ]

        response = reject_request(project)
        self.assertEqual(response.status_code, 404)
        response_content = json.loads(response.body)
        self.assertEqual(response_content['message'], 'Request Doesnt Exists/Inactive')

    @patch('Controllers.Admin.RejectRequest.connect')
    @patch('Controllers.Admin.RejectRequest.disconnect')
    def test_reject_request_internal_error(self, mock_disconnect, mock_connect):
        project = {
            'manager_id': 'MGR1',
            'project_id': 'PRJ1',
            'resource_id': 'EMP1'
        }

        mock_connect.return_value = self.mock_connection
        self.mock_cursor.fetchall.side_effect = Exception("Some database error")

        with self.assertRaises(Exception) as context:
            reject_request(project)
        
        self.assertTrue('Internal Server Error' in str(context.exception))

if __name__ == '__main__':
    unittest.main()
