# app.py
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import sqlite3
import os
import datetime

app = Flask(__name__)
CORS(app)

# Secrets should be provided via environment in production
SECRET_KEY = os.getenv('SECRET_KEY', 'secret_key_moroccan_2024')
JWT_SECRET = os.getenv('JWT_SECRET', 'jwt_secret_weak')
PORT = int(os.getenv('PORT', 8080))

# Simple index page (no hints, no debug info, no listed endpoints)
INDEX_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Secure Login Portal</title>
    <style>
        /* styles kept minimal and friendly */
        * { margin:0; padding:0; box-sizing:border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height:100vh; display:flex; align-items:center; justify-content:center;
            padding:20px;
        }
        .container { background:white; padding:36px; border-radius:10px; max-width:420px; width:100%; box-shadow:0 10px 40px rgba(0,0,0,0.15); }
        h1 { text-align:center; margin-bottom:8px; color:#333; }
        .subtitle { text-align:center; color:#666; margin-bottom:20px; font-size:14px; }
        .form-group { margin-bottom:16px; }
        label { display:block; margin-bottom:6px; color:#555; }
        input { width:100%; padding:10px; border:2px solid #ddd; border-radius:6px; font-size:14px; }
        input:focus { outline:none; border-color:#667eea; }
        button { width:100%; padding:12px; border:none; border-radius:6px; font-weight:600; background:linear-gradient(135deg,#667eea 0%,#764ba2 100%); color:white; cursor:pointer; }
        .result { margin-top:16px; padding:12px; border-radius:6px; display:none; }
        .success { background:#d4edda; color:#155724; border:1px solid #c3e6cb; }
        .error { background:#f8d7da; color:#721c24; border:1px solid #f5c6cb; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔐 Secure Portal</h1>
        <p class="subtitle">Authentication System v1.0</p>
        <form id="loginForm">
            <div class="form-group">
                <label for="username">Username</label>
                <input id="username" name="username" required>
            </div>
            <div class="form-group">
                <label for="password">Password</label>
                <input id="password" name="password" type="password" required>
            </div>
            <button type="submit">Login</button>
        </form>
        <div id="result" class="result"></div>
    </div>

    <script>
    document.getElementById('loginForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        const resultDiv = document.getElementById('result');
        try {
            const resp = await fetch('/api/login', {
                method: 'POST',
                headers: {'Content-Type':'application/json'},
                body: JSON.stringify({username, password})
            });
            const data = await resp.json();
            resultDiv.style.display = 'block';
            if (data.success) {
                resultDiv.className = 'result success';
                resultDiv.innerHTML = `<strong>✓ Success</strong><br>Welcome ${data.username}<br>Role: ${data.role}`;
                if (data.token) localStorage.setItem('token', data.token);
            } else {
                resultDiv.className = 'result error';
                resultDiv.innerHTML = `<strong>✗ Error:</strong> ${data.error || 'Invalid credentials'}`;
            }
        } catch (err) {
            resultDiv.style.display = 'block';
            resultDiv.className = 'result error';
            resultDiv.innerHTML = '<strong>✗ Error:</strong> Connection failed';
        }
    });
    </script>
</body>
</html>
'''

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')
    # seed users (passwords hashed). In production, create users via admin workflow.
    seed = [
        ('guest', generate_password_hash('guest123'), 'user'),
        ('admin', generate_password_hash('Admin@2024!Morocco'), 'admin')
    ]
    for username, pwd_hash, role in seed:
        try:
            c.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', (username, pwd_hash, role))
        except sqlite3.IntegrityError:
            pass
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template_string(INDEX_HTML)

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username', '').strip()
    password = data.get('password', '')

    if not username or not password:
        return jsonify({'success': False, 'error': 'Missing credentials'}), 400

    conn = get_db_connection()
    c = conn.cursor()
    # parameterized query to avoid SQL injection
    c.execute('SELECT id, username, password, role FROM users WHERE username = ?', (username,))
    row = c.fetchone()
    conn.close()

    if not row:
        return jsonify({'success': False, 'error': 'Invalid credentials'}), 401

    stored_hash = row['password']
    if not check_password_hash(stored_hash, password):
        return jsonify({'success': False, 'error': 'Invalid credentials'}), 401

    user_payload = {
        'username': row['username'],
        'role': row['role'],
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    }
    token = jwt.encode(user_payload, JWT_SECRET, algorithm='HS256')

    return jsonify({
        'success': True,
        'username': row['username'],
        'role': row['role'],
        'token': token
    }), 200

# Note: intentionally no file-read endpoints, no debug endpoint, no flag access.

if __name__ == '__main__':
    print(f"🚀 Starting app on port {PORT}")
    app.run(host='0.0.0.0', port=PORT, debug=False)
