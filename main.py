import sys
from src.service import teacher_active, student_active, teacher_log_in, student_log_in
from src.utils import clear_screen, pause
    
def log_in():
    """登录"""
    while True:
        clear_screen()
        print(f"\n======== 登录/激活 ========\n")
        print("1. 教师登录")
        print("2. 学生登录")
        print("3. 教师激活")
        print("4. 学生激活")
        print("0. 退出登录")
        
        choice = input("请选择功能: ")
        
        if choice == "1":
            pause()
            clear_screen()
            print(f"\n======== 教师登录 ========")
            teacher_log_in()

        elif choice == "2":
            pause()
            clear_screen()
            print(f"\n======== 学生登录 ========")
            student_log_in()
        
        elif choice == "3":
            pause()
            clear_screen()
            print(f"\n======== 教师激活 ========")
            teacher_active()

        elif choice == "4":
            pause()
            clear_screen()
            print(f"\n======== 学生激活 ========")
            student_active()

        elif choice == "0":
            print("退出。")
            sys.exit(0)

        else:
            print("输入无效。")
            pause()
            clear_screen()

if __name__ == '__main__':
    log_in()