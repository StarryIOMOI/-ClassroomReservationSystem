import sqlite3
from core import Student
from models import get_connection

def student_log_in(id, password_input):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM student_users
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
            print(f"欢迎回家！博士 {row[3]}\n")
            return Student(row[0], row[1], row[2], row[3], row[4])
        
    else:
        print("登录失败：学号不存在")
        return None
    
def show_student_menu(student):
    """登录成功后的学生菜单"""
    while True:
        print(f"\n======== 欢迎 {student.name} ========")
        print(f"当前用户: {student.id} | 班级: {student.class_id}")
        print("1. 查看我的信息")
        print("2. 修改密码")
        print("3. 查看教室")
        print("0. 退出登录")
        
        choice = input("请选择功能: ")
        
        if choice == "1":
            print(f"姓名: {student.name}")
            print(f"状态: {student.status}")
        
        elif choice == "2":
            print("密码修改功能开发中...")
            
        elif choice == "0":
            print("已退出。")
            break

        else:
            print("输入无效。")
