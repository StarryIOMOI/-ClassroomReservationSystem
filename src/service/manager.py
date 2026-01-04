import sqlite3
from models import get_connection
from utils import clear_screen
from utils import pause

def manager_menu():
    """登录成功后的学生菜单"""
    while True:
        print(f"\n======== 管理员 0 ========")
        print("1. 教室管理")
        print("2. 用户管理")
        print("3. 课程管理")
        print("0. 退出登录")
        
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
            print("\n退出。")
            pause()
            break

        else:
            print("\n输入无效。")
            pause()