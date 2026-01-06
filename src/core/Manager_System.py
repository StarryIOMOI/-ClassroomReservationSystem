import sqlite3, sys
from models import load_building_data, load_area_data, load_floor_data, load_classroom_data
from models import create_student_user, create_teacher_user, create_building, create_area, create_floor, create_classroom, create_class
from models import get_connection
from utils import clear_screen, pause

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
            T_id = input("请输入新增教师ID (例如 "T202503001"): ").strip()
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
    while True:
        print("1. 添加学生")
        print("0. 返回")

        choice = input("请选择功能: ")

        if choice == "1":
            print("\n--- 新增学生 ---")
            C_id = input("请输新增学生所属班级ID (例如 "T202503001"): ").strip()
            T_id = input("请输入新增教师ID (例如 "T202503001"): ").strip()
            T_name = input("请输入教师名 (例如 yeh): ").strip()
            
            if not T_id or not T_name or not C_id:
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