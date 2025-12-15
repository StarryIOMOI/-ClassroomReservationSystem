import sqlite3
from core import Courses
from core import Reservation
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

    conn.close()
    return courses, reservations


