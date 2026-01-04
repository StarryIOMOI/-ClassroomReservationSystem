import sqlite3
from core import Courses
from models import get_connection

def load_courses_data(class_id, teacher_id): 
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    if teacher_id == 0:
        cursor.execute("""
            SELECT * FROM courses
            WHERE class_id = ?
        """, (class_id,))
        course_rows = cursor.fetchall()

        courses = [
            Courses(row["course_id"], row["course_name"], row["class_id"], row["class_name"],
                    row["classroom_id"], row["classroom_name"], row["teacher_id"], row["teacher_name"],
                    row["week_start"], row["week_end"], row["timeslot_id"], row["semester_id"],)
            for row in course_rows
        ]

    if class_id == 0:
        cursor.execute("""
            SELECT * FROM courses
            WHERE teacher_id = ?
        """, (teacher_id,))
        course_rows = cursor.fetchall()

        courses = [
            Courses(row["course_id"], row["course_name"], row["class_id"], row["class_name"],
                    row["classroom_id"], row["classroom_name"], row["teacher_id"], row["teacher_name"],
                    row["week_start"], row["week_end"], row["timeslot_id"], row["semester_id"],)
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