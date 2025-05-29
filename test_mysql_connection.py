import mysql.connector
from mysql.connector import Error

db_config = {
    'host': 'localhost',
    'user': 'Sumasri',  # Replace with your MySQL username
    'password': 'Root',  # Replace with your MySQL password
    'database': 'todo_db'
}

try:
    conn = mysql.connector.connect(**db_config)
    if conn.is_connected():
        print("Successfully connected to MySQL database!")
        print(f"Connected as user: {db_config['user']}")
    conn.close()
except Error as e:
    print(f"Error connecting to MySQL: {e}")