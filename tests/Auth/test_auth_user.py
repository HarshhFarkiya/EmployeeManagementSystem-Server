import unittest
from unittest.mock import Mock, patch
from fastapi.responses import JSONResponse
import bcrypt
import jwt
import json
from datetime import datetime, timedelta
import sys
import os

# Add the parent directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from Controllers.Auth.auth import auth_user, create_access_token, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES  # Replace 'Controllers.Auth.auth' with the actual module name

class TestAuthUser(unittest.TestCase):

    def setUp(self):
        self.mock_connection = Mock()
        self.mock_cursor = Mock()
        self.mock_connection.cursor.return_value = self.mock_cursor

    @patch('Controllers.Auth.auth.connect')  # Replace 'Controllers.Auth.auth' with the actual module name
    @patch('Controllers.Auth.auth.disconnect')  # Replace 'Controllers.Auth.auth' with the actual module name
    def test_auth_user_success(self, mock_disconnect, mock_connect):
        UserId = 'test@example.com'
        password = 'test_password'
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        mock_connect.return_value = self.mock_connection
        self.mock_cursor.fetchall.side_effect = [
            [('admin', hashed_password, 'User123'),],  # User exists
        ]

        response = auth_user(UserId, password)
        self.assertEqual(response.status_code, 200)
        response_content = json.loads(response.body)
        self.assertEqual(response_content['user_id'], 'User123')
        self.assertEqual(response_content['role'], 'admin')
        self.assertIn('token', response_content)

    @patch('Controllers.Auth.auth.connect')
    @patch('Controllers.Auth.auth.disconnect')
    def test_auth_user_user_doesnt_exist(self, mock_disconnect, mock_connect):
        UserId = 'nonexistent@example.com'
        password = 'test_password'

        mock_connect.return_value = self.mock_connection
        self.mock_cursor.fetchall.side_effect = [
            [],  # User doesn't exist
        ]

        response = auth_user(UserId, password)
        self.assertEqual(response.status_code, 404)
        response_content = json.loads(response.body)
        self.assertEqual(response_content['message'], "User Doesn't Exist")

    @patch('Controllers.Auth.auth.connect')
    @patch('Controllers.Auth.auth.disconnect')
    def test_auth_user_invalid_password(self, mock_disconnect, mock_connect):
        UserId = 'test@example.com'
        password = 'wrong_password'
        hashed_password = bcrypt.hashpw('correct_password'.encode(), bcrypt.gensalt()).decode()

        mock_connect.return_value = self.mock_connection
        self.mock_cursor.fetchall.side_effect = [
            [('admin', hashed_password, 'USER123')],  # Incorrect password
        ]

        response = auth_user(UserId, password)
        self.assertEqual(response.status_code, 401)
        response_content = json.loads(response.body)
        self.assertEqual(response_content['message'], 'Invalid Password')

    @patch('Controllers.Auth.auth.connect')
    @patch('Controllers.Auth.auth.disconnect')
    def test_auth_user_internal_error(self, mock_disconnect, mock_connect):
        UserId = 'test@example.com'
        password = 'test_password'

        mock_connect.return_value = self.mock_connection
        self.mock_cursor.fetchall.side_effect = Exception("Some database error")

        response = auth_user(UserId, password)
        self.assertEqual(response.status_code, 500)
        response_content = json.loads(response.body)
        self.assertEqual(response_content, 'Internal Server Error')

if __name__ == '__main__':
    unittest.main()
