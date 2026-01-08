import sqlite3
from .manager import manager_menu
from src.utils.config import clear_screen, pause
from src.core.Class import Teacher
from src.core.Schedule_System import Schedule_System
from src.core.User_System import load_courses_data, query_classroom_schedule
from src.core.time_date_clean import get_time
from src.core.Classroom_System import print_all_buildings_summary, query_building_by_id, build_tree
from src.models.crud import (
get_connection, activate_teacher_status,
new_teacher_password)

def teacher_active():
    id = input("请输入账号: ")
    password_input = input("请输入密码: ")
    pause()
    clear_screen()
    activate_teacher_status(id, password_input)
    return

def teacher_log_in():
    id = input("请输入账号: ")
    password_input = input("请输入密码: ")
    pause()
    clear_screen()
    
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
                pause()
                return
            
            if password == password_input:
                print("密码正确，登录成功！\n")
                pause()
                teacher = Teacher(row[0], row[1], row[2], row[3])
                root = build_tree()
                time = get_time()
                teacher_menu(teacher, root, time)
            
        else:
            print("登录失败：账号不存在")
            pause()
            return
        
def show_teacher(teacher, time):
    """展示学生信息"""
    while True:
        print(f"\n======== 欢迎 {teacher.name} ========")
        print(f"当前用户: {teacher.id} | 班级: {teacher.class_id}")
        print("1. 显示课程信息")
        print("2. 显示社团信息")
        print("0. 返回\n")

        choice = input("请选择功能: ")
        
        if choice == "1":
            print("已选择：1. 显示课程信息")
            pause()
            clear_screen()
            show_courses(teacher, time)

        elif choice == "2":
            print("\n功能正在开发中...")
            pause()
            clear_screen()

        elif choice == "0":
            print("\n返回上一步。")
            pause()
            clear_screen()
            return

        else:
            print("\n输入无效。")
            pause()
            clear_screen()

def show_courses(teacher, time):
    """展示所选课程"""
    while True:
        print(f"\n======== 欢迎 {teacher.name} ========")
        print(f"当前用户: {teacher.id} | 班级: {teacher.class_id}\n")

        load_courses_data(0, teacher.id, time.semester_id)

        choice = input("输入'0'返回: ")

        if choice == "0":
            print("\n返回上一步。")
            pause()
            clear_screen()
            return

        else:
            print("\n输入无效。")
            pause()
            clear_screen()

def reserve_classroom(teacher, root, time):
    while True:
        print(f"当前用户: {teacher.id}")
        print("1. 查看教室")
        print("2. 预约教室")
        print("0. 返回")

        choice = input("请选择功能: ")

        if choice == "1":
            print("已选择：1. 查看教室")
            pause()
            clear_screen()
            print_all_buildings_summary(root)
            query_building_by_id(root)
            print("返回")
            pause()
            clear_screen()

        elif choice == "2":
            print("已选择：2. 预约教室")
            pause()
            clear_screen()
            c_id = input("请输入像查找的教室ID：")
            query_classroom_schedule(c_id)

        else:
            print("\n输入无效。")
            pause()
            clear_screen()
        
def teacher_menu(teacher, root, time):
    """登录成功后的教师菜单"""
    while True:
        print(f"\n======== 欢迎 {teacher.name} ========")
        print(f"当前用户: {teacher.id}")
        print("1. 查看信息")
        print("2. 修改密码")
        print("3. 预约管理")
        print("0. 退出登录")
        
        choice = input("请选择功能: ")
        
        if choice == "1":
            print("已选择：1. 查看信息")
            pause()
            clear_screen()
            show_teacher(teacher, time)

        elif choice == "2":
            print("已选择：2. 修改密码")
            pause()
            clear_screen()
            new_teacher_password()

        elif choice == "3":
            print("已选择：3. 预约管理")
            pause()
            clear_screen()
            reserve_classroom(teacher, root, time)

        elif choice == "0":
            print("\n已退出。")
            pause()
            clear_screen()
            break

        else:
            print("\n输入无效。")
            pause()
            clear_screen()