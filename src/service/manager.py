import sqlite3, sys
from models import get_connection
from utils import clear_screen
from utils import pause

def manager_menu():
    while True:
        print(f"\n======== 管理员 0 ========")
        print("1. 教室管理")
        print("2. 用户管理")
        print("3. 课程管理")
        print("0. 退出")
        
        choice = input("请选择功能: ")
        
        if choice == "1":
            print("\n功能正在开发中...")
            pause()

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
        print(f"\n======== 管理员 0 ========")
        print("1. 添加教学楼")
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

def users():
    while True:
        print(f"\n======== 管理员 0 ========")
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
        print(f"\n======== 管理员 0 ========")
        print("1. 添加课程")
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