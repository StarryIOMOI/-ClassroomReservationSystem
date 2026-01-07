import sqlite3, sys
from time_date_clean import time_interval, get_school_week
from src.utils.config import clear_screen, pause
from src.models.crud import print_course_table       #临时
from src.models.crud import (
    load_building_data, load_area_data, load_floor_data,
    load_classroom_data, load_class_data, load_semester_data,
    load_timeslots_data, load_special_semester_data,
    create_student_user, create_teacher_user, create_building,
    create_area, create_floor, create_classroom, create_class,
    create_semester, create_course)

def add_building():
    print("\n======== 添加教学楼 ========")
    buildings = load_building_data()

    if buildings:
        for b in buildings:
            print(f"教学楼：{b.name},id:{b.id}")

    while True:
        print("1. 添加教室")
        print("0. 返回")

        choice = input("请选择功能: ")

        if choice == "1":
            print("\n--- 新增教学楼 ---")
            b_id = input("请输入教学楼ID (例如 b001): ").strip()
            b_name = input("请输入教学楼名称: ").strip()
            desc = input("请输入描述 (可选, 直接回车跳过): ").strip()
            
            if not b_id or not b_name:
                print("错误：ID和名称不能为空！")
                return

            create_building(building_id=b_id, building_name=b_name, description=desc)
        
        elif choice == "0":
            print("\n返回")
            pause()
            return

        else:
            print("\n输入无效。")
            pause()


def add_area():
    print("\n======== 添加区域 ========")
    buildings = load_building_data()

    if buildings:
        for b in buildings:
            print(f"教学楼：{b.name},id:{b.id}")

    while True:
        print("1. 添加区域")
        print("0. 返回")

        choice = input("请选择功能: ")

        if choice == "1":
            print("\n--- 新增区域 ---")
            b_id = input("请输入所属教学楼ID (例如 b001): ").strip()
            a_id = input("请输入新区域ID (例如 a00103): ").strip()
            a_name = input("请输入区域 (例如 C区): ").strip()
            
            if not b_id or not a_id or not a_name:
                print("错误：所有字段都不能为空！")
                return

            create_area(area_id = a_id, area_name = a_name, building_id = b_id)
        
        elif choice == "0":
            print("\n返回")
            pause()
            return

        else:
            print("\n输入无效。")
            pause()

def add_floor():
    print("\n======== 添加楼层 ========")
    areas = load_area_data()

    if areas:
        for a in areas:
            print(f"区域：{a.name},id:{a.id},所属教学楼：{a.building_id}")

    while True:
        print("1. 添加楼层")
        print("0. 返回")

        choice = input("请选择功能: ")

        if choice == "1":
            print("\n--- 新增楼层 ---")
            a_id = input("请输入所属区域ID (例如 a00103): ").strip()
            f_id = input("请输入新楼层ID (例如 f001031): ").strip()
            f_name = input("请输入楼层 (例如 1层): ").strip()
            
            if not a_id or not f_id or not f_name:
                print("错误：所有字段都不能为空！")
                return

            create_floor(floor_id = f_id, floor_name = f_name, area_id = a_id)
        
        elif choice == "0":
            print("\n返回")
            pause()
            return

        else:
            print("\n输入无效。")
            pause()

def add_classroom():
    print("\n======== 添加教室 ========")
    floors = load_floor_data()

    if floors:
        for f in floors:
            print(f"楼层：{f.name},id:{f.id},所属区域：{f.area_id}")

    while True:
        print("1. 添加教室")
        print("0. 返回")

        choice = input("请选择功能: ")

        if choice == "1":
            print("\n--- 新增教室 ---")
            f_id = input("请输入所属楼层ID (例如 f001031): ").strip()
            c_id = input("请输入新教室ID (例如 c00103101): ").strip()
            c_name = input("请输入教室 (例如 101): ").strip()
            
            if not f_id or not c_id or not c_name:
                print("错误：所有字段都不能为空！")
                return

            create_classroom(classroom_id = c_id, classroom_name = c_name, floor_id = f_id)
        
        elif choice == "0":
            print("\n返回")
            pause()
            return

        else:
            print("\n输入无效。")
            pause()

def add_class():
    while True:
        print("1. 添加班级")
        print("0. 返回")

        choice = input("请选择功能: ")

        if choice == "1":
            print("\n--- 新增班级 ---")
            C_id = input("请输入新增班级ID (例如 C240303): ").strip()
            C_name = input("请输入班级名称 (例如 24软一): ").strip()
            
            if not C_id or not C_name:
                print("错误：所有字段都不能为空！")
                return

            create_class(class_id = C_id, class_name = C_name)

        elif choice == "0":
            print("\n返回")
            pause()
            return

        else:
            print("\n输入无效。")
            pause()

def add_teacher():
    while True:
        print("1. 添加教师")
        print("0. 返回")

        choice = input("请选择功能: ")

        if choice == "1":
            print("\n--- 新增教师 ---")
            T_id = input("请输入新增教师ID (例如 T202503001): ").strip()
            T_name = input("请输入教师名 (例如 yeh): ").strip()
            
            if not T_id or not T_name:
                print("错误：所有字段都不能为空！")
                return

            create_teacher_user(teacher_id = T_id, name = T_name)

        elif choice == "0":
            print("\n返回")
            pause()
            return

        else:
            print("\n输入无效。")
            pause()

def add_student():
    classes = load_class_data()

    if classes:
        for c in classes:
            print(f"班级：{c.name},id:{c.id}")

    while True:
        print("1. 添加学生")
        print("0. 返回")

        choice = input("请选择功能: ")

        if choice == "1":
            print("\n--- 新增学生 ---")
            C_id = input("请输新增学生所属班级ID (例如 C240306): ").strip()
            S_id = input("请输入新增学生ID (例如 S24030601): ").strip()
            S_name = input("请输入学生姓名 (例如 bxc): ").strip()
            
            if not S_id or not S_name or not C_id:
                print("错误：所有字段都不能为空！")
                return

            create_student_user(student_id = S_id, name = S_name, class_id = C_id)

        elif choice == "0":
            print("\n返回")
            pause()
            return

        else:
            print("\n输入无效。")
            pause()

def add_semester():
    while True:
        print("1. 添加学期")
        print("0. 返回")

        choice = input("请选择功能: ")

        if choice == "1":
            print("\n--- 新增学期 ---")
            s_id = input("请输新增学期ID (例如 2025-2026-1): ").strip()
            s_name = input("请输入新增学期 (例如 2025-2026学年第一学期): ").strip()
            s_start = input("请输入学期开始时间 (例如 2025-09-01): ").strip()
            s_end = input("请输入学期开始时间 (例如 2026-01-10): ").strip()
            
            if not s_id or not s_name or not s_start or not s_end:
                print("错误：所有字段都不能为空！")
                return
            
            days = time_interval(s_start, s_end)
            if days > 0:
                s_week = get_school_week(s_start, s_end)

            create_semester(semester_id = s_id, semester_name = s_name, date_start = s_start,
                            date_end = s_end, total_weeks = s_week)

        elif choice == "0":
            print("\n返回")
            pause()
            return

        else:
            print("\n输入无效。")
            pause()

def add_course():
    while True:
        print("\n======== 添加课程 ========")
        print_course_table()

        print("1. 添加课程")
        print("0. 返回")

        choice = input("请选择功能: ")

        if choice == "1":
            print("\n--- 新增课程 ---")
            CRS_id = input("请输新增课程ID (例如 CRS2403060101): ").strip()
            CRS_name = input("请输入新增学期 (例如 计算机导论): ").strip()
            C_id = input("请输入课程开设班级ID (例如 C240306)").strip()
            c_id = input("请输入课程开设教室ID (例如 c00103101)").strip()
            T_id = input("请输入课程教师ID (例如 T202503001)").strip()
            s_id = input("请输入课程开设学期ID (例如 T202503001)").strip()
            TS_start_id = input("请输入课程上课时间点ID (例如 TS_1_01)").strip()
            TS_end_id = input("请输入课程下课时间点ID (例如 TS_1_02)").strip()
            week_start = input("请输入课程开设周 (例如 1)").strip()
            week_end = input("请输入课程结束周 (例如 16)").strip()
            
            if any([not CRS_id, not CRS_name, not C_id, not c_id, not T_id, not s_id, 
            not TS_start_id, not TS_end_id, not week_start, not week_end]):
                print("错误：所有字段都不能为空！")
                return
            
            semester = load_special_semester_data()
            
            s = str(week_start)
            e = str(week_end)
            l = str(semester.week)

            if 0 >= s or s > e or e > l:
                print("错误：开设时间存在问题")
                return

            create_course(course_id = CRS_id, course_name = CRS_name, class_id = C_id,
                        classroom_id = c_id, teacher_id = T_id, semester_id = s_id,
                        start_timeslot_id = TS_start_id, end_timeslot_id = TS_end_id,
                        week_start = week_start, week_end = week_end)
            
        elif choice == "0":
            print("\n返回")
            pause()
            return

        else:
            print("\n输入无效。")
            pause()