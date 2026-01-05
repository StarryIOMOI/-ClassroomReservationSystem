import sys
from src.service import student_log_in, teacher_log_in, student_menu, teacher_menu
from src.core import build_tree, get_time
from src.utils import clear_screen, pause
    
def log_in():
    """登录"""
    while True:
        print(f"\n======== 登录/激活 ========\n")
        print("1. 教师登录")
        print("2. 学生登录")
        print("0. 退出登录")
        
        choice = input("请选择功能: ")
        
        if choice == "1":
            print(f"\n======== 教师登录 ========")
            id = input("请输入账号: ")
            password = input("请输入密码: ")
            pause()
            teacher = teacher_log_in(id, password)
            root = build_tree()
            time = get_time()
            teacher_menu(teacher, root, time)

        elif choice == "2":
            print(f"\n======== 学生登录 ========")
            id = input("请输入账号: ")
            password = input("请输入密码: ")
            pause()
            student = student_log_in(id, password)
            root = build_tree()
            time = get_time()
            student_menu(student, root, time)

        elif choice == "0":
            print("退出。")
            sys.exit(0)

        else:
            print("输入无效。")
            pause()

if __name__ == '__main__':
    log_in()