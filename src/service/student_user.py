import sqlite3
from datetime import datetime
from src.core.Class import Student
from src.core.User_System import load_courses_data, query_classroom_schedule
from src.core.Classroom_System import print_all_buildings_summary, query_building_by_id, build_tree
from src.core.time_date_clean import get_time, MAX_SLOTS_PER_DAY
from src.core.Schedule_System import reserve
from src.models.crud import get_connection, activate_student_status, new_student_password
from src.utils.config import clear_screen, pause

def student_active():
    id = input("请输入账号: ")
    password_input = input("请输入密码: ")
    pause()
    clear_screen()
    clear_screen()
    activate_student_status(id, password_input)
    return

def student_log_in():
    id = input("请输入账号: ")
    password_input = input("请输入密码: ")
    pause()
    clear_screen()
    clear_screen()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM student_users
        WHERE student_id = ?
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
            print(f"欢迎回家！博士 {row[3]}\n")
            student = Student(row[0], row[1], row[2], row[3], row[4])
            root = build_tree()
            time = get_time()
            student_menu(student, root, time)
        else:
            print("ERROR: 密码错误！")
        
    else:
        print("登录失败：学号不存在")
        return None

def show_student(student, time):
    """展示学生信息"""
    while True:
        print(f"\n======== 欢迎 {student.name} ========")
        print(f"当前用户: {student.id} | 班级: {student.class_id}")
        print("1. 显示课程信息\n")
        print("2. 显示社团信息\n")
        print("0. 返回\n")

        choice = input("请选择功能: ")
        
        if choice == "1":
            show_courses(student, time)
            pause()
            clear_screen()

        elif choice == "2":
            print("\n功能正在开发中...")
            pause()
            clear_screen()

        elif choice == "0":
            print("\n返回上一步。")
            pause()
            clear_screen()
            return

        else:
            print("\n输入无效。")
            pause()
            clear_screen()

def show_courses(student, time):
    """展示所选课程"""
    while True:
        print(f"\n======== 欢迎 {student.name} ========")
        print(f"当前用户: {student.id} | 班级: {student.class_id}\n")

        load_courses_data(student.class_id, 0, time.semester_id)

        choice = input("输入'0'返回: ")

        if choice == "0":
            print("\n返回上一步。")
            pause()
            clear_screen()
            return

        else:
            print("\n输入无效。")
            pause()
            clear_screen()

def reserve_classroom(student, root, time):
    while True:
        print(f"\n======== 预约管理 ========")
        print(f"当前用户: {student.name} ({student.id})")
        print("1. 浏览教室与状态")
        print("2. 申请预约")
        print("0. 返回主菜单")

        choice = input("请选择功能: ")

        if choice == "1":
            print("已选择：1. 浏览教室与状态")
            pause()
            clear_screen()
            print_all_buildings_summary(root)
            query_building_by_id(root)
            print("返回")
            pause()
            clear_screen()

        elif choice == "2":
            print("已选择：2. 申请预约")
            print("-" * 30)
            
            c_id = input("请输入要预约的教室ID: ").strip()
            
            print(f"\n正在加载教室 {c_id} 的日程表...")
            query_classroom_schedule(c_id)
            print("-" * 30)

            date_str = input("请输入预约日期 (格式 YYYY-MM-DD): ").strip()
            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                weekday = date_obj.isoweekday()
            except ValueError:
                print("❌ 日期格式错误，请使用 YYYY-MM-DD 格式。")
                pause()
                clear_screen()
                continue

            print(f"\n请输入起止节次 (1-{MAX_SLOTS_PER_DAY}):")
            start_slot = input("开始节次: ").strip()
            end_slot = input("结束节次: ").strip()

            if not start_slot.isdigit() or not end_slot.isdigit():
                print("❌ 节次必须是数字。")
                pause() 
                clear_screen()
                continue
            
            start_ts_id = f"TS_{weekday}_{start_slot}"
            end_ts_id = f"TS_{weekday}_{end_slot}"

            print(f"\n[确认信息] 申请预约: {c_id}")
            print(f"时间: {date_str} (周{weekday}) | 第 {start_slot} 节 至 第 {end_slot} 节")
            confirm = input("确认提交? (y/n): ")

            if confirm.lower() == 'y':
                success = reserve(
                    classroom_id=c_id, 
                    user_id=student.id, 
                    user_name=student.name, 
                    date_str=date_str, 
                    start_ts_id=start_ts_id, 
                    end_ts_id=end_ts_id
                )
                
                if success:
                    print("✅ 预约流程结束。")
                else:
                    print("❌ 预约流程结束（未成功）。")
            else:
                print("操作已取消。")
            
            pause()
            clear_screen()

        elif choice == "0":
            print("\n返回上一步。")
            pause()
            clear_screen()
            return

        else:
            print("\n输入无效。")
            pause()
            clear_screen()

def student_menu(student, root, time):
    """登录成功后的学生菜单"""
    while True:
        print(f"\n======== 欢迎 {student.name} ========")
        print(f"当前用户: {student.id} | 班级: {student.class_id}")
        print("1. 查看信息")
        print("2. 修改密码")
        print("3. 预约管理")
        print("0. 退出登录")
        
        choice = input("请选择功能: ")
        
        if choice == "1":
            print("\n已选择：1. 查看信息")
            pause()
            clear_screen()
            show_student(student, time)

        elif choice == "2":
            print("\n已选择：2. 修改密码")
            pause()
            clear_screen()
            new_student_password(student)

        elif choice == "3":
            print("\n已选择：3. 预约教室")
            pause()
            clear_screen()
            reserve_classroom(student, root, time)

        elif choice == "0":
            print("\n已退出。")
            pause()
            clear_screen()
            break

        else:
            print("\n输入无效。")
            pause()
            clear_screen()