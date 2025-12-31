import sqlite3

conn = sqlite3.connect('database.db')
cur = conn.cursor()

cur.execute("SELECT COUNT(*) FROM questions")
total = cur.fetchone()[0]
print(f"Total questions: {total}")

# Example counts by grade/subject
cur.execute("SELECT grade, subject, COUNT(*) FROM questions GROUP BY grade, subject")
for row in cur.fetchall():
    print(f"Grade {row[0]}, Subject {row[1]}: {row[2]} questions")

conn.close()
