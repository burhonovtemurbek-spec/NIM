from flask import Flask, render_template_string, request, redirect, session
import os

app = Flask(__name__)
app.secret_key = "maktab_secret_key"

# Ma'lumotlarni kod ichida saqlaymiz
db = {
    "users": {},
    "teachers": [], "students": [], "news": [],
    "settings": {"bg": "https://images.unsplash.com/photo-1523050853063-bd8012fec21b"}
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Maktab Tizimi</title>
    <style>
        body { background: url('{{ db.settings.bg }}') no-repeat center; background-size: cover; color: white; font-family: sans-serif; }
        .box { background: rgba(0,0,0,0.8); padding: 20px; max-width: 500px; margin: 50px auto; border-radius: 10px; text-align: center; }
        .btn { display: block; background: #3498db; color: white; padding: 10px; margin: 10px 0; text-decoration: none; border-radius: 5px; }
        input { width: 90%; padding: 10px; margin: 10px 0; }
    </style>
</head>
<body>
    <div class="box">
        {% if 'user' not in session %}
            <h2>Kirish / Ro'yxatdan o'tish</h2>
            <form method="post" action="/login">
                <input name="user" placeholder="Login" required><br>
                <input name="pw" type="password" placeholder="Parol" required><br>
                <button name="action" value="in" class="btn" style="width:100%">Kirish</button>
                <button name="action" value="up" class="btn" style="width:100%; background:green">Ro'yxatdan o'tish</button>
            </form>
        {% else %}
            <h1>Assalomu alaykum, {{ session.user }}!</h1>
            <p>Sizning rolingiz: {{ session.role }}</p>
            <a href="/section/teachers" class="btn">O'qituvchilar</a>
            <a href="/section/news" class="btn">Yangiliklar</a>
            <a href="/logout" class="btn" style="background:red">Chiqish</a>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, db=db)

@app.route('/login', methods=['POST'])
def login():
    user = request.form['user']
    pw = request.form['pw']
    action = request.form['action']
    if action == "up":
        role = "super-admin" if not db['users'] else "viewer"
        db['users'][user] = {"pw": pw, "role": role}
    if db['users'].get(user, {}).get('pw') == pw:
        session['user'] = user
        session['role'] = db['users'][user]['role']
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# Vercel uchun interface
def handler(request):
    return app(request)
