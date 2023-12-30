from unittest import TestCase
import unittest
from unittest.mock import patch, Mock
from entry import app

class TestLeaveRequest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_add_leave_request_success(self):
        data = {
            'leaverequestid': 1,
            'employeeid': 101,
            'leavetype': 'Annual',
            'startdate': '2021-02-01',
            'enddate': '2021-02-05',
            'reason': 'Test leave request',
            'status': 'Pending'
        }
        with patch('db.Database.execute_query') as mock_execute_query:
            # Simulate a successful database operation
            mock_execute_query.return_value = None  # Mock the database call
            response =  self.app.post('/saveleaverequest', json=data)
            self.assertEqual(response.status_code, 201)
            print(response.json)

    def test_add_leave_request_error(self):
        data = {
            'leaverequestid': None,
            'employeeid': 101,
            'leavetype': 'Annual',
            'startdate': '2021-02-01',
            'enddate': '2021-02-05',
            'reason': 'Test leave request',
            'status': 'Pending'
        }
        with patch('db.Database.execute_query') as mock_execute_query:
            # Simulate a database error or invalid data
            response = self.app.post('/saveleaverequest', json=data)
            self.assertEqual(response.status_code, 400)

    def test_get_leave_requests_success(self):
        with patch('db.Database.execute_query') as mock_execute_query:
            # Simulate a successful database response
            mock_execute_query.return_value = [
                (1, 101, 'Annual', '2021-02-01', '2021-02-05', 'Test leave request', 'Pending')
            ]
            response = self.app.get('/getleaverequests')
            self.assertEqual(response.status_code, 200)
            print(response.json)

    def test_get_leave_requests_error(self):
        with patch('db.Database.execute_query') as mock_execute_query:
            # Simulate a database error
            mock_execute_query.side_effect = Exception('Database connection error')
            response = self.app.get('/getleaverequests')
            self.assertEqual(response.status_code, 500)

    def test_delete_leave_request_success(self):
        # Simulate a successful deletion
        leaverequest_id = 1
        response = self.app.post(f'/deleteleaverequest/{leaverequest_id}')
        self.assertEqual(response.status_code, 200)

    def test_delete_leave_request_error(self):
        with patch('db.Database.execute_query') as mock_execute_query:
            # Simulate a database error
            mock_execute_query.side_effect = Exception('Database connection error')
            leaverequest_id = 1
            response = self.app.post(f'/deleteleaverequest/{leaverequest_id}')
            self.assertEqual(response.status_code, 500)

if __name__ == '__main__':
    unittest.main()