import unittest
from unittest.mock import Mock, patch
from fastapi.responses import JSONResponse
import json
import sys
import os
# Add the parent directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from Models.Project.ProjectModel import Project
from Controllers.Project.Project import add_project  # Replace 'Controllers.Project.Project' with the actual module name

class TestAddProject(unittest.TestCase):

    def setUp(self):
        self.mock_connection = Mock()
        self.mock_cursor = Mock()
        self.mock_connection.cursor.return_value = self.mock_cursor

    @patch('Controllers.Project.Project.connect')  # Replace 'Controllers.Project.Project' with the actual module name
    @patch('Controllers.Project.Project.disconnect')  # Replace 'Controllers.Project.Project' with the actual module name
    def test_add_project_success(self, mock_disconnect, mock_connect):
        project = {'project_name': 'New Project', 'skills_required': 'Python'}

        mock_connect.return_value = self.mock_connection
        self.mock_cursor.fetchone.side_effect = [
            (0,),  # New project ID
        ]
        self.mock_cursor.fetchall.side_effect = [
            [],  # Project name does not exist
        ]

        response = add_project(project)
        self.assertEqual(response.status_code, 200)
        response_content = json.loads(response.body)
        self.assertEqual(response_content['message'], 'Project Added Successfully')
        self.assertEqual(response_content['project_id'], 'PRJ1')

    @patch('Controllers.Project.Project.connect')
    @patch('Controllers.Project.Project.disconnect')
    def test_add_project_missing_parameters(self, mock_disconnect, mock_connect):
        project = {'project_name': 'New Project'}

        mock_connect.return_value = self.mock_connection
        
        response = add_project(project)
        self.assertEqual(response.status_code, 422)
        response_content = json.loads(response.body)
        self.assertEqual(response_content['message'], 'Missing Parameters')

    @patch('Controllers.Project.Project.connect')
    @patch('Controllers.Project.Project.disconnect')
    def test_add_project_already_exists(self, mock_disconnect, mock_connect):
        project = {'project_name': 'Existing Project', 'skills_required': 'Python'}
        
        mock_connect.return_value = self.mock_connection
        self.mock_cursor.fetchone.side_effect = [
            (0,),  # New project ID
        ]
        self.mock_cursor.fetchall.side_effect = [
            [(1,)],  # Project name already exists
        ]

        response = add_project(project)
        self.assertEqual(response.status_code, 409)
        response_content = json.loads(response.body)
        self.assertEqual(response_content['message'], 'Project Already Exists')

    @patch('Controllers.Project.Project.connect')
    @patch('Controllers.Project.Project.disconnect')
    def test_add_project_internal_error(self, mock_disconnect, mock_connect):
        project = {'project_name': 'New Project', 'skills_required': 'Python'}

        mock_connect.return_value = self.mock_connection
        self.mock_cursor.execute.side_effect = Exception("Some database error")

        with self.assertRaises(Exception) as context:
            add_project(project)
        
        self.assertTrue('Internal Server Error' in str(context.exception))

if __name__ == '__main__':
    unittest.main()
