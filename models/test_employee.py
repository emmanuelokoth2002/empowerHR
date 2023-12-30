from unittest import TestCase
import unittest
from unittest.mock import patch, Mock
from entry import app

class TestEmployee(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_add_employee_success(self):
        data = {
            'employeeid': 1,
            'firstname': 'John',
            'lastname': 'Doe',
            'email': 'jdoe@gmail.com',
            'dateofbirth': '12/2/1990',
            'phonenumber': '0784356233',
            'address': '80100-msa',
            'departmentid': 3,
            'roleid': 2
        }
        with patch('db.Database.execute_query') as mock_execute_query:
            # Simulate a successful database operation
            mock_execute_query.return_value = None  # Mock the database call
            response = self.app.post('/saveemployee', json=data)
            self.assertEqual(response.status_code, 201)

    def test_add_employee_error(self):
        data = {
            'employeeid': None,
            'firstname': 'John',
            'lastname': 'Doe',
            'email': 'jdoe@gmail.com',
            'dateofbirth': '12/2/1990',
            'phonenumber': '0784356233',
            'address': '80100-msa',
            'departmentid': 3,
            'roleid': 2
        }
        with patch('db.Database.execute_query') as mock_execute_query:
            # Simulate a database error or invalid data
            response = self.app.post('/saveemployee', json=data)
            self.assertEqual(response.status_code, 400)

    def test_get_employees_success(self):
        with patch('db.Database.execute_query') as mock_execute_query:
            # Simulate a successful database response
            mock_execute_query.return_value = [
                (1, 'John', 'Doe', 'jdoe@gmail.com', '12/2/1990', '0784356233', '80100-msa', 3, 2)
            ]
            response = self.app.get('/getemployees')
            self.assertEqual(response.status_code, 200)
            print(response.json)

    def test_get_employees_error(self):
        with patch('db.Database.execute_query') as mock_execute_query:
            # Simulate a database error
            mock_execute_query.side_effect = Exception('Database connection error')
            response = self.app.get('/getemployees')
            self.assertEqual(response.status_code, 500)

    def test_delete_employee_success(self):
        # Simulate a successful deletion
        employee_id = 1
        response = self.app.post(f'/deleteemployee/{employee_id}')
        self.assertEqual(response.status_code, 200)

    def test_delete_employee_error(self):
        # Simulate a database error
        employee_id = 1
        with patch('db.Database.execute_query') as mock_execute_query:
            mock_execute_query.side_effect = Exception('Database connection error')
            response = self.app.post(f'/deleteemployee/{employee_id}')
            self.assertEqual(response.status_code, 500) # Error while fetching returns status code 500

if __name__ == '__main__':
    unittest.main()