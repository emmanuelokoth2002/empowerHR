import unittest
from unittest.mock import patch, Mock
from entry import app

class TestRole(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_add_role_success(self):
        data ={
            'roleid': 1,
            'rolename': 'Admin',
        }
        with patch('db.Database.execute_query') as mock_execute_query:
            # Simulate a successful database operation
            mock_execute_query.return_value = None
            response = self.app.post('/saverole', json=data)
            self.assertEqual(response.status_code, 201)
            print(response.json)

    def test_add_role_error(self):
        data ={
            'roleid': None,
            'rolename': 'Admin',
        }
        with patch('db.Database.execute_query') as mock_execute_query:
            # Simulate a database error or invalid data
            response = self.app.post('/saverole', json={})
            self.assertEqual(response.status_code, 400)

    def test_get_role_success(self):
        with patch('db.Database.execute_query') as mock_execute_query:
            # Simulate a successful database response
            mock_execute_query.return_value = [
                (1, 'Admin')
            ]
            response = self.app.get('/getroles')
            self.assertEqual(response.status_code, 200)
            print(response.json)

    def test_get_role_error(self):
        with patch('db.Database.execute_query') as mock_execute_query:
            # Simulate a database error
            mock_execute_query.side_effect = Exception('Database connection error')
            response = self.app.get('/getroles')
            self.assertEqual(response.status_code, 500)

    def test_delete_role_success(self):
        # Simulate a successful deletion
        role_id = 1
        response = self.app.post(f'/deleterole/{role_id}')
        self.assertEqual(response.status_code, 200)

    def test_delete_role_error(self):
        role_id = 1
        with patch('db.Database.execute_query') as mock_execute_query:
            # Simulate a database error
            mock_execute_query.side_effect = Exception('Database connection error')
            response = self.app.post(f'/deleterole/{role_id}')
            self.assertEqual(response.status_code, 500)

if __name__ == '__main__':
    unittest.main()