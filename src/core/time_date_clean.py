import sqlite3
from datetime import datetime as dt, timedelta
from models import get_connection
from core import Semesters
from core import Timenow
from core import Timeslots

# 获取当前时间
current_time = dt.now()
year_now = current_time.year
month_now = current_time.month
day_now = current_time.day

def time_now():
    return current_time.strftime("%Y-%m-%d %H:%M:%S")

def load_semester():
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM semester")
    semester_rows = cursor.fetchall()

    semesters = [
        Semesters(row["semester_id"], row["semester_name"], row["date_start"], row["date_end"], row["total_week"])
        for row in semester_rows
    ]

    conn.close()
    return semesters

def load_timeslots():
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM timeslot")
    timeslot_rows = cursor.fetchall()

    timeslots = [
        Timeslots(row["timeslot_id"], row["weekday"], row["start_time"], row["end_time"])
        for row in timeslot_rows
    ]

    conn.close()
    return timeslots

def get_school_week(start_str, current_str):
    start = dt.strptime(start_str, "%Y-%m-%d").date()
    current = dt.strptime(current_str, "%Y-%m-%d").date()
    # 找出开学日所在周的周一
    start_monday = start - timedelta(days=start.isoweekday() - 1)
    # 找出当前日期所在周的周一
    current_monday = current - timedelta(days=current.isoweekday() - 1)
    # 计算两个周一之间相差的完整周数
    weeks_diff = (current_monday - start_monday).days // 7
    # 当前周数
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
                    return Timenow(s.id, s.name, week)
                elif st.month < month_now < et.month:
                    week = get_school_week(start_date_str, current_date_str)
                    return Timenow(s.id, s.name, week)
                elif et.month == month_now and day_now <= et.day:
                    week = get_school_week(start_date_str, current_date_str)
                    return Timenow(s.id, s.name, week)
                    
        else:
            if year_now == st.year:
                if month_now == st.month and day_now >= st.day:
                    week = get_school_week(start_date_str, current_date_str)
                    return Timenow(s.id, s.name, week)
                elif month_now > st.month:
                    week = get_school_week(start_date_str, current_date_str)
                    return Timenow(s.id, s.name, week)
            elif year_now == et.year:
                if month_now == et.month and day_now <= et.day:
                    week = get_school_week(start_date_str, current_date_str)
                    return Timenow(s.id, s.name, week)
                elif month_now < et.month:
                    week = get_school_week(start_date_str, current_date_str)
                    return Timenow(s.id, s.name, week)
            elif st.year < year_now < et.year:
                week = get_school_week(start_date_str, current_date_str)
                return Timenow(s.id, s.name, week)
    
    return None

def to_minute(time):
    _time = dt.strptime(time, "%H:%M")
    minutes = _time.hour * 60 + _time.minute
    return minutes

def total_minute(timeslots):
    for t in timeslots:
        st = to_minute(t.start)
        et = to_minute(t.end)
