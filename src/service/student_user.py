import sqlite3
from core import Student
from core import load_courses_data
from models import get_connection
from utils import clear_screen
from utils import pause

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
            student = Student(row[0], row[1], row[2], row[3], row[4])
            student_menu(student)
        
    else:
        print("登录失败：学号不存在")
        return None
    
def student_menu(student):
    """登录成功后的学生菜单"""
    while True:
        print(f"\n======== 欢迎 {student.name} ========")
        print(f"当前用户: {student.id} | 班级: {student.class_id}")
        print("1. 查看我的信息\n")
        print("2. 修改密码\n")
        print("3. 预约教室\n")
        print("0. 退出登录\n")
        
        choice = input("请选择功能: ")
        
        if choice == "1":
            show_student()
            pause()

        elif choice == "2":
            print("\n密码修改功能开发中...")
            pause()

        elif choice == "0":
            print("\n已退出。")
            pause()
            break

        else:
            print("\n输入无效。")
            pause()

def show_student(student):
    """展示学生信息"""
    while True:
        print(f"\n======== 欢迎 {student.name} ========")
        print(f"当前用户: {student.id} | 班级: {student.class_id}")
        print("1. 显示课程信息\n")
        print("2. 显示社团信息\n")
        print("0. 返回\n")

        choice = input("请选择功能: ")
        
        if choice == "1":
            show_courses()
            pause()

        elif choice == "2":
            print("\n功能正在开发中...")
            pause()

        elif choice == "0":
            print("\n返回上一步。")
            pause()
            return

        else:
            print("\n输入无效。")
            pause()

def show_courses(student):
    """展示所选课程"""
    while True:
        print(f"\n======== 欢迎 {student.name} ========")
        print(f"当前用户: {student.id} | 班级: {student.class_id}\n")

        load_courses_data(student.class_id, 0)

        choice = input("输入'0'返回: ")

        if choice == "0":
            print("\n返回上一步。")
            pause()
            return

        else:
            print("\n输入无效。")
            pause()