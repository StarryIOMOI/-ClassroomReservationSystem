import sqlite3
from core import Teacher
from models import get_connection
from utils import clear_screen
from utils import pause
from .manager import manager_menu

def teacher_log_in(id, password_input):
    if id == '0' and password_input == '0':
        manager_menu()
    else:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM teacher_users 
            WHERE teacher_id = ?
        """, (id,))

        row = cursor.fetchone()
        conn.close()

        password = row[2]
        status = row[0]

        if row:
            if status == 0:
                print("账号未激活！请先激活账号")
                return None
            
            if password == password_input:
                print("密码正确，登录成功！\n")
                teacher = Teacher(row[0], row[1], row[2], row[3], row[4])
                teacher_menu(teacher)
            
        else:
            print("登录失败：账号不存在")
            return None
        
def teacher_menu(teacher):
    """登录成功后的学生菜单"""
    while True:
        print(f"\n======== 欢迎 {teacher.name} ========")
        print(f"当前用户: {teacher.id}")
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
            print("\n已退出。")
            pause()
            break

        else:
            print("\n输入无效。")
            pause()