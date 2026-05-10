from flask import Flask, render_template_string, request, redirect, session, url_for

app = Flask(__name__)
app.secret_key = "norinim_secret_2026"

# 🛡️ O'CHMAS OWNER AKKAUNTI
OWNER_USER = "SuperAdmin_2026"
OWNER_PASS = "X7_vB9!zR2@pQw99_Owner"

# Ma'lumotlar bazasi (Vaqtinchalik xotira)
db = {
    "users": {},
    "sections": ["O'qituvchilar", "O'quvchilar", "Bilimdonlar", "Yangiliklar", "Ma'muriyat", "Kutubxona"]
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Norinim Tizimi</title>
    <style>
        body { background: #0f172a; color: white; font-family: sans-serif; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; }
        .card { background: #1e293b; padding: 40px; border-radius: 25px; width: 100%; max-width: 450px; box-shadow: 0 20px 40px rgba(0,0,0,0.4); text-align: center; }
        input { width: 100%; padding: 15px; margin: 10px 0; border-radius: 12px; border: 1px solid #334155; background: #0f172a; color: white; box-sizing: border-box; font-size: 16px; }
        button { width: 100%; padding: 15px; margin: 10px 0; border-radius: 12px; border: none; font-size: 18px; font-weight: bold; cursor: pointer; transition: 0.3s; }
        .btn-blue { background: #38bdf8; color: #0f172a; }
        .btn-menu { background: #334155; color: white; text-align: left; padding-left: 20px; margin: 5px 0; }
        .btn-menu:hover { background: #38bdf8; color: #0f172a; }
        .badge { background: #fbbf24; color: black; padding: 5px 10px; border-radius: 8px; font-size: 12px; font-weight: bold; }
    </style>
</head>
<body>
    <div class="card">
        {% if 'user' not in session %}
            <h2>Tizimga Kirish</h2>
            <form method="POST" action="/login">
                <input name="u" placeholder="Login" required>
                <input name="p" type="password" placeholder="Parol" required>
                <button type="submit" name="action" value="login" class="btn-blue">Kirish</button>
                <button type="submit" name="action" value="reg" style="background:transparent; border:1px solid #22c55e; color:#22c55e;">Ro'yxatdan o'tish</button>
            </form>
            {% if error %}<p style="color:#ef4444">{{ error }}</p>{% endif %}
        {% else %}
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <h3>Salom, {{ session.user }}</h3>
                <span class="badge">{{ session.role.upper() }}</span>
            </div>
            <hr style="opacity:0.1; margin: 20px 0;">
            {% for s in sections %}
                <button class="btn-menu" onclick="alert('{{ s }} bo\\'limi tez kunda...')">{{ loop.index }}. {{ s }}</button>
            {% endfor %}
            
            {% if session.role == 'owner' %}
                <button style="background:#ef4444; color:white; margin-top:20px;" onclick="alert('Baza tozalandi!')">💥 Bazani tozalash</button>
            {% endif %}
            <a href="/logout" style="color:#94a3b8; text-decoration:none; display:block; margin-top:20px;">Chiqish</a>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, sections=db["sections"])

@app.route('/login', methods=['POST'])
def login():
    u = request.form.get('u')
    p = request.form.get('p')
    action = request.form.get('action')

    if action == "reg":
        if u == OWNER_USER: return "Taqiqlangan login!"
        db["users"][u] = {"pass": p, "role": "viewer"}
        return redirect(url_for('index'))

    if u == OWNER_USER and p == OWNER_PASS:
        session['user'], session['role'] = u, "owner"
    elif db["users"].get(u) and db["users"][u]["pass"] == p:
        session['user'], session['role'] = u, db["users"][u]["role"]
    
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
