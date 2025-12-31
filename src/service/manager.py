import sqlite3
from models import get_connection
from utils import clear_screen
from utils import pause

def manager_menu():
    """登录成功后的学生菜单"""
    while True:
        print(f"\n======== 管理员 0 ========")
        print("1. 查看我的信息")
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
            print("\n退出。")
            pause()
            break

        else:
            print("\n输入无效。")
            pause()