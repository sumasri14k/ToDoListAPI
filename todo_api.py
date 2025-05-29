from flask import Flask, jsonify, request
from waitress import serve
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'Sumasri',  # Replace with your MySQL username
    'password': 'Root',  # Replace with your MySQL password
    'database': 'todo_db'
}

def init_db():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                completed BOOLEAN DEFAULT FALSE
            )
        """)
        conn.commit()
    except Error as e:
        print(f"Error initializing database: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Initialize database on startup
init_db()

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/tasks', methods=['GET'])
def get_tasks():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tasks")
        tasks = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(tasks), 200
    except Error as e:
        return jsonify({"error": f"Database error: {e}"}), 500

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
        task = cursor.fetchone()
        cursor.close()
        conn.close()
        if task:
            return jsonify(task), 200
        return jsonify({"error": "Task not found"}), 404
    except Error as e:
        return jsonify({"error": f"Database error: {e}"}), 500

@app.route('/tasks', methods=['POST'])
def create_task():
    if not request.json or 'title' not in request.json:
        return jsonify({"error": "Title is required"}), 400
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        task = (
            request.json['title'],
            request.json.get('description', ''),
            False
        )
        cursor.execute(
            "INSERT INTO tasks (title, description, completed) VALUES (%s, %s, %s)",
            task
        )
        conn.commit()
        task_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return jsonify({"id": task_id, "title": task[0], "description": task[1], "completed": task[2]}), 201
    except Error as e:
        return jsonify({"error": f"Database error: {e}"}), 500

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    if not request.json:
        return jsonify({"error": "Request body must be JSON"}), 400
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
        task = cursor.fetchone()
        if not task:
            cursor.close()
            conn.close()
            return jsonify({"error": "Task not found"}), 404

        updates = {
            'title': request.json.get('title', task['title']),
            'description': request.json.get('description', task['description']),
            'completed': request.json.get('completed', task['completed'])
        }
        cursor.execute(
            "UPDATE tasks SET title = %s, description = %s, completed = %s WHERE id = %s",
            (updates['title'], updates['description'], updates['completed'], task_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify(updates | {"id": task_id}), 200
    except Error as e:
        return jsonify({"error": f"Database error: {e}"}), 500

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
        task = cursor.fetchone()
        if not task:
            cursor.close()
            conn.close()
            return jsonify({"error": "Task not found"}), 404
        cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Task deleted"}), 200
    except Error as e:
        return jsonify({"error": f"Database error: {e}"}), 500

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)