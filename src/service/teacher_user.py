import sqlite3
from core import Teacher
from models import get_connection

def teacher_log_in(id, password_input):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM teacher_users 
        WHERE student_id = ?
    """, (id,))

    row = cursor.fetchone()
    conn.close()

    password = row[2]
    status = row[0]

    if row:
        if status == 0:
            print("账号未激活！请先激活账号")
            return None
        
        if password == password_input:
            print("密码正确，登录成功！\n")
            return Teacher(row[0], row[1], row[2], row[3], row[4])
        
    else:
        print("登录失败：学号不存在")
        return None