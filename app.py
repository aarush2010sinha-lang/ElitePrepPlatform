from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-in-production'  # Keep or change this

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
        q_ids = [str(q['id']) for q in questions]  # Convert to strings for form
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
            user_ans = request.form.get(str(i))  # name="0", "1", etc. in your form
            if user_ans:  # Only check if user actually selected an answer
                try:
                    cur.execute("SELECT correct_answer FROM questions WHERE id = ?", (q_ids[i],))
                    row = cur.fetchone()
                    if row and user_ans.strip().lower() == row['correct_answer'].strip().lower():
                        score += 1
                except:
                    pass  # Skip any error for this question
    finally:
        cur.close()
        conn.close()

    session.clear()
    return render_template('result.html', score=score, total=total)

if __name__ == '__main__':
    app.run(debug=True)
