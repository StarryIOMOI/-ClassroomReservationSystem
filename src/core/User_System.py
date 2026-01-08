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

def query_classroom_schedule(classroom_id, time):
    """
    查询指定教室在特定逻辑时间段内的所有安排（课程 + 预约）
    适配 data_db.py 和 Class.py 结构
    """
    print(f"正在查询教室 {classroom_id} 的日程安排...")
    
    # 1. 获取当前学期状态
    semesters_data = load_semester_data()
    timenow = locate_time(semesters_data)
    
    if not timenow:
        print("❌ 当前不在任何学期内，无法计算周次。")
        return

    current_semester_id = timenow.semester_id
    
    # 【修复 1】Timenow 类(Class.py)没有 semester 属性，只有 semester_id
    # 我们需要通过 ID 在 semesters_data 中找到对应的学期对象，以获取开学日期
    current_semester_obj = next((s for s in semesters_data if s.id == current_semester_id), None)
    
    if not current_semester_obj:
        print("❌ 无法找到匹配的学期信息。")
        return
        
    semester_start_str = current_semester_obj.start # Class.py 中 Semesters 使用 .start
    print(f"当前学期: {timenow.name} (ID: {current_semester_id})")

    # 2. 获取日期范围
    target_dates = get_date_range()
    start_str = target_dates[0].strftime("%Y-%m-%d")
    end_str = target_dates[-1].strftime("%Y-%m-%d")
    print(f"查询时间范围: {start_str} 至 {end_str}\n")

    # 3. 加载基础数据
    all_timeslots = load_timeslots_data()
    # 映射: timeslot_id -> Timeslots对象
    timeslot_map = {ts.id: ts for ts in all_timeslots}

    # 3.2 加载该教室本学期所有课程
    # 假设 load_courses_data 参数: (classroom_id, mode, semester_id)
    courses = load_courses_data(classroom_id, 0, current_semester_id)

    # 3.3 加载该教室本学期所有预约
    reservations = load_reservation_data(classroom_id, current_semester_id, time.date)

    # 4. 按日期整合输出
    for date_obj in target_dates:
        date_str = date_obj.strftime("%Y-%m-%d")
        
        # Python weekday() 是 0(Mon)-6(Sun)。
        # data_db.py 中 timeslot 表 weekday 定义通常对应 ISO (1-7) 或 Python (0-6)。
        # 假设数据库存的是 1-7 (ISO标准)，这里进行转换 +1
        week_day_num = date_obj.weekday() + 1 
        
        # 计算该日期是学期的第几周
        school_week = get_school_week(semester_start_str, date_str)

        print(f"📅 {date_str} (周{week_day_num}) [第 {school_week} 周]")
        print("-" * 50)
        
        daily_items = []

        # --- 处理课程 (Courses) ---
        if courses:
            for course in courses:
                # Class.py: course.week_start, week_end
                # 1. 检查课程周次范围 (转换为 int 进行比较)
                try:
                    c_start_week = int(course.week_start)
                    c_end_week = int(course.week_end)
                except ValueError:
                    continue # 数据格式错误跳过

                if c_start_week <= school_week <= c_end_week:
                    # 2. 获取时间段对象
                    # Class.py: start_timeslot_id
                    ts = timeslot_map.get(course.start_timeslot_id)
                    
                    # 3. 检查星期几是否匹配
                    # Class.py: Timeslots.weekday (需确认是 int 还是 str)
                    if ts and int(ts.weekday) == week_day_num:
                        
                        # 获取结束时间
                        end_ts = timeslot_map.get(course.end_timeslot_id)
                        
                        # Class.py: Timeslots.start (不是 start_time)
                        start_t = ts.start 
                        end_t = end_ts.end if end_ts else ts.end
                        time_display = f"{start_t}-{end_t}"
                        
                        item = {
                            "type": "【课程】",
                            "time_sort": start_t, # 排序键
                            "time_display": time_display,
                            "name": course.name,
                            "user": course.teacher_name,
                            "info": f"{course.class_name}"
                        }
                        daily_items.append(item)

        # --- 处理预约 (Reservation) ---
        if reservations:
            for res in reservations:
                # Class.py: Reservation.date, Reservation.status
                if res.date == date_str:
                    # 状态检查 (假设 -1 是取消)
                    if res.status != -1: 
                        
                        # Class.py: Reservation 直接存了 start 和 end 字符串，不需要查 timeslot
                        # 假设格式为 "HH:MM"
                        item = {
                            "type": "【预约】",
                            "time_sort": res.start, 
                            "time_display": f"{res.start}-{res.end}",
                            "name": "个人预约", 
                            "user": res.user_name,
                            "info": f"ID: {res.id}" # Class.py: Reservation.id
                        }
                        daily_items.append(item)

        # --- 排序并打印 ---
        if not daily_items:
            print("    (今日无安排)")
        else:
            # 按开始时间字符串排序 (例如 "08:00" < "10:00")
            daily_items.sort(key=lambda x: x["time_sort"])
            
            for item in daily_items:
                # 格式化打印
                print(f"    {item['time_display']:<11} | {item['type']} {item['name']}")
                print(f"                 用户: {item['user']} | 备注: {item['info']}")
        
        print("\n")

def load_courses_data(class_id, teacher_id, semester_id): 
    courses = []

    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    if teacher_id == "0":
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

    if class_id == "0":
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
    if courses:
        print_course(courses)
    else:
        print("没有课程信息！")

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