import unittest
from unittest.mock import patch, Mock
from suggestion import *
from entry import app

class TestSuggestion(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_add_suggestion_success(self):
        data ={
            'suggestion_id': 1,
            'employee_id': 101,
            'description': 'Test suggestion',
            'status': 'Pending',
        }
        with patch('db.Database.execute_query') as mock_execute_query:
            # Simulate a successful database operation
            mock_execute_query.return_value = None
            response = self.app.post('/savesuggestion', json=data)
            self.assertEqual(response.status_code, 201)
            print(response.json)

    def test_add_suggestion_error(self):
        data ={
            'suggestion_id': None,
            'employee_id': 101,
            'description': 'Test suggestion',
            'status': 'Pending',
        }
        with patch('db.Database.execute_query') as mock_execute_query:
            # Simulate a database error or invalid data
            response = self.app.post('/savesuggestion', json={})
            self.assertEqual(response.status_code, 400)

    def test_get_suggestion_success(self):
        with patch('db.Database.execute_query') as mock_execute_query:
            # Simulate a successful database response
            mock_execute_query.return_value = [
                (1, 101, 'Test suggestion', 'Pending')
            ]
            response = self.app.get('/getsuggestions')
            self.assertEqual(response.status_code, 200)
            print(response.json)

    def test_get_suggestion_error(self):
        with patch('db.Database.execute_query') as mock_execute_query:
            # Simulate a database error
            mock_execute_query.side_effect = Exception('Database connection error')
            response = self.app.get('/getsuggestions')
            self.assertEqual(response.status_code, 500)

    def test_delete_suggestion_success(self):
        # Simulate a successful deletion
        suggestion_id = 1
        response = self.app.post(f'/deletesuggestion/{suggestion_id}')
        self.assertEqual(response.status_code, 200)

    def test_delete_suggestion_error(self):
        with patch('db.Database.execute_query') as mock_execute_query:
            # Simulate a database error
            suggestion_id = 1
            mock_execute_query.side_effect = Exception('Database connection error')
            response = self.app.post(f'/deletesuggestion/{suggestion_id}')
            self.assertEqual(response.status_code, 500)