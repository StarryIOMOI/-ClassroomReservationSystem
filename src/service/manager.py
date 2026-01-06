import sqlite3, sys
from core import (add_building, add_area, add_floor, add_classroom,
                  add_teacher, add_student, add_class, add_semester,
                  add_course)
from models import get_connection
from utils import clear_screen, pause

def manager_menu():
    while True:
        print("\n======== 管理员 0 ========")
        print("1. 教室管理")
        print("2. 用户管理")
        print("3. 课程管理")
        print("0. 退出")
        
        choice = input("请选择功能: ")
        
        if choice == "1":
            print("已选择：1. 教室管理")
            pause()
            clear_screen()
            classrooms()

        elif choice == "2":
            print("\n已选择：2. 用户管理")
            pause()
            clear_screen()
            users()

        elif choice == "3":
            print("\n功能正在开发中...")
            pause()
            clear_screen()

        elif choice == "0":
            print("\n退出")
            pause()
            clear_screen()
            return

        else:
            print("\n输入无效。")
            pause()
            clear_screen()

def classrooms():
    while True:
        print("\n======== 管理员 0 ========")
        print("1. 添加教室")
        print("2. 管理教室")
        print("0. 返回")

        choice = input("请选择功能: ")

        if choice == "1":
            print("\n已选择：1. 添加教室")
            pause()
            clear_screen()
            add_classrooms()

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

def users():
    while True:
        print("\n======== 管理员 0 ========")
        print("1. 添加用户")
        print("2. 重置密码")
        print("0. 返回")

        choice = input("请选择功能: ")

        if choice == "1":
            print("\n已选择：1. 添加用户")
            pause()
            clear_screen()
            add_user()

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

def courses():
    while True:
        print("\n======== 管理员 0 ========")
        print("1. 添加学期")
        print("2. 添加课程")
        print("0. 返回")

        choice = input("请选择功能: ")

        if choice == "1":
            print("\n已选择：1. 添加学期")
            pause()
            clear_screen()
            add_semester()

        if choice == "2":
            print("\n已选择：2. 添加课程")
            pause()
            clear_screen()
            add_course()

        elif choice == "0":
            print("\n返回上一步。")
            pause()
            clear_screen()
            return

        else:
            print("\n输入无效。")
            pause()
            clear_screen()

def add_classrooms():
    while True:
        print("\n======== 添加教室 ========")
        print("1. 添加教学楼")
        print("2. 添加区域")
        print("3. 添加楼层")
        print("4. 添加教室")
        print("0. 返回")

        choice = input("请选择功能: ")

        if choice == "1":
            print("\n已选择：1. 添加教学楼")
            pause()
            clear_screen()
            add_building()

        elif choice == "2":
            print("\n已选择：2. 添加区域")
            pause()
            clear_screen()
            add_area()

        elif choice == "3":
            print("\n已选择：3. 添加楼层")
            pause()
            clear_screen()
            add_floor

        elif choice == "4":
            print("\n已选择：4. 添加教室")
            pause()
            clear_screen()
            add_classroom

        elif choice == "0":
            print("\n返回上一步。")
            pause()
            clear_screen()
            return

        else:
            print("\n输入无效。")
            pause()
            clear_screen()

def modify_classrooms():
    while True:
        print("\n======== 教室管理 ========")
        print("1. 管理教学楼")
        print("2. 管理区域")
        print("3. 管理楼层")
        print("4. 管理教室")
        print("0. 返回")

        choice = input("请选择功能: ")

        if choice == "1":
            print("\n已选择：1. 管理教学楼")
            pause()
            clear_screen()
            add_building()

        elif choice == "2":
            print("\n已选择：2. 管理区域")
            pause()
            clear_screen()
            add_area()

        elif choice == "3":
            print("\n已选择：3. 管理楼层")
            pause()
            clear_screen()
            add_floor()

        elif choice == "4":
            print("\n已选择：4. 管理教室")
            pause()
            clear_screen()
            add_classroom()

        elif choice == "0":
            print("\n返回上一步。")
            pause()
            clear_screen()
            return

        else:
            print("\n输入无效。")
            pause()
            clear_screen()

def add_user():
    while True:
        print("\n======== 添加用户 ========")
        print("1. 添加教师")
        print("2. 添加学生")
        print("3. 添加院系")
        print("4. 添加班级")
        print("0. 返回")

        choice = input("请选择功能: ")

        if choice == "1":
            print("\n已选择：1. 添加教师")
            pause()
            clear_screen()
            add_teacher()

        elif choice == "2":
            print("\n已选择：2. 添加学生")
            pause()
            clear_screen()
            add_student

        elif choice == "3":
            print("\n已选择：3. 添加班级")
            pause()
            clear_screen()
            add_class

        elif choice == "4":
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