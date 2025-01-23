from flask import Flask, jsonify
from flask_cors import CORS
import pyodbc
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

# Database configuration
server = 'EMMASPC\\MSSQLSERVER01'
database = 'Elevdatabase'

# Define a function to get students from the database
def get_students():
    conn = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT ElevID, Navn, TeamID FROM Elever
    ''')
    
    students = cursor.fetchall()
    conn.close()

    # Format the result as a list of dictionaries
    return [{"ElevID": student[0], "Navn": student[1], "TeamID": student[2]} for student in students]

# Route to get all students
@app.route('/api/students', methods=['GET'])
def students():
    try:
        student_list = get_students()
        return jsonify(student_list), 200  # Return the student list as JSON
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Handle any errors

if __name__ == '__main__':
    app.run(debug=True)