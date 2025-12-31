from flask import Flask, render_template, request, redirect, session
import sqlite3
import random
import os

app = Flask(__name__)
app.secret_key = 'eliteprep_final_secure_key_2025'

DEFAULT_GRADE = 5
DEFAULT_SUBJECT = "Math"
DEFAULT_NUM_QUESTIONS = 5
DB_PATH = 'database.db'

def safe_db_connect():
    if not os.path.exists(DB_PATH):
        return None
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except:
        return None
    finally:
        if conn:
            try:
                conn.close()
            except:
                pass

@app.errorhandler(Exception)
def handle_error(e):
    return render_template('error.html', message="A small issue occurred. Try again!"), 200

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_test', methods=['POST'])
def start_test():
    try:
        grade = DEFAULT_GRADE
        subject = DEFAULT_SUBJECT
        num_questions = DEFAULT_NUM_QUESTIONS

        # Safe URL params
        try:
            g = request.args.get('grade')
            if g: grade = max(5, min(12, int(g)))
        except: pass
        s = request.args.get('subject')
        if s: subject = s.strip()
        try:
            n = request.args.get('num_questions')
            if n: num_questions = max(1, min(20, int(n)))
        except: pass

        conn = safe_db_connect()
        if not conn:
            return render_template('error.html', message="No questions loaded. Run import first."), 200

        cur = conn.cursor()
        ids = []
        try:
            cur.execute("SELECT id FROM questions WHERE grade = ? AND subject = ?", (grade, subject))
            rows = cur.fetchall()
            ids = [row['id'] for row in rows]

            if not ids:
                cur.execute("SELECT id FROM questions")
                rows = cur.fetchall()
                ids = [row['id'] for row in rows]

            if not ids:
                conn.close()
                return render_template('error.html', message="No questions in database."), 200

            selected = random.sample(ids, min(num_questions, len(ids)))

            session.clear()
            session['question_ids'] = selected
            session['current_index'] = 0
            session['answers'] = {}
            session['total'] = len(selected)
        finally:
            conn.close()

        return redirect('/question')
    except:
        return render_template('error.html', message="Couldn't start test."), 200

@app.route('/question', methods=['GET', 'POST'])
def question():
    try:
        if 'question_ids' not in session or not session['question_ids']:
            return redirect('/')

        index = session.get('current_index', 0)
        total = session['total']
        if index >= total:
            return redirect('/result')

        q_id = session['question_ids'][index]

        conn = safe_db_connect()
        if not conn:
            return redirect('/result')

        cur = conn.cursor()
        cur.execute("SELECT * FROM questions WHERE id = ?", (q_id,))
        q = cur.fetchone()
        conn.close()

        if not q:
            session['current_index'] = index + 1
            return redirect('/question')

        if request.method == 'POST':
            answer = request.form.get('answer')
            if answer:
                session['answers'][str(index)] = answer
            session['current_index'] = index + 1
            return redirect('/question')

        return render_template('question.html',
                               question_num=index + 1,
                               total_questions=total,
                               question_text=q['question'],
                               a=q['option_a'],
                               b=q['option_b'],
                               c=q['option_c'],
                               d=q['option_d'])
    except:
        return redirect('/result')

@app.route('/result')
def result():
    try:
        # Always show result even if something minor fails
        score = 0
        total = session.get('total', 0)
        if total == 0:
            session.clear()
            return render_template('result.html', score=0, total=0)

        q_ids = session.get('question_ids', [])
        user_answers = session.get('answers', {})

        conn = safe_db_connect()
        if conn:
            cur = conn.cursor()
            try:
                for i in range(total):
                    user_ans = user_answers.get(str(i))
                                    if user_ans:  # Only check if user answered
                    try:
                        cur.execute("SELECT correct_answer FROM questions WHERE id = ?", (q_ids[i],))
                        row = cur.fetchone()
                        if row and user_ans == row['correct_answer']:
                            score += 1
                    except:
                        pass  # Skip any DB error for this question, don't add to score
            finally:
                try:
                    conn.close()
                except:
                    pass

        session.clear()
        return render_template('result.html', score=score, total=total)

    except:
        total = session.get('total', 0)
        session.clear()
        return render_template('result.html', score=0, total=total)
