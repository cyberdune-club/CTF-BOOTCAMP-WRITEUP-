#!/usr/bin/env python3
from flask import Flask, request, render_template_string, session, redirect, url_for
import sqlite3
import hashlib
import os
import pickle
import base64
from functools import wraps

app = Flask(__name__)
app.secret_key = os.urandom(32)

# Initialize database (no visible hints/flags)
def init_db():
    conn = sqlite3.connect('bank.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT, role TEXT, balance INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS transactions
                 (id INTEGER PRIMARY KEY, user_id INTEGER, amount INTEGER, description TEXT, secret_note TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS admin_logs
                 (id INTEGER PRIMARY KEY, action TEXT, timestamp TEXT, meta TEXT)''')
    
    # Default users (passwords hashed, nothing printed in UI)
    admin_pass = hashlib.md5(b"changeme_admin").hexdigest()
    user_pass = hashlib.md5(b"user_pass").hexdigest()
    
    c.execute("INSERT OR IGNORE INTO users VALUES (1, 'admin', ?, 'admin', 1000000)", (admin_pass,))
    c.execute("INSERT OR IGNORE INTO users VALUES (2, 'youssef', ?, 'user', 5000)", (user_pass,))
    c.execute("INSERT OR IGNORE INTO users VALUES (3, 'fatima', ?, 'user', 3000)", (user_pass,))
    
    # No flags or revealing notes in transactions or logs
    c.execute("INSERT OR IGNORE INTO transactions VALUES (1, 2, -500, 'Payment processed', '')")
    c.execute("INSERT OR IGNORE INTO transactions VALUES (2, 2, 1000, 'Salary credit', '')")
    c.execute("INSERT OR IGNORE INTO transactions VALUES (3, 3, -200, 'Utility bill', '')")
    
    c.execute("INSERT OR IGNORE INTO admin_logs VALUES (1, 'System initialized', '2024-01-15', '')")
    
    conn.commit()
    conn.close()

init_db()

# Login required decorator
def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Admin required decorator
def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'role' not in session or session['role'] != 'admin':
            return "Access Denied! Admins only.", 403
        return f(*args, **kwargs)
    return decorated_function

HOME_TEMPLATE = """
<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
    <meta charset="UTF-8">
    <title>بوابة إلكترونية</title>
    <style>
        body { font-family: Arial, sans-serif; background: linear-gradient(135deg,#667eea 0%,#764ba2 100%); margin:0; padding:20px; direction: rtl; }
        .card { max-width:800px; margin:0 auto; background:#fff; padding:30px; border-radius:12px; box-shadow:0 8px 30px rgba(0,0,0,0.2); }
        h1 { color:#333; text-align:center; }
        p { color:#555; line-height:1.6; }
        .btn { display:inline-block; padding:12px 24px; background:#667eea; color:#fff; text-decoration:none; border-radius:8px; }
    </style>
</head>
<body>
    <div class="card">
        <h1>بوابة إلكترونية</h1>
        <p>مرحبا. هاذ الواجهة مخصّصة لتحدي تقني. الدخول عبر صفحة التسجيل.</p>
        <div style="text-align:center; margin-top:20px;">
            <a href="/login" class="btn">تسجيل الدخول</a>
        </div>
    </div>
</body>
</html>
"""

LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>تسجيل الدخول</title>
    <style>
        body { font-family: Arial, sans-serif; background: linear-gradient(135deg,#667eea 0%,#764ba2 100%); display:flex; align-items:center; justify-content:center; height:100vh; margin:0; }
        .box { background:#fff; padding:30px; border-radius:12px; width:360px; box-shadow:0 8px 30px rgba(0,0,0,0.2); }
        input { width:100%; padding:10px; margin:10px 0; border-radius:6px; border:1px solid #ddd; box-sizing:border-box; }
        button { width:100%; padding:12px; background:#667eea; color:#fff; border:none; border-radius:8px; cursor:pointer; }
        .error { color:#c62828; text-align:center; }
    </style>
</head>
<body>
    <div class="box">
        <h2 style="text-align:center;">تسجيل الدخول</h2>
        {% if error %}
        <p class="error">{{ error }}</p>
        {% endif %}
        <form method="POST">
            <input type="text" name="username" placeholder="اسم المستخدم" required>
            <input type="password" name="password" placeholder="كلمة السر" required>
            <button type="submit">دخول</button>
        </form>
    </div>
</body>
</html>
"""

DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html dir="rtl">
<head>
<meta charset="UTF-8">
<title>لوحة المستخدم</title>
<style>
body { font-family: Arial, sans-serif; background: linear-gradient(135deg,#667eea 0%,#764ba2 100%); margin:0; padding:20px; }
.container { max-width:1000px; margin:0 auto; background:#fff; padding:30px; border-radius:12px; }
.header { display:flex; justify-content:space-between; align-items:center; }
.btn { padding:10px 18px; background:#667eea; color:#fff; text-decoration:none; border-radius:8px; }
.logout { background:#d32f2f; }
.table { width:100%; border-collapse:collapse; margin-top:20px; }
.table th, .table td { padding:12px; border-bottom:1px solid #eee; text-align:right; }
</style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1>مرحبا {{ username }}</h1>
        <div>
            {% if role == 'admin' %}
            <a href="/admin" class="btn">لوحة الأدمن</a>
            {% endif %}
            <a href="/profile" class="btn">الملف</a>
            <a href="/logout" class="btn logout">خروج</a>
        </div>
    </div>

    <div style="margin-top:20px; padding:18px; background:linear-gradient(90deg,#eef4ff,#f7f0ff); border-radius:8px;">
        <strong>الرصيد:</strong> {{ balance }} وحدة
    </div>

    <h2 style="margin-top:20px;">المعاملات الأخيرة</h2>
    <table class="table">
        <tr><th>المبلغ</th><th>الوصف</th></tr>
        {% for trans in transactions %}
        <tr><td>{{ trans[0] }}</td><td>{{ trans[1] }}</td></tr>
        {% endfor %}
    </table>

    <h3 style="margin-top:20px;">بحث</h3>
    <form method="POST" action="/search">
        <input type="text" name="query" placeholder="ابحث..." style="width:70%; padding:10px; border-radius:6px; border:1px solid #ddd;">
        <button type="submit" class="btn">بحث</button>
    </form>
</div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HOME_TEMPLATE)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        password_hash = hashlib.md5(password.encode()).hexdigest()
        
        conn = sqlite3.connect('bank.db')
        c = conn.cursor()
        c.execute("SELECT id, username, role, balance FROM users WHERE username=? AND password=?", 
                  (username, password_hash))
        user = c.fetchone()
        conn.close()
        
        if user:
            session['user_id'] = user[0]
            session['username'] = user[1]
            session['role'] = user[2]
            session['balance'] = user[3]
            return redirect(url_for('dashboard'))
        else:
            return render_template_string(LOGIN_TEMPLATE, error="اسم المستخدم أو كلمة السر خاطئة!")
    return render_template_string(LOGIN_TEMPLATE)

@app.route('/dashboard')
@login_required
def dashboard():
    conn = sqlite3.connect('bank.db')
    c = conn.cursor()
    c.execute("SELECT amount, description FROM transactions WHERE user_id=? ORDER BY id DESC LIMIT 5", 
              (session['user_id'],))
    transactions = c.fetchall()
    conn.close()
    
    return render_template_string(DASHBOARD_TEMPLATE, 
                                   username=session.get('username','مستخدم'),
                                   role=session.get('role','user'),
                                   balance=session.get('balance',0),
                                   transactions=transactions)

@app.route('/search', methods=['POST'])
@login_required
def search():
    query = request.form.get('query', '')
    conn = sqlite3.connect('bank.db')
    c = conn.cursor()
    # Keep original behavior but using parameterized LIKE to avoid accidental leaks
    try:
        c.execute("SELECT amount, description FROM transactions WHERE user_id=? AND description LIKE ?",
                  (session['user_id'], f"%{query}%"))
        results = c.fetchall()
        conn.close()
        return render_template_string("""
        <html dir="rtl"><head><meta charset="UTF-8"><title>نتائج</title>
        <style>body{font-family:Arial;padding:20px;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);} .box{max-width:800px;margin:0 auto;background:#fff;padding:20px;border-radius:10px;}</style>
        </head><body><div class="box"><h2>نتائج البحث عن: {{ query }}</h2>
        <table style="width:100%; border-collapse:collapse;"><tr><th style="text-align:right;padding:8px;">المبلغ</th><th style="text-align:right;padding:8px;">الوصف</th></tr>
        {% for r in results %}<tr><td style="padding:8px;">{{ r[0] }}</td><td style="padding:8px;">{{ r[1] }}</td></tr>{% endfor %}
        </table><p style="margin-top:16px;"><a href='/dashboard'>رجوع</a></p></div></body></html>
        """, query=query, results=results)
    except Exception as e:
        conn.close()
        return f"<html dir='rtl'><body style='padding:20px;'><h2>خطأ:</h2><pre>{str(e)}</pre><br><a href='/dashboard'>رجوع</a></body></html>"

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        greeting = request.form.get('greeting', 'مرحبا')
        # render a safe template, do not expose internal data
        return render_template_string("""
        <html dir="rtl"><head><meta charset="UTF-8"><title>الملف</title></head><body style="font-family:Arial;padding:20px;">
        <div style="max-width:600px;margin:0 auto;background:#fff;padding:20px;border-radius:8px;">
        <h2>الملف الشخصي</h2>
        <div style="background:#f0f0f0;padding:12px;border-radius:6px;">{{ greeting }} {{ username }}!</div>
        <p>الرصيد: {{ balance }}</p>
        <p><a href="/dashboard">رجوع</a></p>
        </div></body></html>
        """, greeting=greeting, username=session.get('username','مستخدم'), balance=session.get('balance',0))
    return render_template_string("""
    <html dir="rtl"><head><meta charset="UTF-8"><title>الملف</title></head><body style="font-family:Arial;padding:20px;">
    <div style="max-width:600px;margin:0 auto;background:#fff;padding:20px;border-radius:8px;">
    <h2>الملف الشخصي</h2>
    <p><strong>الاسم:</strong> {{ username }}</p>
    <p><strong>الدور:</strong> {{ role }}</p>
    <p><strong>الرصيد:</strong> {{ balance }}</p>
    <h3>تخصيص التحية:</h3>
    <form method="POST"><input name="greeting" placeholder="أدخل تحية..." style="width:100%;padding:8px;margin-bottom:8px;"><button type="submit">حفظ</button></form>
    <p><a href="/dashboard">رجوع</a></p>
    </div></body></html>
    """, username=session.get('username','مستخدم'), role=session.get('role','user'), balance=session.get('balance',0))

@app.route('/admin')
@login_required
@admin_required
def admin_panel():
    return render_template_string("""
    <html dir="rtl"><head><meta charset="UTF-8"><title>لوحة الأدمن</title></head><body style="font-family:Arial;padding:20px;">
    <div style="max-width:800px;margin:0 auto;background:#fff;padding:20px;border-radius:8px;">
    <h1>لوحة الأدمن</h1>
    <div style="margin-top:12px;">
        <p>وارد استيراد إعدادات النظام (محدد للمسؤولين فقط).</p>
        <form method="POST" action="/admin/import" enctype="multipart/form-data">
            <input type="file" name="config" accept=".pkl"><button type="submit">استيراد</button>
        </form>
    </div>
    <div style="margin-top:12px;">
        <form method="POST" action="/admin/import_b64">
            <textarea name="config_b64" style="width:100%;height:120px;" placeholder="ضع محتوى Base64 هنا"></textarea><button type="submit">استيراد Base64</button>
        </form>
    </div>
    <p><a href="/dashboard">رجوع</a></p>
    </div></body></html>
    """)

@app.route('/admin/import', methods=['POST'])
@login_required
@admin_required
def admin_import():
    if 'config' in request.files:
        file = request.files['config']
        try:
            config = pickle.loads(file.read())
            # show only type and keys to avoid revealing internal secrets
            summary = {"type": type(config).__name__}
            try:
                if hasattr(config, "keys"):
                    summary["keys"] = list(config.keys())[:10]
            except Exception:
                pass
            return render_template_string("<pre>{{ summary }}</pre><p><a href='/admin'>رجوع</a></p>", summary=summary)
        except Exception as e:
            return render_template_string("<h3>خطأ في الاستيراد</h3><pre>{{ err }}</pre><p><a href='/admin'>رجوع</a></p>", err=str(e))
    return redirect(url_for('admin_panel'))

@app.route('/admin/import_b64', methods=['POST'])
@login_required
@admin_required
def admin_import_b64():
    config_b64 = request.form.get('config_b64', '')
    try:
        config_data = base64.b64decode(config_b64)
        config = pickle.loads(config_data)
        summary = {"type": type(config).__name__}
        try:
            if hasattr(config, "keys"):
                summary["keys"] = list(config.keys())[:10]
        except Exception:
            pass
        return render_template_string("<pre>{{ summary }}</pre><p><a href='/admin'>رجوع</a></p>", summary=summary)
    except Exception as e:
        return render_template_string("<h3>خطأ في الاستيراد</h3><pre>{{ err }}</pre><p><a href='/admin'>رجوع</a></p>", err=str(e))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    # run on the same port for your environment
    app.run(host='0.0.0.0', port=31350, debug=False)
