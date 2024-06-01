import unittest
from unittest.mock import Mock, patch
from fastapi.responses import JSONResponse
import json
import sys
import os
# Add the parent directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from Controllers.Project.DeleteProject import delete_project  # Replace 'Controllers.Project.DeleteProject' with the actual module name

class TestDeleteProject(unittest.TestCase):

    def setUp(self):
        self.mock_connection = Mock()
        self.mock_cursor = Mock()
        self.mock_connection.cursor.return_value = self.mock_cursor

    @patch('Controllers.Project.DeleteProject.connect')  # Replace 'Controllers.Project.DeleteProject' with the actual module name
    @patch('Controllers.Project.DeleteProject.disconnect')  # Replace 'Controllers.Project.DeleteProject' with the actual module name
    def test_delete_project_success(self, mock_disconnect, mock_connect):
        project_id = "PRJ1"
        
        mock_connect.return_value = self.mock_connection
        self.mock_cursor.fetchall.side_effect = [
            [(1,)],  # Project exists
        ]
        self.mock_cursor.fetchone.side_effect = [
            ('[1]', '[1,2]'),  # Managers and employees exist
            ('[1]',)
        ]

        response = delete_project(project_id)
        self.assertEqual(response.status_code, 200)
        response_content = json.loads(response.body)
        self.assertEqual(response_content['message'], 'Project Deleted Successfully')

    @patch('Controllers.Project.DeleteProject.connect')
    @patch('Controllers.Project.DeleteProject.disconnect')
    def test_delete_project_not_found(self, mock_disconnect, mock_connect):
        project_id = 'PRJ1'

        mock_connect.return_value = self.mock_connection
        self.mock_cursor.fetchall.side_effect = [
            [],  # Project does not exist
        ]

        response = delete_project(project_id)
        self.assertEqual(response.status_code, 404)
        response_content = json.loads(response.body)
        self.assertEqual(response_content['message'], 'Project Doesnt Exists')

    @patch('Controllers.Project.DeleteProject.connect')
    @patch('Controllers.Project.DeleteProject.disconnect')
    def test_delete_project_internal_error(self, mock_disconnect, mock_connect):
        project_id = 'PRJ1'

        mock_connect.return_value = self.mock_connection
        self.mock_cursor.execute.side_effect = Exception("Some database error")

        with self.assertRaises(Exception) as context:
            delete_project(project_id)
        
        self.assertTrue('Internal Server Error' in str(context.exception))

if __name__ == '__main__':
    unittest.main()
