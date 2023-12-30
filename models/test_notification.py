from unittest import TestCase
import unittest
from unittest.mock import patch, Mock
from entry import app

class TestNotification(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_add_notification_success(self):
        data ={
            'notificationid': 1,
            'employeeid': 101,
            'notificationtype': 'Leave Request',
            'message': 'Test leave request',
            'is_read': False,
        }
        with patch('db.Database.execute_query') as mock_execute_query:
            # Simulate a successful database operation
            mock_execute_query.return_value = None
            response = self.app.post('/savenotification', json=data)
            self.assertEqual(response.status_code, 201)
            print(response.json)

    def test_add_notification_error(self):
        data ={
            'notificationid': None,
            'employeeid': 101,
            'notificationtype': 'Leave Request',
            'message': 'Test leave request',
            'is_read': False,
        }
        with patch('db.Database.execute_query') as mock_execute_query:
            # Simulate a database error or invalid data
            response = self.app.post('/savenotification', json=data)
            self.assertEqual(response.status_code, 500)

    def test_get_notification_success(self):
        with patch('db.Database.execute_query') as mock_execute_query:
            # Simulate a successful database response
            mock_execute_query.return_value = [
                (1, 101, 'Leave Request', 'Test leave request', False)
            ]
            response = self.app.get('/getnotifications')
            self.assertEqual(response.status_code, 200)
            print(response.json)

    def test_get_notification_error(self):
        with patch('db.Database.execute_query') as mock_execute_query:
            # Simulate a database error
            mock_execute_query.side_effect = Exception('Database connection error')
            response = self.app.get('/getnotifications')
            self.assertEqual(response.status_code, 500)

    def test_delete_notification_success(self):
        # Simulate a successful deletion
        notification_id = 1
        response = self.app.post(f'/deletenotification/{notification_id}')
        self.assertEqual(response.status_code, 200)
        
    def test_delete_notification_error(self):
        # Simulate a database error
        notification_id = 1
        with patch('db.Database.execute_query') as mock_execute_query:
            mock_execute_query.side_effect = Exception('Database connection error')
            response = self.app.post(f'/deletenotification/{notification_id}')
            self.assertEqual(response.status_code, 500)

if __name__ == '__main__':
     unittest.main()