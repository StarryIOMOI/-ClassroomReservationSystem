import sqlite3
import os, sys
from datetime import datetime, timedelta
from src.core.Class import Courses, Reservation
from src.core.time_date_clean import get_time, get_school_week, locate_time
from src.core.Schedule_System import load_course_data, load_reservation_data
from src.models.crud import get_connection, load_timeslots_data, load_semester_data

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

def query_classroom_schedule(classroom_id):
    """
    查询指定教室在特定逻辑时间段内的所有安排（课程 + 预约）
    """
    print(f"正在查询教室 {classroom_id} 的日程安排...")
    
    # 1. 获取当前学期状态
    semesters_data = load_semester_data()
    timenow = locate_time(semesters_data)
    
    if not timenow:
        print("❌ 当前不在任何学期内，无法计算周次。")
        return

    current_semester_id = timenow.semester.id
    print(f"当前学期: {timenow.name} (ID: {current_semester_id})")

    # 2. 获取日期范围
    target_dates = get_date_range()
    start_str = target_dates[0].strftime("%Y-%m-%d")
    end_str = target_dates[-1].strftime("%Y-%m-%d")
    print(f"查询时间范围: {start_str} 至 {end_str}\n")

    # 3. 加载基础数据
    all_timeslots = load_timeslots_data()
    timeslot_map = {ts.id: ts for ts in all_timeslots}

    # 3.2 加载该教室本学期所有课程
    courses = load_course_data(classroom_id, current_semester_id)

    # 3.3 加载该教室本学期所有预约 (需要后续按日期过滤)
    reservations = load_reservation_data(classroom_id, current_semester_id)

    # 4. 按日期整合输出
    for date_obj in target_dates:
        date_str = date_obj.strftime("%Y-%m-%d")
        week_day_num = date_obj.weekday() + 1 # Python 0-6, 通常习惯 1-7 (需确认Timeslots里的定义)
        # 假设 Timeslots.weekday 存储的是 1(Mon) - 7(Sun)
        
        # 计算该日期是学期的第几周
        # 使用 time_date_clean.get_school_week
        semester_start_str = timenow.semester.start
        school_week = get_school_week(semester_start_str, date_str)

        print(f"📅 {date_str} (周{week_day_num}) [第 {school_week} 周]")
        print("-" * 50)
        
        daily_items = []

        # --- 处理课程 ---
        for course in courses:
            # 1. 检查课程周次范围 (例如: 1-16周)
            if int(course.week_start) <= school_week <= int(course.week_end):
                # 2. 检查星期几是否匹配
                # 课程对象有 timeslot_id，需要查 timeslot_map 获取 weekday
                ts = timeslot_map.get(course.start_timeslot_id) # 假设课程主要看开始时间段
                
                if ts and ts.weekday == week_day_num:
                    # 找到了当天的课程
                    # 获取结束时间 (如果有 end_timeslot_id)
                    end_ts = timeslot_map.get(course.end_timeslot_id)
                    time_range = f"{ts.start}-{end_ts.end}" if end_ts else f"{ts.start}-{ts.end}"
                    
                    item = {
                        "type": "【课程】",
                        "time_sort": ts.start, # 用于排序
                        "time_display": time_range,
                        "name": course.name,
                        "user": course.teacher_name,
                        "info": f"{course.class_name}"
                    }
                    daily_items.append(item)

        # --- 处理预约 ---
        for res in reservations:
            # 预约对象通常有 date 字段 (字符串)
            if res.date == date_str:
                # 状态检查 (假设 1 是有效，-1 是取消，根据 cancel 函数推断)
                if res.status != -1: 
                    item = {
                        "type": "【预约】",
                        "time_sort": res.start,
                        "time_display": f"{res.start}-{res.end}",
                        "name": "个人预约", # 预约表里可能存的是 user_name
                        "user": res.user_name,
                        "info": f"ID: {res.user_id}"
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
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    if teacher_id == 0:
        cursor.execute("""
            SELECT * FROM courses
            WHERE class_id = ? AND semester_id
        """, (class_id, semester_id))
        course_rows = cursor.fetchall()

        courses = [
            Courses(row["course_id"], row["course_name"], row["class_id"], row["class_name"],
                    row["classroom_id"], row["classroom_name"], row["teacher_id"], row["teacher_name"],
                    row["week_start"], row["week_end"], row["start_timeslot_id"], row["end_timeslot_id"],
                    row["semester_id"],)
            for row in course_rows
        ]

    if class_id == 0:
        cursor.execute("""
            SELECT * FROM courses
            WHERE teacher_id = ? AND semester_id = ?
        """, (teacher_id, semester_id))
        course_rows = cursor.fetchall()

        courses = [
            Courses(row["course_id"], row["course_name"], row["class_id"], row["class_name"],
                    row["classroom_id"], row["classroom_name"], row["teacher_id"], row["teacher_name"],
                    row["week_start"], row["week_end"], row["start_timeslot_id"], row["end_timeslot_id"],
                    row["semester_id"],)
            for row in course_rows
        ]

    conn.close()

    print_course(courses)

def print_course(courses):
    for c in courses:
        print(f"课程编号：{c.id}")
        print(f"课程名：{c.name}")
        print(f"班级：{c.class_name}")
        print(f"教室：{c.classroom_name}")
        print(f"教师：{c.teacher_name}")
        print(f"起始周：{c.week_start}")
        print(f"结束周：{c.week_end}")
        print(f"时间：{c.timeslot_id}")