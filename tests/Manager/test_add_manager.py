import unittest
from unittest.mock import Mock, patch
from fastapi.responses import JSONResponse
import bcrypt
import sys
import os
import json
# Add the parent directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..')))
from Controllers.Manager.Manager import add_manager

class TestAddManager(unittest.TestCase):

    def setUp(self):
        self.mock_connection = Mock()
        self.mock_cursor = Mock()
        self.mock_connection.cursor.return_value = self.mock_cursor

    @patch('Controllers.Manager.Manager.connect')
    @patch('Controllers.Manager.Manager.disconnect')
    def test_add_manager_success(self, mock_disconnect, mock_connect):
        manager = {'email': 'test@example.com', 'phone': '1234567890', 'name': 'Test Manager'}
        
        mock_connect.return_value = self.mock_connection
        self.mock_cursor.fetchone.side_effect = [
            (0,),  # Initial managers count
        ]
        self.mock_cursor.fetchall.side_effect = [
            [],  # Email does not exist
        ]

        response = add_manager(manager)
        self.assertEqual(response.status_code, 200)
        response_content=json.loads(response.body)
        self.assertEqual(response_content['message'], 'User Added Successfully')
        self.assertEqual(response_content['manager_id'], 1)
        self.assertIn('password', response_content)

    @patch('Controllers.Manager.Manager.connect')
    @patch('Controllers.Manager.Manager.disconnect')
    def test_add_manager_missing_parameters(self, mock_disconnect, mock_connect):
        manager = {'email': 'test@example.com', 'phone': '1234567890'}

        mock_connect.return_value = self.mock_connection
        
        response = add_manager(manager)
        self.assertEqual(response.status_code, 422)
        response_content=json.loads(response.body)
        self.assertEqual(response_content['message'], 'Missing Parameters')

    @patch('Controllers.Manager.Manager.connect')
    @patch('Controllers.Manager.Manager.disconnect')
    def test_add_manager_already_exists(self, mock_disconnect, mock_connect):
        manager = {'email': 'test@example.com', 'phone': '1234567890', 'name': 'Test Manager'}
        
        mock_connect.return_value = self.mock_connection
        self.mock_cursor.fetchone.side_effect = [
            (0,),  # Initial managers count
        ]
        self.mock_cursor.fetchall.side_effect = [
            [(1,)],  # Email already exists
        ]

        response = add_manager(manager)
        self.assertEqual(response.status_code, 409)
        response_content=json.loads(response.body)
        self.assertEqual(response_content['message'], 'User Already Exists')

    @patch('Controllers.Manager.Manager.connect')
    @patch('Controllers.Manager.Manager.disconnect')
    def test_add_manager_internal_error(self, mock_disconnect, mock_connect):
        manager = {'email': 'test@example.com', 'phone': '1234567890', 'name': 'Test Manager'}

        mock_connect.return_value = self.mock_connection
        self.mock_cursor.fetchone.side_effect = Exception("Some database error")

        response = add_manager(manager)
        self.assertEqual(response.status_code, 500)
        response_content=json.loads(response.body)
        self.assertEqual(response_content['message'], 'Some Error Occured')

if __name__ == '__main__':
    unittest.main()
