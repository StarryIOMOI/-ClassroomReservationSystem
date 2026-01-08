import sqlite3
from datetime import datetime, timedelta
from src.core.Class import Courses, Reservation
from src.core.Segment_Tree import SegmentTree
from src.core.time_date_clean import (
    get_tree_index, 
    TOTAL_TREE_SIZE, 
    get_time, 
    MAX_SLOTS_PER_DAY,
    parse_timeslot_id
)
from src.models.crud import get_connection

def get_current_week_dates():
    """
    获取本周（周一到周日）的日期字符串列表
    返回: ['2023-10-01', '2023-10-02', ...]
    """
    now = datetime.now()
    # 找到本周一 (isoweekday: Mon=1 ... Sun=7)
    monday = now - timedelta(days=now.isoweekday() - 1)
    dates = []
    for i in range(7):
        day = monday + timedelta(days=i)
        dates.append(day.strftime("%Y-%m-%d"))
    return dates

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
                row["week_start"], row["week_end"], 
                row["start_timeslot_id"], row["end_timeslot_id"], 
                row["semester_id"])
        for row in course_rows
    ]

    conn.close()
    return courses

def load_reservation_data(classroom_id, semester_id, week_dates): 
    """
    只加载本周涉及的预约记录
    """
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    if isinstance(week_dates, str):
        week_dates = [week_dates]
    
    if not week_dates:
        conn.close()
        return []

    placeholders = ','.join('?' for _ in week_dates)
    
    query = f"""
        SELECT * FROM reservation
        WHERE classroom_id = ? 
          AND semester_id = ?
          AND date IN ({placeholders})
          AND status != -1
    """
    
    params = [classroom_id, semester_id] + week_dates
    
    try:
        cursor.execute(query, params)
        reservation_rows = cursor.fetchall()
    except Exception as e:
        print(f"数据库查询出错: {e}")
        reservation_rows = []
    
    reservations = []
    for row in reservation_rows:
        res_id = row["reservation_id"] if "reservation_id" in row.keys() else row["id"]
        
        # 从 timeslot_id 解析 weekday
        parsed_weekday, _ = parse_timeslot_id(row["start_timeslot_id"])
        if parsed_weekday is None:
            parsed_weekday = 0

        res = Reservation(
            res_id, 
            row["classroom_id"], 
            row["user_id"], 
            row["user_name"], 
            row["date"], 
            row["start_timeslot_id"], 
            row["end_timeslot_id"], 
            parsed_weekday,
            row["status"],
            row["semester_id"]
        )
        reservations.append(res)

    conn.close()
    return reservations

class Schedule_System:
    def __init__(self, classroom_id):
        self.classroom_id = classroom_id
        self.tree = SegmentTree(TOTAL_TREE_SIZE)
        
        self.timenow = get_time() 
        if not self.timenow:
            print("❌ 错误：当前不在学期时间内，无法初始化日程。")
            self.current_week = 0
            self.semester_id = 0
        else:
            self.current_week = int(self.timenow.week)
            self.semester_id = self.timenow.semester_id

        self.week_dates = get_current_week_dates()
        
        if self.semester_id:
            self.refresh_tree()

    def refresh_tree(self):
        self.tree = SegmentTree(TOTAL_TREE_SIZE)
        
        courses = load_course_data(self.classroom_id, self.semester_id)
        reservations = load_reservation_data(self.classroom_id, self.semester_id, self.week_dates)

        for c in courses:
            if int(c.week_start) <= self.current_week <= int(c.week_end):
                start_idx = get_tree_index(c.start_timeslot_id)
                end_idx = get_tree_index(c.end_timeslot_id)
                
                if start_idx != -1 and end_idx != -1:
                    self.tree.update(1, 0, TOTAL_TREE_SIZE - 1, start_idx, end_idx, 1)

        for r in reservations:
            start_idx = get_tree_index(r.start_timeslot_id)
            end_idx = get_tree_index(r.end_timeslot_id)
            
            if start_idx != -1 and end_idx != -1:
                self.tree.update(1, 0, TOTAL_TREE_SIZE - 1, start_idx, end_idx, 1)

    def check_conflict(self, start_id, end_id):
        l = get_tree_index(start_id)
        r = get_tree_index(end_id)

        if l == -1 or r == -1:
            print("❌ 节次 ID 无效")
            return True
        if l > r:
            print("❌ 开始时间不能晚于结束时间")
            return True

        result = self.tree.query(1, 0, TOTAL_TREE_SIZE - 1, l, r)
        return result == 1

def reserve(classroom_id, user_id, user_name, date_str, start_ts_id, end_ts_id):
    """
    执行预约的核心业务逻辑
    """
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        # 1. 前置检查
        cursor.execute("SELECT status FROM classrooms WHERE classroom_id = ?", (classroom_id,))
        row = cursor.fetchone()
        if not row:
            print("❌ 教室不存在")
            return False
        
        if row['status'] != 1:
            print(f"❌ 教室当前状态不可预约 (Status: {row['status']})")
            return False

        # 2. 冲突检测
        system = Schedule_System(classroom_id)
        
        if date_str not in system.week_dates:
            print("❌ 目前仅支持预约本周内的时间")
            return False
        
        req_weekday, _ = parse_timeslot_id(start_ts_id)
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        if req_weekday != date_obj.isoweekday():
            print(f"❌ 日期 {date_str} 与节次ID中的星期不匹配")
            return False

        if system.check_conflict(start_ts_id, end_ts_id):
            print(f"⚠️ 预约失败: {date_str} {start_ts_id} - {end_ts_id} (时间冲突)")
            return False

        # 3. DB 写入
        timenow = get_time()
        current_semester = timenow.semester_id if timenow else 0
        
        sql = '''
        INSERT INTO reservation
        (classroom_id, user_id, user_name, date, start_timeslot_id, end_timeslot_id, status, semester_id) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        '''
        
        cursor.execute(sql, (
            classroom_id,
            user_id,
            user_name,
            date_str,
            start_ts_id,
            end_ts_id,
            1, 
            current_semester
        ))

        # 4. 更新教室状态
        cursor.execute("UPDATE classrooms SET status = 1 WHERE classroom_id = ?", (classroom_id,))

        conn.commit()
        print(f"✅ 预约成功！{date_str} | {start_ts_id} 至 {end_ts_id}")
        return True

    except sqlite3.Error as e:
        print(f"❌ 数据库错误: {e}")
        conn.rollback()
        return False
    except Exception as e:
        print(f"❌ 未知错误: {e}")
        return False
    finally:
        conn.close()

def cancel(reservation_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE reservation SET status = -1 WHERE reservation_id = ?", (reservation_id,))
        conn.commit()
        print("✅ 预约已取消")
        return True
    except Exception as e:
        print(f"取消失败: {e}")
        return False
    finally:
        conn.close()