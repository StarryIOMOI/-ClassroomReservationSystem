import sqlite3
from core import Student
from models import get_connection

def student_log_in(id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM courses 
        WHERE student_id = ?
    """, (id))

    row = cursor.fetchone()
    conn.close()

    if row:
        print(f"登录成功！欢迎 {row[3]}")
        return Student(row[0], row[1], row[2], row[3], row[4])
    else:
        print("登录失败：学号不存在")
        return None

