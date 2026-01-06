import sqlite3, sys
from core import add_building, add_area, add_floor, add_classroom
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
            classrooms()

        elif choice == "2":
            print("\n功能正在开发中...")
            pause()

        elif choice == "3":
            print("\n功能正在开发中...")
            pause()

        elif choice == "0":
            print("\n退出")
            pause()
            sys.exit(0)

        else:
            print("\n输入无效。")
            pause()

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
            add_classrooms()

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

def users():
    while True:
        print("\n======== 管理员 0 ========")
        print("1. 添加用户")
        print("2. 重置密码")
        print("0. 返回")

        choice = input("请选择功能: ")

        if choice == "1":
            print("\n功能正在开发中...")
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

def courses():
    while True:
        print("\n======== 管理员 0 ========")
        print("1. 添加学期")
        print("2. 添加课程")
        print("0. 返回")

        choice = input("请选择功能: ")

        if choice == "1":
            print("\n功能正在开发中...")
            pause()

        elif choice == "0":
            print("\n返回上一步。")
            pause()
            return

        else:
            print("\n输入无效。")
            pause()

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
            add_building()

        elif choice == "2":
            print("\n已选择：2. 添加区域")
            pause()

        elif choice == "3":
            print("\n已选择：3. 添加楼层")
            pause()

        elif choice == "4":
            print("\n已选择：4. 添加教室")
            pause()

        elif choice == "0":
            print("\n返回上一步。")
            pause()
            return

        else:
            print("\n输入无效。")
            pause()

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
            add_building()

        elif choice == "2":
            print("\n已选择：2. 管理区域")
            pause()
            add_area()

        elif choice == "3":
            print("\n已选择：3. 管理楼层")
            pause()
            add_floor()

        elif choice == "4":
            print("\n已选择：4. 管理教室")
            pause()
            add_classroom()

        elif choice == "0":
            print("\n返回上一步。")
            pause()
            return

        else:
            print("\n输入无效。")
            pause()