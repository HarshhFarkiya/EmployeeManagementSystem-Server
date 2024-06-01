import unittest
from unittest.mock import Mock, patch
from fastapi.responses import JSONResponse
import json
import sys
import os
# Add the parent directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..')))
from Controllers.Manager.UnassignProject import unassign_project_manager  # Replace with the actual import

class TestUnassignProjectManager(unittest.TestCase):

    def setUp(self):
        self.mock_connection = Mock()
        self.mock_cursor = Mock()
        self.mock_connection.cursor.return_value = self.mock_cursor

    @patch('Controllers.Manager.UnassignProject.connect')  # Replace with the actual module where `connect` is located
    @patch('Controllers.Manager.UnassignProject.disconnect')  # Replace with the actual module where `disconnect` is located
    def test_unassign_project_manager_success(self, mock_disconnect, mock_connect):
        manager = {'manager_id': '1', 'project_id': '101'}
        
        mock_connect.return_value = self.mock_connection
        self.mock_cursor.fetchall.side_effect = [
            [(1,)],  # Manager exists
            [(json.dumps(['101']),)],  # Project exists
        ]
        self.mock_cursor.fetchone.side_effect = [
           
            (json.dumps(['101']),)  # Projects assigned to manager
        ]

        response = unassign_project_manager(manager)
        self.assertEqual(response.status_code, 200)
        response_content = json.loads(response.body)
        self.assertEqual(response_content['message'], 'Manager is Unssigned from project successfully')

    @patch('Controllers.Manager.UnassignProject.connect')
    @patch('Controllers.Manager.UnassignProject.disconnect')
    def test_unassign_project_manager_missing_parameters(self, mock_disconnect, mock_connect):
        manager = {'manager_id': '1'}

        mock_connect.return_value = self.mock_connection
        
        response = unassign_project_manager(manager)
        self.assertEqual(response.status_code, 422)
        response_content = json.loads(response.body)
        self.assertEqual(response_content['message'], 'Missing Parameters')

    @patch('Controllers.Manager.UnassignProject.connect')
    @patch('Controllers.Manager.UnassignProject.disconnect')
    def test_unassign_project_manager_invalid_manager_id(self, mock_disconnect, mock_connect):
        manager = {'manager_id': '999', 'project_id': '101'}
        
        mock_connect.return_value = self.mock_connection
        self.mock_cursor.fetchall.side_effect = [
            [(1,)],  # Manager does not exist,
            []
        ]

        response = unassign_project_manager(manager)
        self.assertEqual(response.status_code, 404)
        response_content = json.loads(response.body)
        self.assertEqual(response_content['message'], 'Invalid Manager Id')

    @patch('Controllers.Manager.UnassignProject.connect')
    @patch('Controllers.Manager.UnassignProject.disconnect')
    def test_unassign_project_manager_invalid_project_id(self, mock_disconnect, mock_connect):
        manager = {'manager_id': 1, 'project_id': '999'}
        
        mock_connect.return_value = self.mock_connection
        self.mock_cursor.fetchall.side_effect = [
           [],  # Manager exists
           [(json.dumps(['999']),)],  # Project exists
        ]

        response = unassign_project_manager(manager)
        self.assertEqual(response.status_code, 404)
        response_content = json.loads(response.body)
        self.assertEqual(response_content['message'], 'Invalid Project Id')

    @patch('Controllers.Manager.UnassignProject.connect')
    @patch('Controllers.Manager.UnassignProject.disconnect')
    def test_unassign_project_manager_project_id_not_exists_for_manager(self, mock_disconnect, mock_connect):
        manager = {'manager_id': '1', 'project_id': '101'}
        
        mock_connect.return_value = self.mock_connection
        self.mock_cursor.fetchall.side_effect = [
            [(1,)],  # Manager exists
            [(json.dumps(['102']),)],  # Project exists
        ]
        self.mock_cursor.fetchone.side_effect = [
            (json.dumps(['2']),),  # Managers assigned to project (manager '1' not in list)
            (json.dumps(['102']),)  # Projects assigned to manager (project '101' not in list)
        ]

        response = unassign_project_manager(manager)
        self.assertEqual(response.status_code, 404)
        response_content = json.loads(response.body)
        self.assertEqual(response_content['message'], "Project Id Doesn't Exists For the manager, Please Provide a Valid Project Id")

    @patch('Controllers.Manager.UnassignProject.connect')
    @patch('Controllers.Manager.UnassignProject.disconnect')
    def test_unassign_project_manager_internal_error(self, mock_disconnect, mock_connect):
        manager = {'manager_id': '1', 'project_id': '101'}

        mock_connect.return_value = self.mock_connection
        self.mock_cursor.execute.side_effect = Exception("Some database error")

        with self.assertRaises(Exception) as context:
            unassign_project_manager(manager)
        
        self.assertTrue('Internal Server Error' in str(context.exception))

if __name__ == '__main__':
    unittest.main()
