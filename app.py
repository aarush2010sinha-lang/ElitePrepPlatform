from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3
import os

# Tell Flask to look in root folder for templates (your current setup)
app = Flask(__name__, template_folder='.')

app.secret_key = 'your-secret-key-change-this-in-production'

DATABASE = 'database.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        return redirect(url_for('result'))

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute("SELECT id, question_text, option_a, option_b, option_c, option_d FROM questions ORDER BY RANDOM() LIMIT 10")
        questions = cur.fetchall()
        q_ids = [str(q['id']) for q in questions]
    finally:
        cur.close()
        conn.close()

    return render_template('question.html',
                           questions=questions,
                           q_ids=q_ids,
                           total=len(questions),
                           enumerate=enumerate)

@app.route('/result', methods=['POST'])
def result():
    score = 0
    total = int(request.form.get('total', 0))
    q_ids = request.form.getlist('q_ids')

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        for i in range(total):
            user_ans = request.form.get(str(i))
            if user_ans:
                try:
                    cur.execute("SELECT correct_answer FROM questions WHERE id = ?", (q_ids[i],))
                    row = cur.fetchone()
                    if row and user_ans.strip().lower() == row['correct_answer'].strip().lower():
                        score += 1
                except:
                    pass
    finally:
        cur.close()
        conn.close()

    session.clear()
    return render_template('result.html', score=score, total=total)

# This is the key fix for Render
if __name__ == '__main__':
    # Local development: run on localhost:5000 with debug
    app.run(host='127.0.0.1', port=5000, debug=True)
else:
    # On Render: use the PORT env var and bind to 0.0.0.0
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
    from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os

# Add your existing imports if any (e.g., from check_db.py, etc.)
# from check_db import something  # keep your imports

app = Flask(__name__)
app.secret_key = "your_secret_key"  # change this to something random

# Your existing routes (KEEP ALL OF THEM UNCHANGED)
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/analytical")
def analytical():
    return render_template("analytical.html")

# Add ALL your other existing routes here exactly as they are
# Examples (replace with your actual ones):
# @app.route("/some_route")
# def some_function():
#     ...

@app.errorhandler(404)
def page_not_found(e):
    return render_template("error.html"), 404

# === THIS IS THE ONLY NEW PART FOR RENDER.COM ===
if __name__ == "__main__":
    # This makes it work on Render (binds to 0.0.0.0 and uses $PORT)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)  # debug=False recommended for production
# ================================================


