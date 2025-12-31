import sqlite3, os

DB_PATH = os.path.join(os.path.dirname(__file__), "database.db")
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

questions = [
(8,"Science","Force",1,"SI unit of force?","Newton","Joule","Pascal","Watt","A"),
(8,"Math","Integers",1,"-3 + 5 = ?","2","-2","8","-8","A"),
(9,"Math","Triangles",1,"Sum of angles of triangle?","90","180","270","360","B"),
(9,"Science","Motion",1,"Unit of velocity?","m/s","m/s²","kg","m","A"),
(10,"Math","Quadratic",1,"Roots of x² = 4?","±2","±4","0","1","A"),
(12,"Physics","Kinematics",2,"Slope of v-t graph gives?","Speed","Velocity","Acceleration","Distance","C")
]

cur.executemany("""
INSERT INTO questions
(grade,subject,chapter,difficulty,question,option_a,option_b,option_c,option_d,correct_option)
VALUES (?,?,?,?,?,?,?,?,?,?)
""", questions)

conn.commit()
conn.close()
print("✅ Questions inserted successfully")
