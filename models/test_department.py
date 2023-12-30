from unittest.mock import patch, Mock
import unittest
from entry import app

class TestDepartment(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_add_department_success(self):
       data = {
           'departmentid': 1,
           'departmentname': 'Test department'
       }
       with patch('db.Database.execute_query') as mock_execute_query:
           # Simulate a successful database operation
           mock_execute_query.return_value = None  # Mock the database call
           response = self.app.post('/savedepartment', json=data)
           self.assertEqual(response.status_code, 201)  # Assuming a successful save returns status code 201

    def test_add_department_error(self):
         data = {
              'departmentid': None,  # Intentionally making departmentid None to trigger an error
              'departmentname': 'Test department'
         }
         with patch('db.Database.execute_query') as mock_execute_query:
              # Simulate a database error or invalid data
              response = self.app.post('/savedepartment', json=data)
              self.assertEqual(response.status_code, 400)  # Error in input returns status code 400

    def test_get_departments_success(self):
        with patch('db.Database.execute_query') as mock_execute_query:
            # Simulate a successful database response
            mock_execute_query.return_value = [
                (1, 'IT')
            ]
            response = self.app.get('/getdepartments')
            self.assertEqual(response.status_code, 200) # Successful retrieval returns status code 200
            print(response.json)

    def test_get_departments_error(self):
        with patch('db.Database.execute_query') as mock_execute_query:
            # Simulate a database error
            mock_execute_query.side_effect = Exception('Database connection error')
            response = self.app.get('/getdepartments')
            self.assertEqual(response.status_code, 500)  # Error while fetching returns status code 500

    def test_delete_department_success(self):
        # Simulate a successful deletion
        department_id = 1
        response = self.app.post(f'/deletedepartment/{department_id}')
        self.assertEqual(response.status_code, 200)  # Assuming successful deletion returns status code 200

    def test_delete_department_error(self):
        # Simulate a database error
        department_id = 1
        with patch('db.Database.execute_query') as mock_execute_query:
            mock_execute_query.side_effect = Exception('Database connection error')
            response = self.app.post(f'/deletedepartment/{department_id}')
            self.assertEqual(response.status_code, 500)  # Error while fetching returns status code 500

if __name__ == '__main__':
    unittest.main() 