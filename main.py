import sys
from src.service.teacher_user import teacher_active,  teacher_log_in
from src.service.student_user import student_active, student_log_in
from src.utils.config import clear_screen, pause
    
def log_in():
    """登录"""
    clear_screen()
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
            pause()

        elif choice == "4":
            pause()
            clear_screen()
            print(f"\n======== 学生激活 ========")
            student_active()
            pause()

        elif choice == "0":
            print("退出。")
            clear_screen()
            sys.exit(0)

        else:
            print("输入无效。")
            pause()
            clear_screen()

if __name__ == '__main__':
    log_in()