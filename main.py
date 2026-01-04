from src.service import student_log_in
from src.service import teacher_log_in
from src.utils import clear_screen
from src.utils import pause

def log_in():
    """登录"""
    while True:
        print(f"\n======== 登录/激活 ========\n")
        print("1. 教师登录")
        print("2. 学生登录")
        print("3. 退出登录")
        
        choice = input("请选择功能: ")
        
        if choice == "1":
            print(f"\n======== 教师登录 ========")
            id = input("请输入账号: ")
            password = input("请输入密码: ")
            pause()
            teacher = teacher_log_in(id, password)

        elif choice == "2":
            print(f"\n======== 学生登录 ========")
            id = input("请输入账号: ")
            password = input("请输入密码: ")
            pause()
            student_log_in(id, password)

        elif choice == "3":
            print("退出。")
            break

        else:
            print("输入无效。")
            pause()

if __name__ == '__main__':
    log_in()