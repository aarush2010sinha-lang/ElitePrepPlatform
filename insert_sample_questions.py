import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")

questions = [
    ("9", "Math", "Algebra", 1,
     "What is 2x + 3 = 7?",
     "x = 1", "x = 2", "x = 3", "x = 4", "B"),

    ("9", "Math", "Algebra", 2,
     "Solve: x² = 16",
     "2", "-4", "4", "±4", "D"),

    ("8", "Science", "Physics", 1,
     "Unit of force?",
     "Joule", "Newton", "Watt", "Pascal", "B"),

    ("8", "Science", "Chemistry", 1,
     "Water chemical formula?",
     "CO2", "H2", "H2O", "O2", "C")
]

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.executemany("""
INSERT INTO questions
(grade, subject, chapter, difficulty, question,
 option_a, option_b, option_c, option_d, correct_option)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", questions)

conn.commit()
conn.close()

print("✅ Sample questions inserted successfully")
