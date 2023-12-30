import unittest
from unittest.mock import patch, Mock
from entry import app

class TestComplaints(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_add_complaint_success(self):
        data = {
            'complaintid': 1,
            'employeeid': 101,
            'type': 'Issue',
            'description': 'Test complaint',
            'status': 'Pending'
        }
        with patch('db.Database.execute_query') as mock_execute_query:
            # Simulate a successful database operation
            mock_execute_query.return_value = None  # Mock the database call
            response = self.app.post('/savecomplaint', json=data)
            self.assertEqual(response.status_code, 201)  # Assuming a successful save returns status code 201

    def test_add_complaint_error(self):
        data = {
            'complaintid': None,  # Intentionally making complaintid None to trigger an error
            'employeeid': 101,
            'type': 'Issue',
            'description': 'Test complaint',
            'status': 'Pending'
        }
        with patch('db.Database.execute_query') as mock_execute_query:
            # Simulate a database error or invalid data
            response = self.app.post('/savecomplaint', json=data)
            self.assertEqual(response.status_code, 400)  # Error in input returns status code 400


    @patch('db.Database.execute_query')
    def test_get_complaints_success(self, mock_execute_query):
        # Simulate a successful database response
        mock_execute_query.return_value = [
            (1, 101, 'IT', 'Network Issue', 'Pending', '2023-01-01', False, None)
        ]
        response = self.app.get('/getcomplaints')
        self.assertEqual(response.status_code, 200)  # Successful retrieval returns status code 200
        print(response.json)

    @patch('db.Database.execute_query')
    def test_get_complaints_error(self, mock_execute_query):
        # Simulate a database error
        mock_execute_query.side_effect = Exception('Database connection error')
        response = self.app.get('/getcomplaints')
        self.assertEqual(response.status_code, 500)  # Error while fetching returns status code 500

    @patch('db.Database.execute_query')
    def test_delete_complaint_success(self, mock_execute_query):
        # Simulate a successful deletion
        complaint_id = 1
        response = self.app.post(f'/deletecomplaint/{complaint_id}')
        self.assertEqual(response.status_code, 200)  # Assuming successful deletion returns status code 200

    @patch('db.Database.execute_query')
    def test_delete_complaint_error(self, mock_execute_query):
        # Simulate a database error while deleting
        mock_execute_query.side_effect = Exception('Database error')
        complaint_id = 1
        response = self.app.post(f'/deletecomplaint/{complaint_id}')
        self.assertEqual(response.status_code, 500)  # Error during deletion returns status code 500

if __name__ == '__main__':
    unittest.main()
