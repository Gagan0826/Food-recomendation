import mysql.connector
db_config = {
    'user': 'root',
    'password': 'a4appless',
    'host': '127.0.0.1',
    'database': 'CafeManagement'
}

class Database:
    @staticmethod
    def execute_query(query, params=None):
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def fetch_query(query, params=None):
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results

