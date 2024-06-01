import unittest
from unittest.mock import Mock, patch
from fastapi.responses import JSONResponse
import sys
import os
# Add the parent directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..')))
import json
from Controllers.Manager.DeleteManager import delete_manager

class TestDeleteManager(unittest.TestCase):

    def setUp(self):
        self.mock_connection = Mock()
        self.mock_cursor = Mock()
        self.mock_connection.cursor.return_value = self.mock_cursor

    @patch('Controllers.Manager.DeleteManager.connect')
    @patch('Controllers.Manager.DeleteManager.disconnect')
    def test_delete_manager_success(self, mock_disconnect, mock_connect):
        manager_id = 'MNG1'
        
        mock_connect.return_value = self.mock_connection
        self.mock_cursor.fetchall.side_effect = [
            [(manager_id, 'name', 'email', 'phone', None)],  # Manager exists, not assigned to any project
        ]

        response = delete_manager(manager_id)
        self.assertEqual(response.status_code, 200)
        response_content=json.loads(response.body)
        self.assertEqual(response_content['message'], 'manager Deleted Successfully')

    @patch('Controllers.Manager.DeleteManager.connect')
    @patch('Controllers.Manager.DeleteManager.disconnect')
    def test_delete_manager_not_exists(self, mock_disconnect, mock_connect):
        manager_id = 'MNG1'
        
        mock_connect.return_value = self.mock_connection
        self.mock_cursor.fetchall.side_effect = [
            [],  # Manager does not exist
        ]

        response = delete_manager(manager_id)
        self.assertEqual(response.status_code, 404)
        response_content=json.loads(response.body)
        self.assertEqual(response_content['message'], 'manager Doesnt Exists')

    @patch('Controllers.Manager.DeleteManager.connect')
    @patch('Controllers.Manager.DeleteManager.disconnect')
    def test_delete_manager_already_assigned(self, mock_disconnect, mock_connect):
        manager_id = 'MNG1'
        
        mock_connect.return_value = self.mock_connection
        self.mock_cursor.fetchall.side_effect = [
            [(manager_id, 'name', 'email', 'phone', 'PRJ1')],  # Manager exists, assigned to a project
        ]

        response = delete_manager(manager_id)
        self.assertEqual(response.status_code, 200)
        response_content=json.loads(response.body)
        self.assertEqual(response_content['message'], 'manager already assigned to a project, Unassign before delete the user')

    @patch('Controllers.Manager.DeleteManager.connect')
    @patch('Controllers.Manager.DeleteManager.disconnect')
    def test_delete_manager_internal_error(self, mock_disconnect, mock_connect):
        manager_id = 'MNG1'

        mock_connect.return_value = self.mock_connection
        self.mock_cursor.fetchall.side_effect = Exception("Some database error")

        response = None
        try:
            response = delete_manager(manager_id)
        except Exception as e:
            self.assertEqual(str(e), "('Internal Server Error', Exception('Some database error'))")

if __name__ == '__main__':
    unittest.main()
