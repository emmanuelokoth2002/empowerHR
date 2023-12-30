import unittest
from unittest.mock import patch, Mock
from db import Database

class TestDatabase(unittest.TestCase):
    def test_connect_success(self):
        # Simulating a successful database connection
        with patch('mysql.connector.connect') as mock_connect:
            db = Database()
            db.connect()
            mock_connect.assert_called_once()

    @patch('mysql.connector.connect')
    def test_connect_failure(self, mock_connect):
        # Simulating a database connection failure
        mock_connect.side_effect = Exception('Connection failed')
        db = Database()
        with self.assertRaises(Exception):
            db.connect()

    @patch('mysql.connector.connect')
    def test_execute_query_success(self, mock_connect):
        # Simulating a successful query execution
        mock_cursor = mock_connect.return_value.cursor.return_value
        db = Database()
        db.execute_query('SELECT * FROM table')
        mock_cursor.execute.assert_called_once_with('SELECT * FROM table', None)

    @patch('mysql.connector.connect')
    def test_execute_query_failure(self, mock_connect):
        # Simulating a query execution failure
        mock_cursor = mock_connect.return_value.cursor.return_value
        mock_cursor.execute.side_effect = Exception('Query execution failed')
        db = Database()
        with self.assertRaises(Exception):
            db.execute_query('SELECT * FROM table')

    @patch('mysql.connector.connect')
    def test_get_data_success(self, mock_connect):
        # Simulating a successful data retrieval
        mock_cursor = mock_connect.return_value.cursor.return_value
        mock_cursor.stored_results.return_value = [
            Mock(fetchall=Mock(return_value=[(1, 'Test')]))
        ]
        db = Database()
        result = db.get_data('SELECT * FROM table')
        self.assertEqual(result, [(1, 'Test')])

    @patch('mysql.connector.connect')
    def test_get_data_failure(self, mock_connect):
        # Simulating a data retrieval failure
        mock_cursor = mock_connect.return_value.cursor.return_value
        mock_cursor.stored_results.side_effect = Exception('Data retrieval failed')
        db = Database()
        with self.assertRaises(Exception):
            db.get_data('SELECT * FROM table')

    @patch('mysql.connector.connect')
    def test_get_json_success(self, mock_connect):
        # Simulating a successful JSON response
        mock_cursor = mock_connect.return_value.cursor.return_value
        mock_cursor.stored_results.return_value = [
            Mock(fetchall=Mock(return_value=[(1, 'Test')]))
        ]
        db = Database()
        result = db.get_json('SELECT * FROM table')
        self.assertEqual(result, '[[1, "Test"]]')
        self.assertEqual(type(result), str)

    @patch('mysql.connector.connect')
    def test_get_json_failure(self, mock_connect):
        # Simulating a JSON response failure
        mock_cursor = mock_connect.return_value.cursor.return_value
        mock_cursor.stored_results.side_effect = Exception('JSON response failed')
        db = Database()
        with self.assertRaises(Exception):
            db.get_json('SELECT * FROM table')

    @patch('mysql.connector.connect')
    def close_connection_success(self, mock_connect):
        # Simulating a successful connection close
        mock_cursor = mock_connect.return_value.cursor.return_value
        db = Database()
        db.close_connection()
        mock_cursor.close.assert_called_once()
        mock_connect.close.assert_called_once()

    @patch('mysql.connector.connect')
    def close_connection_failure(self, mock_connect):
        # Simulating a connection close failure
        mock_cursor = mock_connect.return_value.cursor.return_value
        mock_cursor.close.side_effect = Exception('Connection close failed')
        db = Database()
        with self.assertRaises(Exception):
            db.close_connection()


if __name__ == '__main__':
    unittest.main()