import mysql.connector
import json

class Database:
    def __init__(self):
        self.dbname = "empowerhr"
        self.dbuser = "root"
        self.dbpassword = ""
        self.dbhost = "localhost"
        self.conn = None

    def connect(self):
        try:
            conn = mysql.connector.connect(
                host=self.dbhost,
                user=self.dbuser,
                password=self.dbpassword,
                database=self.dbname
            )
            cursor = conn.cursor()
            return conn, cursor
        except mysql.connector.Error as e:
            print("Connection failed:", e)
            raise

    def execute_query(self, query, args=None):
        conn, cursor = self.connect()
        try:
            print("Executing query:", query)
            print("With args:", args)
            cursor.execute(query, args)
            conn.commit()
        except Exception as e:
            print("Error executing query:", str(e))
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()

    def get_data(self, query, args=None, multi=True):
        conn, cursor = self.connect()
        try:
            print("Executing query:", query)
            print("With args:", args)
            
            if args is not None:
                cursor.callproc(query, args)
            else:
                cursor.callproc(query)

            if multi:
                result = []
                for result_cursor in cursor.stored_results():
                    result.extend(result_cursor.fetchall())
                return result
            else:
                return cursor.fetchall()

        except Exception as e:
            print("Error fetching results:", str(e))
            raise
        finally:
            cursor.close()
            conn.close()

    def get_json(self, query):
        data = self.fetch_results(query)
        json_data = json.dumps(data)
        return json_data

    def close_connection(self):
        if self.conn:
            self.conn.close()
