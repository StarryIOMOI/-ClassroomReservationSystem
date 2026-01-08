import sqlite3
import os, sys
from datetime import datetime, timedelta
from src.core.Class import Courses, Reservation
from src.core.time_date_clean import (
    get_time, 
    get_school_week, 
    locate_time, 
    SCHEDULE_DATA, 
    parse_timeslot_id
)
from src.core.Schedule_System import load_course_data, load_reservation_data
from src.models.crud import get_connection, load_semester_data

def get_date_range():
    """
    根据当前时间生成查询所需的日期范围列表。
    逻辑：
    - 周一到周五(0-4): 返回本周一到本周日。
    - 周六(5)到周日(6): 返回今天到下周五。
    """
    now = datetime.now()
    today = now.date()
    weekday = today.weekday() # 0=Mon, 6=Sun
    
    date_list = []
    
    if weekday <= 4: # 周一到周五
        # 找本周一
        start_date = today - timedelta(days=weekday)
        # 找本周日 (周一 + 6天)
        end_date = start_date + timedelta(days=6)
    else: # 周六或周日
        # 起始日是今天
        start_date = today
        # 找下周一
        days_to_next_monday = 7 - weekday
        next_monday = today + timedelta(days=days_to_next_monday)
        # 找下周五 (下周一 + 4天)
        end_date = next_monday + timedelta(days=4)
        
    # 生成从 start_date 到 end_date 的所有日期
    current = start_date
    while current <= end_date:
        date_list.append(current)
        current += timedelta(days=1)
        
    return date_list

def get_time_str_by_slot(slot_id):
    """
    根据节次ID (int) 获取时间字符串
    例如: 1 -> ("08:00", "08:45")
    """
    for item in SCHEDULE_DATA:
        if item[0] == slot_id:
            return item[1], item[2] # start, end
    return "??:??", "??:??"

def query_classroom_schedule(classroom_id, time):
    """
    查询指定教室在特定逻辑时间段内的所有安排（课程 + 预约）
    适配新的 timeslot_id 结构
    """
    print(f"正在查询教室 {classroom_id} 的日程安排...")
    
    # 1. 获取当前学期状态
    semesters_data = load_semester_data()
    timenow = locate_time(semesters_data)
    
    if not timenow:
        print("❌ 当前不在任何学期内，无法计算周次。")
        return

    current_semester_id = timenow.semester_id

    # 2. 获取日期范围
    target_dates = get_date_range()
    # 将日期对象转换为字符串列表，供 load_reservation_data 使用
    date_strings = [d.strftime("%Y-%m-%d") for d in target_dates]

    # 3. 加载数据
    # 3.1 加载该教室本学期所有课程 (使用 Schedule_System 中的加载函数)
    courses = load_course_data(classroom_id, current_semester_id)

    # 3.2 加载该教室本周所有预约 (传入日期列表)
    reservations = load_reservation_data(classroom_id, current_semester_id, date_strings)

    # 4. 按日期整合输出
    for date_obj in target_dates:
        date_str = date_obj.strftime("%Y-%m-%d")
        week_day_num = date_obj.isoweekday() # 1=Mon, 7=Sun
        
        # 计算该日期是学期的第几周
        # locate_time 返回的 timenow 包含当前周次，但这里需要针对每一天计算准确周次
        # 也可以直接用 get_school_week 计算
        semester_start = timenow.semester.start if hasattr(timenow, 'semester') else None
        # 如果 timenow 对象结构不同，这里做回退处理，重新查找 semester 对象
        if not semester_start:
            for s in semesters_data:
                if s.id == current_semester_id:
                    semester_start = s.start
                    break
        
        school_week = get_school_week(semester_start, date_str)

        print(f"📅 {date_str} (周{week_day_num}) [第 {school_week} 周]")
        print("-" * 50)
        
        daily_items = []

        # --- 处理课程 ---
        for course in courses:
            # 1. 检查课程周次范围
            if int(course.week_start) <= school_week <= int(course.week_end):
                # 2. 解析 ID 获取星期和节次
                # course.start_timeslot_id 如 "TS_1_1"
                c_weekday, c_start_slot = parse_timeslot_id(course.start_timeslot_id)
                _, c_end_slot = parse_timeslot_id(course.end_timeslot_id)

                # 3. 匹配星期
                if c_weekday == week_day_num:
                    # 4. 获取具体时间字符串用于显示和排序
                    t_start, _ = get_time_str_by_slot(c_start_slot)
                    _, t_end = get_time_str_by_slot(c_end_slot)
                    
                    item = {
                        "type": "【课程】",
                        "time_sort": t_start, 
                        "time_display": f"{t_start}-{t_end}",
                        "name": course.name,
                        "user": course.teacher_name,
                        "info": f"{course.class_name} (第{c_start_slot}-{c_end_slot}节)"
                    }
                    daily_items.append(item)

        # --- 处理预约 ---
        for res in reservations:
            # load_reservation_data 已经筛选了日期范围，但这里要匹配具体哪一天
            if res.date == date_str and res.status != -1:
                # 解析 ID
                _, r_start_slot = parse_timeslot_id(res.start_timeslot_id)
                _, r_end_slot = parse_timeslot_id(res.end_timeslot_id)
                
                t_start, _ = get_time_str_by_slot(r_start_slot)
                _, t_end = get_time_str_by_slot(r_end_slot)

                item = {
                    "type": "【预约】",
                    "time_sort": t_start,
                    "time_display": f"{t_start}-{t_end}",
                    "name": "个人预约",
                    "user": res.user_name,
                    "info": f"ID: {res.id}"
                }
                daily_items.append(item)

        # --- 排序并打印 ---
        if not daily_items:
            print("    (今日无安排)")
        else:
            # 按开始时间排序
            daily_items.sort(key=lambda x: x["time_sort"])
            
            for item in daily_items:
                print(f"    {item['time_display']} | {item['type']} {item['name']}")
                print(f"             用户: {item['user']} | 备注: {item['info']}")
        
        print("\n")

def load_courses_data(class_id, teacher_id, semester_id): 
    """
    用户（学生/教师）查询自己课程表的函数
    """
    courses = []

    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # 构建查询
    sql = "SELECT * FROM courses WHERE semester_id = ?"
    params = [semester_id]

    if teacher_id != 0 and teacher_id != "0":
        sql += " AND teacher_id = ?"
        params.append(teacher_id)
    
    if class_id != 0 and class_id != "0":
        sql += " AND class_id = ?"
        params.append(class_id)

    cursor.execute(sql, params)
    course_rows = cursor.fetchall()

    courses = [
        Courses(row["course_id"], row["course_name"], row["class_id"], row["class_name"],
                row["classroom_id"], row["classroom_name"], row["teacher_id"], row["teacher_name"],
                row["week_start"], row["week_end"], 
                row["start_timeslot_id"], row["end_timeslot_id"], # 确保读取新字段
                row["semester_id"])
        for row in course_rows
    ]

    conn.close()
    if courses:
        print_course(courses)
    else:
        print("没有课程信息！")

def print_course(courses):
    for c in courses:
        # 解析 ID 以便打印友好的节次信息
        w_day, s_slot = parse_timeslot_id(c.start_timeslot_id)
        _, e_slot = parse_timeslot_id(c.end_timeslot_id)

        print(f"课程编号：{c.id}")
        print(f"课程名：{c.name}")
        print(f"班级：{c.class_name}")
        print(f"教室：{c.classroom_name}")
        print(f"教师：{c.teacher_name}")
        print(f"周次：第{c.week_start}-{c.week_end}周")
        # 打印解析后的时间信息
        print(f"时间：周{w_day} 第{s_slot}-{e_slot}节 ({c.start_timeslot_id})")
        print("-" * 20)