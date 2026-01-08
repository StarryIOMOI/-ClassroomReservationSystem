import sqlite3
from datetime import datetime as dt, timedelta
from src.core.Class import Timenow
from src.models.crud import load_semester_data, load_timeslots_data, get_connection

MAX_SLOTS_PER_DAY = 13
DAYS_PER_WEEK = 7
TOTAL_TREE_SIZE = MAX_SLOTS_PER_DAY * DAYS_PER_WEEK

SCHEDULE_DATA = [
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

# 获取当前时间
current_time = dt.now()
year_now = current_time.year
month_now = current_time.month
day_now = current_time.day

def time_now():
    return current_time.strftime("%Y-%m-%d %H:%M:%S")

def get_time():
    semesters = load_semester_data()
    timenow_obj = locate_time(semesters)
    return timenow_obj

def get_school_week(start_str, end_str):
    start = dt.strptime(start_str, "%Y-%m-%d").date()
    end = dt.strptime(end_str, "%Y-%m-%d").date()
    # 找出开学日所在周的周一
    start_monday = start - timedelta(days=start.isoweekday() - 1)
    # 找出结束日期所在周的周一
    end_monday = end - timedelta(days=end.isoweekday() - 1)
    # 计算两个周一之间相差的完整周数
    weeks_diff = (end_monday - start_monday).days // 7
    # 周数
    week_number = weeks_diff + 1
    
    return week_number

def locate_time(semesters):
    current_date_str = f"{year_now:04d}-{month_now:02d}-{day_now:02d}"
    
    for s in semesters:
        st = dt.strptime(s.start, "%Y-%m-%d")
        et = dt.strptime(s.end, "%Y-%m-%d")
        
        start_date_str = s.start
        
        if st.year == et.year:
            if year_now == st.year:
                if st.month == month_now and st.day <= day_now:
                    week = get_school_week(start_date_str, current_date_str)
                    time = Timenow(s.name, week, s.id)
                elif st.month < month_now < et.month:
                    week = get_school_week(start_date_str, current_date_str)
                    time = Timenow(s.name, week, s.id) 
                elif et.month == month_now and day_now <= et.day:
                    week = get_school_week(start_date_str, current_date_str)
                    time = Timenow(s.name, week, s.id) 
                    
        else:
            if year_now == st.year:
                if month_now == st.month and day_now >= st.day:
                    week = get_school_week(start_date_str, current_date_str)
                    time = Timenow(s.name, week, s.id) 
                elif month_now > st.month:
                    week = get_school_week(start_date_str, current_date_str)
                    time = Timenow(s.name, week, s.id) 
            elif year_now == et.year:
                if month_now == et.month and day_now <= et.day:
                    week = get_school_week(start_date_str, current_date_str)
                    time = Timenow(s.name, week, s.id) 
                elif month_now < et.month:
                    week = get_school_week(start_date_str, current_date_str)
                    time = Timenow(s.name, week, s.id) 
            elif st.year < year_now < et.year:
                week = get_school_week(start_date_str, current_date_str)
                time = Timenow(s.name, week, s.id) 
    if time:
        return time
    else:
        return None

def to_minute(time):
    _time = dt.strptime(time, "%H:%M")
    minutes = _time.hour * 60 + _time.minute
    return minutes

def minute_of_tree(timeslots):
    start = 1440
    end = 0

    for t in timeslots:
        st = to_minute(t.start)
        et = to_minute(t.end)
        if st < start and st > 0:
            start = st
        if et > end and et < 1440:
            end = et
            
    total_minute = end - start
    time = {st, end, total_minute}
    return time

def day_of_year(day):
    d = dt.strptime(day, "%Y-%m-%d")
    days = 0
    day_in_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    if (d.year % 4 == 0 and d.year % 100 != 0) or (d.year % 400 == 0):
        day_in_month[2] = 29

    for i in range(d.month): 
        days += day_in_month[i]

    days += d.day
    return days

def time_interval(day1, day2):
    date1 = dt.strptime(day1, "%Y-%m-%d")
    date2 = dt.strptime(day2, "%Y-%m-%d")

    days_diff = abs((date2 - date1).days)
    return days_diff

def parse_timeslot_id(timeslot_id):
    """
    解析 TS_星期_节数 格式
    例如: 'TS_1_1' -> (1, 1)
    """
    try:
        parts = timeslot_id.split('_')
        weekday = int(parts[1])
        slot = int(parts[2])
        return weekday, slot
    except (IndexError, ValueError):
        print(f"❌ 错误: timeslot_id 格式无效 ({timeslot_id})")
        return None, None

def get_tree_index(timeslot_id):
    """
    将 timeslot_id 映射为线段树的线性下标 [0, 90]
    公式: (星期 - 1) * 每天节数 + (节数 - 1)
    """
    weekday, slot = parse_timeslot_id(timeslot_id)
    
    if weekday is None:
        return -1
        
    if not (1 <= weekday <= 7) or not (1 <= slot <= MAX_SLOTS_PER_DAY):
        print(f"❌ 错误: timeslot_id 数值越界 ({timeslot_id})")
        return -1

    index = (weekday - 1) * MAX_SLOTS_PER_DAY + (slot - 1)
    return index

def get_timeslot_from_index(index):
    """
    将线段树下标反向映射回 (weekday, slot)
    :return: (weekday, slot) 例如 (1, 1)
    """
    if index < 0 or index >= TOTAL_TREE_SIZE:
        return None, None
        
    weekday = (index // MAX_SLOTS_PER_DAY) + 1
    slot = (index % MAX_SLOTS_PER_DAY) + 1
    return weekday, slot

def get_id_from_index(index):
    """
    将线段树下标反向映射回 ID 字符串
    :return: 'TS_1_1'
    """
    weekday, slot = get_timeslot_from_index(index)
    if weekday:
        return f"TS_{weekday}_{slot}"
    return None