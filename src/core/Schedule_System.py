import sqlite3
from core import Courses
from core import Reservation
from core import Timeslots
from core import Semesters
from core import to_minute
from core import SegmentTree
from core import day_of_year
from models import get_connection

def load_course_data(classroom_id, semester_id): 
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM courses 
        WHERE classroom_id = ? AND semester_id = ?
    """, (classroom_id, semester_id))                                                                                                              

    course_rows = cursor.fetchall()

    courses = [
        Courses(row["course_id"], row["course_name"], row["class_id"], row["class_name"],
                row["classroom_id"],row["classroom_name"], row["teacher_id"], row["teacher_name"],
                row["week_start"], row["week_end"], row["timeslot_id"], row["semester_id"])
        for row in course_rows
    ]

    cursor.execute("""
        SELECT * FROM  reservation
        WHERE classroom_id = ? AND semester_id = ?
    """, (classroom_id, semester_id))

    reservation_rows = cursor.fetchall()

    reservations = [
        Reservation(row["course_id"], row["course_name"], row["class_id"], row["class_name"],
                    row["classroom_id"],row["classroom_name"], row["teacher_id"], row["teacher_name"],
                    row["week_start"], row["week_end"], row["timeslot_id"], row["semester_id"])
        for row in reservation_rows
    ]

    cursor.execute("SELECT * FROM timeslot")
    timeslot_rows = cursor.fetchall()

    timeslots = [
        Timeslots(row["timeslot_id"], row["weekday"], row["start_time"], row["end_time"])
        for row in timeslot_rows
    ]

    cursor.execute("""SELECT * FROM semester""")                                                                                                              

    semester_rows = cursor.fetchall()

    semesters = [
            Semesters(row["semester_id"], row["semester_name"], row["date_start"],
                      row["date_end"], row["total_weeks"])
        for row in semester_rows
    ]

    conn.close()
    return courses, reservations, timeslots, semesters

def clean_timeslots(timeslots):
    for t in timeslots:
        t.start = to_minute(t.start)
        t.end = to_minute(t.end)
    return timeslots

def reserve(semester_id, classroom_id, user_id, user_name, date, start, end, status):
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    have_time = Schedule_System.memory_reserve(date, start)
    if have_time:
        try:
            sql = '''
            INSERT INTO reservation
            (classroom_id, user_id, user_name, date, start, end, status) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
            '''  

            cursor.execute(sql, (
                classroom_id,
                user_id,
                user_name,
                date,
                start,
                end,
                status
            ))

            conn.commit()
            print(f"预约成功！")
            return True

        except sqlite3.IntegrityError as e:
            print(f"添加失败：数据冲突。详细信息：{e}")
            return False
        
        except Exception as e:
            print(f"添加失败：发生未知错误 {e}")
            return False

        finally:
            cursor.execute("""
            SELECT * FROM  reservation
            WHERE classroom_id = ? AND semester_id = ?
            """, (classroom_id, semester_id))

            reservation_rows = cursor.fetchall()

            reservations = [
            Reservation(row["course_id"], row["course_name"], row["class_id"], row["class_name"],
                        row["classroom_id"],row["classroom_name"], row["teacher_id"], row["teacher_name"],
                        row["week_start"], row["week_end"], row["timeslot_id"], row["semester_id"])
            for row in reservation_rows
            ]
            conn.close()
            return reservations

def cancel(semester_id, classroom_id, user_id, user_name, date, start, end, status = -1):
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        cursor.execute("""
        UPDATE reservation
        SET status = ?
        WHERE semester_id = ? AND classroom_id = ? AND user_id = ?
            AND user_name = ? AND date = ? AND start = ? AND end = ?
        """, (status, semester_id, classroom_id, user_id, user_name, date, start, end))

        conn.commit()
        return True
    
    except sqlite3.IntegrityError as e:
        print(f"添加失败：数据冲突。详细信息：{e}")
        return False
        
    except Exception as e:
        print(f"添加失败：发生未知错误 {e}")
        return False

    finally:
        cursor.execute("""
        SELECT * FROM  reservation
        WHERE classroom_id = ? AND semester_id = ?
        """, (classroom_id, semester_id))

        reservation_rows = cursor.fetchall()

        reservations = [
        Reservation(row["course_id"], row["course_name"], row["class_id"], row["class_name"],
                    row["classroom_id"],row["classroom_name"], row["teacher_id"], row["teacher_name"],
                    row["week_start"], row["week_end"], row["timeslot_id"], row["semester_id"])
        for row in reservation_rows
        ]
        conn.close()
        Schedule_System.memory_cancel(date, end, start)
        return reservations

class Schedule_System:
    def __init__(self, start_time, end_time, total_time, time_step = 5):
        self.start = start_time
        self.end = end_time
        self.step = time_step
        self.total_slots = total_slots
        self.date = {}

        total_slots = total_time / time_step

    def add_date(self, semesters):
        start = day_of_year(semesters.start)
        end = day_of_year(semesters.end) + 1

        for i in range(start, end):
            self.date[i] = SegmentTree(self.total_slots)

    def find_idx(self, time, is_end):
        minute = to_minute(time)
        offset = minute - self.start
        idx = offset // self.step

        if (is_end == 0):
            return idx - 1
        else:
            return idx
        
    def memory_reserve(self, date, start, end):
        d = day_of_year(date)
        if d not in self.date:
            print(f"❌ 时间{date}超出预约范围！")
            return
        
        l = self.find_idx(start, is_end = 0)
        r = self.find_idx(end, is_end = 1)

        if l > r:
            print(f"❌ 时间无效: 开始不能晚于结束")
            return
        if l < 0 or l >= self.total_slots:
            print(f"❌ 时间无效：开始时间超出预约范围")
            return
        if l < 0 or l >= self.total_slots:
            print(f"❌ 时间无效：结束时间超出预约范围")
            return
        
        st = self.date[d]
        if st.book(l, r):
            print(f"✅ 预约成功: {date} | {start} - {end}")
            return True
        else:
            print(f"⚠️ 预约失败: {date} | {start} - {end} (时间冲突)")
            return False
        
    def memory_cancel(self, date, start, end):
        d = day_of_year(date)

        l = self.find_idx(start, is_end = 0)
        r = self.find_idx(end, is_end = 1)

        st = self.date[d]
        st.cancel(l,r)
        print(f"✅ 已取消预约: {date} | {start} - {end}")