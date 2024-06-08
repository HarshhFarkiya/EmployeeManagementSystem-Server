import unittest
from unittest.mock import Mock, patch
from fastapi.responses import JSONResponse
import sys
import os
# Add the parent directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..')))
from Controllers.Manager.RequestResources import request_resource
import json
class TestRequestResource(unittest.TestCase):

    def setUp(self):
        self.mock_connection = Mock()
        self.mock_cursor = Mock()
        self.mock_connection.cursor.return_value = self.mock_cursor

    @patch('Controllers.Manager.RequestResources.connect')
    @patch('Controllers.Manager.RequestResources.disconnect')
    def test_request_resource_success(self, mock_disconnect, mock_connect):
        request_data = {
            'manager_id': 1,
            'project_id': 'PRJ1',
            'resource_id': 'EMP1'
        }

        mock_connect.return_value = self.mock_connection
        self.mock_cursor.fetchall.side_effect = [
            [(request_data['manager_id'],)],  # Manager exists
            [(request_data['project_id'],)],  # Project exists
            [(request_data['resource_id'],)],  # Resource exists
            [],  # No existing requests
            [(None,)],  # Resource not assigned to the project
        ]
        self.mock_cursor.fetchone.side_effect = [
            ['[1]'],
            ('PRJ1')
        ]

        response = request_resource(request_data)
        self.assertEqual(response.status_code, 200)
        response_content=json.loads(response.body)
        self.assertEqual(response_content['message'], 'Resource Requested successfully')

    @patch('Controllers.Manager.RequestResources.connect')
    @patch('Controllers.Manager.RequestResources.disconnect')
    def test_request_resource_missing_parameters(self, mock_disconnect, mock_connect):
        request_data = {
            'manager_id': 'MNG1',
            'project_id': 'PRJ1'
        }

        response = request_resource(request_data)
        self.assertEqual(response.status_code, 422)
        response_content=json.loads(response.body)
        self.assertEqual(response_content['message'], 'Missing required parameters')

    @patch('Controllers.Manager.RequestResources.connect')
    @patch('Controllers.Manager.RequestResources.disconnect')
    def test_request_resource_invalid_manager(self, mock_disconnect, mock_connect):
        request_data = {
            'manager_id': 'MNG1',
            'project_id': 'PRJ1',
            'resource_id': 'EMP1'
        }

        mock_connect.return_value = self.mock_connection
        self.mock_cursor.fetchall.side_effect = [
            [],  # Manager does not exist
        ]

        response = request_resource(request_data)
        self.assertEqual(response.status_code, 404)
        response_content=json.loads(response.body)
        self.assertEqual(response_content['message'], 'Invalid manager id')

    @patch('Controllers.Manager.RequestResources.connect')
    @patch('Controllers.Manager.RequestResources.disconnect')
    def test_request_resource_invalid_project(self, mock_disconnect, mock_connect):
        request_data = {
            'manager_id': 'MNG1',
            'project_id': 'PRJ1',
            'resource_id': 'EMP1'
        }

        mock_connect.return_value = self.mock_connection
        self.mock_cursor.fetchall.side_effect = [
            [(request_data['manager_id'],)],  # Manager exists
            [],  # Project does not exist
        ]

        response = request_resource(request_data)
        self.assertEqual(response.status_code, 404)
        response_content=json.loads(response.body)
        self.assertEqual(response_content['message'], 'Invalid project id')

    @patch('Controllers.Manager.RequestResources.connect')
    @patch('Controllers.Manager.RequestResources.disconnect')
    def test_request_resource_invalid_resource(self, mock_disconnect, mock_connect):
        request_data = {
            'manager_id': 'MNG1',
            'project_id': 'PRJ1',
            'resource_id': 'EMP1'
        }

        mock_connect.return_value = self.mock_connection
        self.mock_cursor.fetchall.side_effect = [
            [(request_data['manager_id'],)],  # Manager exists
            [(request_data['project_id'],)],  # Project exists
            [],  # Resource does not exist
        ]

        response = request_resource(request_data)
        self.assertEqual(response.status_code, 404)
        response_content=json.loads(response.body)
        self.assertEqual(response_content['message'], 'Invalid resource id')

    @patch('Controllers.Manager.RequestResources.connect')
    @patch('Controllers.Manager.RequestResources.disconnect')
    def test_request_resource_unauthorized_assignment(self, mock_disconnect, mock_connect):
        request_data = {
            'manager_id': 'MNG1',
            'project_id': 'PRJ1',
            'resource_id': 'EMP1'
        }

        mock_connect.return_value = self.mock_connection
        self.mock_cursor.fetchall.side_effect = [
            [(request_data['manager_id'],)],  # Manager exists
            [(request_data['project_id'],)],  # Project exists
            [(request_data['resource_id'],)],  # Resource exists
            ['[]'],  # Manager is not assigned to the project
        ]
        self.mock_cursor.fetchone.side_effect = [
            ['[]'],  # Manager is not assigned to the project
        ]

        response = request_resource(request_data)
        self.assertEqual(response.status_code, 403)
        response_content=json.loads(response.body)
        self.assertEqual(response_content['message'], 'Unauthorized Assignment(Project not assinged)')

    @patch('Controllers.Manager.RequestResources.connect')
    @patch('Controllers.Manager.RequestResources.disconnect')
    def test_request_resource_request_exists(self, mock_disconnect, mock_connect):
        request_data = {
            'manager_id': 1,
            'project_id': 'PRJ1',
            'resource_id': 'EMP1'
        }

        mock_connect.return_value = self.mock_connection
        self.mock_cursor.fetchall.side_effect = [
            [(request_data['manager_id'],)],  # Manager exists
            [(request_data['project_id'],)],  # Project exists
            [(request_data['resource_id'],)],  # Resource exists
            [[(0)]],  # Manager is assigned to the project
            [(0,)],  # Existing request with status 0
        ]
        self.mock_cursor.fetchone.side_effect = [
            ['[1]'],  # Manager is not assigned to the project
        ]
        response = request_resource(request_data)
        self.assertEqual(response.status_code, 200)
        response_content=json.loads(response.body)
        self.assertEqual(response_content['message'], 'Request Exists')

    @patch('Controllers.Manager.RequestResources.connect')
    @patch('Controllers.Manager.RequestResources.disconnect')
    def test_request_resource_resource_already_present(self, mock_disconnect, mock_connect):
        request_data = {
            'manager_id': 1,
            'project_id': 'PRJ1',
            'resource_id': 'EMP1'
        }

        mock_connect.return_value = self.mock_connection
        self.mock_cursor.fetchall.side_effect = [
            [(request_data['manager_id'],)],  # Manager exists
            [(request_data['project_id'],)],  # Project exists
            [(request_data['project_id'],)],  # Resource exists
            [],  # existing requests
            [(request_data['project_id'],)],  # Resource already assigned to the project
        ]
        self.mock_cursor.fetchone.side_effect = [
            ['[1]'],
            ['PRJ1']
        ]

        response = request_resource(request_data)
        self.assertEqual(response.status_code, 200)
        response_content=json.loads(response.body)
        self.assertEqual(response_content['message'], 'Resource Already Present')

    @patch('Controllers.Manager.RequestResources.connect')
    @patch('Controllers.Manager.RequestResources.disconnect')
    def test_request_resource_internal_error(self, mock_disconnect, mock_connect):
        request_data = {
            'manager_id': 'MNG1',
            'project_id': 'PRJ1',
            'resource_id': 'EMP1'
        }

        mock_connect.return_value = self.mock_connection
        self.mock_cursor.fetchall.side_effect = Exception("Some database error")

        response = None
        try:
            response = request_resource(request_data)
        except Exception as e:
            self.assertEqual(str(e), "('Internal Server Error', Exception('Some database error'))")

if __name__ == '__main__':
    unittest.main()
