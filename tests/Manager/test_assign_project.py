import unittest
from unittest.mock import Mock, patch
from fastapi.responses import JSONResponse
import sys
import os
import json
# Add the parent directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..')))
from Controllers.Manager.AssignProject import assign_project_manager

class TestAssignProjectManage(unittest.TestCase):

    def setUp(self):
        self.mock_connection = Mock()
        self.mock_cursor = Mock()
        self.mock_connection.cursor.return_value = self.mock_cursor

    @patch('Controllers.Manager.AssignProject.connect')
    @patch('Controllers.Manager.AssignProject.disconnect')
    def test_assign_project_manager_success(self, mock_disconnect, mock_connect):
        project = {'manager_id': 'MNG1', 'project_id': 'PRJ1'}
        
        mock_connect.return_value = self.mock_connection
        self.mock_cursor.fetchall.side_effect = [
            [(1,)],  # Project exists
            [(None,)], # No previous projects for the manager
        ]
        self.mock_cursor.fetchone.side_effect = [
            None,  # No previous managers
        ]

        response = assign_project_manager(project)
        self.assertEqual(response.status_code, 200)
        response_content=json.loads(response.body)
        self.assertEqual(response_content['message'], 'Project Assigned To Manager Successfully')

    @patch('Controllers.Manager.AssignProject.connect')
    @patch('Controllers.Manager.AssignProject.disconnect')
    def test_assign_project_manager_missing_parameters(self, mock_disconnect, mock_connect):
        project = {'manager_id': 'MNG1'}

        mock_connect.return_value = self.mock_connection
        
        response = assign_project_manager(project)
        self.assertEqual(response.status_code, 422)
        response_content=json.loads(response.body)
        self.assertEqual(response_content['message'], 'Missing Parameters')

    @patch('Controllers.Manager.AssignProject.connect')
    @patch('Controllers.Manager.AssignProject.disconnect')
    def test_assign_project_manager_project_not_exists(self, mock_disconnect, mock_connect):
        project = {'manager_id': 'MNG1', 'project_id': 'PRJ1'}
        
        mock_connect.return_value = self.mock_connection
        self.mock_cursor.fetchall.side_effect = [
            [],  # Project does not exist
        ]

        response = assign_project_manager(project)
        self.assertEqual(response.status_code, 404)
        response_content=json.loads(response.body)
        self.assertEqual(response_content['message'], "Project Doesn't Exists, Please Provide a Valid Active Project Id")

    @patch('Controllers.Manager.AssignProject.connect')
    @patch('Controllers.Manager.AssignProject.disconnect')
    def test_assign_project_manager_manager_not_exists(self, mock_disconnect, mock_connect):
        project = {'manager_id': 'MNG1', 'project_id': 'PRJ1'}
        
        mock_connect.return_value = self.mock_connection
        self.mock_cursor.fetchall.side_effect = [
            [(1,)],  # Project exists
            [],  # Manager does not exist
        ]

        response = assign_project_manager(project)
        self.assertEqual(response.status_code, 404)
        response_content=json.loads(response.body)
        self.assertEqual(response_content['message'], "Manager Doesn't Exists, Please Provide a Valid Manager Id")

    @patch('Controllers.Manager.AssignProject.connect')
    @patch('Controllers.Manager.AssignProject.disconnect')
    def test_assign_project_manager_already_assigned(self, mock_disconnect, mock_connect):
        project = {'manager_id': 1, 'project_id': 1}
        
        mock_connect.return_value = self.mock_connection
        self.mock_cursor.fetchall.side_effect = [
            [(1,)],  # Project exists
            [('[2,3]',)],  # Project exists
        ]
        self.mock_cursor.fetchone.side_effect = [
            ['[1,2,3]'],  # Previous managers include MNG1
        ]

        response = assign_project_manager(project)
        self.assertEqual(response.status_code, 200)
        response_content=json.loads(response.body)
        self.assertEqual(response_content['message'], 'Manager Already Assigned')

    @patch('Controllers.Manager.AssignProject.connect')
    @patch('Controllers.Manager.AssignProject.disconnect')
    def test_assign_project_manager_internal_error(self, mock_disconnect, mock_connect):
        project = {'manager_id': 'MNG1', 'project_id': 'PRJ1'}

        mock_connect.return_value = self.mock_connection
        self.mock_cursor.fetchall.side_effect = Exception("Some database error")

        response = None
        try:
            response = assign_project_manager(project)
        except Exception as e:
            self.assertEqual(str(e), "('Internal Server Error', Exception('Some database error'))")

if __name__ == '__main__':
    unittest.main()
