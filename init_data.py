import sys
import os
import sqlite3

# 确保能引用到同级目录下的模块
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from src.models.crud import get_connection
from src.models.data_db import init_db
# 从 crud.py 导入上一轮生成的函数
# 如果你还没有更新 crud.py，请先更新，或者手动将那些函数复制到这里
from src.models.crud import (
    create_teacher_user, 
    create_student_user, 
    create_building, 
    create_area, 
    create_floor, 
    create_classroom,
    create_class,
    create_timeslot,
    create_semester
)

# ---------------------------------------------------------
# 主初始化逻辑
# ---------------------------------------------------------
def run_initialization():
    print("=== 开始初始化数据 ===")
    
    # 0. 确保数据库表结构已建立
    init_db()
    print("-" * 30)

    # 1. 添加班级 (必须先有班级，学生才能关联)
    create_class("C240306", "24软四")

    # 2. 添加教师
    # id：T202503001, 姓名：yeh, 密码：123456， 状态：1
    create_teacher_user("T202503001", "yeh", password_hash="123456", status=1)

    # 3. 添加学生
    students_data = [
        ("S24030601", "bxc"),
        ("S24030625", "wyc"),
        ("S24030620", "thl"),
        ("S24030605", "cqy")
    ]
    
    for s_id, s_name in students_data:
        # 统一设置：密码123456，状态1，班级C240306
        create_student_user(s_id, s_name, class_id="C240306", password_hash="123456", status=1)

    print("-" * 30)

    # 4. 添加教学楼
    # id：b001，教学楼名：天枢楼
    create_building("b001", "天枢楼", status=1, description="无")

    # 5. 添加区域
    areas_data = [
        ("a00101", "a区"),
        ("a00102", "b区")
    ]
    for a_id, a_name in areas_data:
        create_area(a_id, a_name, building_id="b001", status=1)

    # 6. 添加楼层 和 教室
    # 定义楼层数据结构: (楼层ID, 层名, 所属区域ID)
    floors_data = [
        # a区
        ("f001011", "1层", "a00101"),
        ("f001012", "2层", "a00101"),
        ("f001013", "3层", "a00101"),
        ("f001014", "4层", "a00101"),
        # b区
        ("f001021", "1层", "a00102"),
        ("f001022", "2层", "a00102"),
        ("f001023", "3层", "a00102"),
        ("f001024", "4层", "a00102"),
    ]

    for f_id, f_name, area_id in floors_data:
        # 添加楼层
        success = create_floor(f_id, f_name, area_id, status=1)
        
        if success:
            # 自动生成该楼层的5个教室
            # 提取楼层数字用于教室名 (例如 "4层" -> "4")
            floor_num_str = f_name.replace("层", "")
            
            # 提取楼层ID的数字部分用于教室ID (例如 "f001024" -> "001024")
            floor_id_num = f_id[1:] 

            for i in range(1, 6): # 1 到 5
                # 格式化序号，补零 (01, 02...)
                seq = f"{i:02d}"
                
                # 规则：id = c + 楼层id数字 + 序号
                c_id = f"c{floor_id_num}{seq}"
                
                # 规则：name = 楼层数 + 序号 (例如 4 + 01 = 401)
                c_name = f"{floor_num_str}{seq}"
                
                # 【修改处】在这里显式添加 type="普通教室"
                create_classroom(c_id, c_name, floor_id=f_id, status=1, capacity=30, type="普通教室")

    print("=== 开始初始化 13节课 标准作息时间 ===")

    # 你提供的具体时间表 (序号, 开始, 结束)
    # 注意：已将中文冒号替换为英文冒号，并补全了0
    schedule_data = [
        (1,  "08:00", "08:45"),
        (2,  "08:50", "09:35"),
        (3,  "09:55", "10:40"),
        (4,  "10:45", "11:30"),
        (5,  "11:35", "12:15"),
        (6,  "13:30", "14:15"),
        (7,  "14:20", "15:05"),
        (8,  "15:25", "16:10"),
        (9,  "16:15", "17:00"),
        (10, "17:05", "17:45"),
        (11, "18:30", "19:15"),
        (12, "19:20", "20:05"),
        (13, "20:10", "20:50"),
    ]

    # 设置生成的星期范围：1=周一, 5=周五, 7=周日
    # 这里默认生成 周一 到 周五
    days_range = range(1, 6) 

    success_count = 0
    
    for day in days_range:
        print(f"--- 正在生成 周{day} 的数据 ---")
        for seq, start, end in schedule_data:
            # ID 生成规则: TS + 星期几 + 节次 (补零)
            # 例如: 周一第1节 -> TS_1_01
            # 例如: 周五第13节 -> TS_5_13
            t_id = f"TS_{day}_{seq:02d}"
            
            if create_timeslot(t_id, day, start, end):
                success_count += 1

    s_id = "2025-2026-1"
    s_name = "2025-2026学年第一学期"
    s_start = "2025-09-01"
    s_end = "2026-01-10"
    s_week = "19"
    create_semester(s_id, s_name, s_start, s_end, s_week)

    print("=== 初始化完成 ===")

if __name__ == "__main__":
    run_initialization()