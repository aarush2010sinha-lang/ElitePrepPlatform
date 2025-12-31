import sqlite3
import csv
import os

DB_PATH = 'database.db'

conn = None
try:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT,
        option_a TEXT,
        option_b TEXT,
        option_c TEXT,
        option_d TEXT,
        correct_answer TEXT,
        grade INTEGER,
        subject TEXT
    )
    ''')

    if os.path.exists('questions.csv'):
        with open('questions.csv', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['question'].strip():  # Skip empty
                    cur.execute("SELECT 1 FROM questions WHERE question = ?", (row['question'],))
                    if not cur.fetchone():
                        cur.execute('''
                        INSERT INTO questions (question, option_a, option_b, option_c, option_d, correct_answer, grade, subject)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (row['question'], row['option_a'], row['option_b'], row['option_c'], row['option_d'], row['correct_answer'], int(row.get('grade', 5)), row.get('subject', 'Math')))
    conn.commit()
    print("Import successful! Questions loaded.")
except Exception as e:
    print(f"Import error: {e}")
finally:
    if conn:
        conn.close()