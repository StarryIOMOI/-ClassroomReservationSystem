from src import student_log_in
from src import teacher_log_in

def log_in():
    """登录"""
    while True:
        print(f"\n======== 登录/激活 ========\n")
        print("1. 教师登录")
        print("2. 学生登录")
        print("3. 退出登录")
        
        choice = input("请选择功能: ")
        
        if choice == "1":
            print(f"\n======== 教师登录 ========\n")
            id = input("\n请输入账号: ")
            password = input("\n请输入密码: ")
            teacher = teacher_log_in(id, password)

        elif choice == "2":
            print(f"\n======== 学生登录 ========\n")
            id = input("\n请输入账号: ")
            password = input("\n请输入密码: ")
            student = student_log_in(id, password)

        elif choice == "3":
            print("已退出。")
            break

        else:
            print("输入无效。")

if __name__ == '__main__':
    log_in