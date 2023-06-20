from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect('data.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        subject TEXT,
        phone TEXT,
        description TEXT
    )
''')
conn.commit()

@app.route('/api/contacts', methods=['POST'])
def add_contact():
   data = request.get_json()
   name = data.get("name")
   email = data.get("email")
   subject = data.get("subject")
   phone = data.get("phone")
   description = data.get("description")
   
   if not name or not email or not subject or not phone or not description:
      return jsonify(message='Please provide all the required fields.'), 400
   
   try:
      cursor.execute('''
         INSERT INTO contacts (name, email, subject, phone, description)
         VALUES (?, ?, ?, ?, ?)
      ''', (name, email, subject, phone, description))
      conn.commit()
      return jsonify(message='Contact added successfully!'), 200
   except Exception as e:
      return jsonify(message='An error occurred while adding the contact.'), 500


