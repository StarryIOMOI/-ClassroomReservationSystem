import sqlite3
from core import Teacher
from core import load_courses_data
from models import get_connection
from utils import clear_screen
from utils import pause
from .manager import manager_menu

def teacher_log_in(id, password_input):
    if id == '0' and password_input == '0':
        manager_menu()
    else:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM teacher_users 
            WHERE teacher_id = ?
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
                teacher = Teacher(row[0], row[1], row[2], row[3], row[4])
                teacher_menu(teacher)
            
        else:
            print("登录失败：账号不存在")
            return None
        
def show_teacher(teacher):
    """展示学生信息"""
    while True:
        print(f"\n======== 欢迎 {teacher.name} ========")
        print(f"当前用户: {teacher.id} | 班级: {teacher.class_id}")
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

def show_courses(teacher):
    """展示所选课程"""
    while True:
        print(f"\n======== 欢迎 {teacher.name} ========")
        print(f"当前用户: {teacher.id} | 班级: {teacher.class_id}\n")

        load_courses_data(0, teacher.id)

        choice = input("输入'0'返回: ")

        if choice == "0":
            print("\n返回上一步。")
            pause()
            return

        else:
            print("\n输入无效。")
            pause()

def reserve_classroom():
    
        
def teacher_menu(teacher):
    """登录成功后的学生菜单"""
    while True:
        print(f"\n======== 欢迎 {teacher.name} ========")
        print(f"当前用户: {teacher.id}")
        print("1. 查看信息")
        print("2. 修改密码")
        print("3. 预约教室")
        print("0. 退出登录")
        
        choice = input("请选择功能: ")
        
        if choice == "1":
            print("\n功能正在开发中...")
            pause()

        elif choice == "2":
            print("\n功能正在开发中...")
            pause()

        elif choice == "0":
            print("\n已退出。")
            pause()
            break

        else:
            print("\n输入无效。")
            pause()