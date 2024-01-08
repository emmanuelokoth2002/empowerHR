import unittest
from unittest.mock import patch, MagicMock
from entry import app
from unittest import TestCase

class TestUser(TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_add_user_success(self):
        data ={
            'userid': 1,
            'employeeid': 101,
            'username': 'Test user',
            'password': 'Test password',
            'email': 'employee@gmail.com',
        }
        with patch('db.Database.execute_query') as mock_execute_query:
            # Simulate a successful database operation
            mock_execute_query.return_value = None
            response = self.app.post('/saveuser', json=data)
            self.assertEqual(response.status_code, 201)
            print(response.json)

    def test_add_user_error(self):
        data ={
            'userid': None,
            'employeeid': 101,
            'username': 'Test user',
            'password': 'Test password',
            'email': '  ',
        }
        with patch('db.Database.execute_query') as mock_execute_query:
            # Simulate a database error or invalid data
            response = self.app.post('/saveuser', json={})
            self.assertEqual(response.status_code, 400)

    def test_get_user_success(self):
        with patch('db.Database.execute_query') as mock_execute_query:
            # Simulate a successful database response
            mock_execute_query.return_value = [
                (1, 101, 'Test user', 'Test password', 'employee@gmail.com')
            ]
            response = self.app.get('/getusers')
            self.assertEqual(response.status_code, 200)
            print(response.json)

    def test_get_user_error(self):
        with patch('db.Database.execute_query') as mock_execute_query:
            # Simulate a database error
            mock_execute_query.side_effect = Exception('Database connection error')
            response = self.app.get('/getusers')
            self.assertEqual(response.status_code, 500)

    def test_delete_user_success(self):
        # Simulate a successful deletion
        user_id = 1
        response = self.app.post(f'/deleteuser/{user_id}')
        self.assertEqual(response.status_code, 200)

    def test_delete_user_error(self):
        with patch('db.Database.execute_query') as mock_execute_query:
            # Simulate a database error
            user_id = 1
            mock_execute_query.side_effect = Exception('Database connection error')
            response = self.app.post(f'/deleteuser/{user_id}')
            self.assertEqual(response.status_code, 500)

if __name__ == '__main__':
    unittest.main()