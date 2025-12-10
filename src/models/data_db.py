import sqlite3
import sys
import os

current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(current_dir)
from utils import DB_PATH
db_name = 'data.db'

def get_connection():
    return sqlite3.connect(DB_PATH)

def prepare_path():
    print("Checking the parent file of the database")

    if os.path.exists(os.path.dirname(DB_PATH)):
        print("'data' file was ready")
    else:
        print(f"path error: missing 'data' file in {os.path.dirname(DB_PATH)}")
        print(f"gonna create 'data' file in {os.path.dirname(DB_PATH)}")
        os.makedirs(os.path.dirname(DB_PATH))

def init_db():
    print("whether been initialized")
    if os.path.exists(DB_PATH):
        print(f"{DB_PATH} has already been built")
    else:
        print("Initializing data.db")
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS teacher_users (
            status INTEGER NOT NULL, 
            teacher_id TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            name TEXT NOT NULL,
            phone_number TEXT,
            email TEXT,
            class TEXT,
            club_id TEXT,
            Recovery_code TEXT,
                       
            CONSTRAINT uniq_teacher_id UNIQUE (teacher_id),
            CONSTRAINT uniq_phone UNIQUE (phone_number),
            CONSTRAINT uniq_email UNIQUE (email)
        );
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS student_users (
            status INTEGER NOT NULL, 
            student_id TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            name TEXT NOT NULL,
            class_id TEXT NOT NULL,
            phone_number TEXT,
            email TEXT,
            Recovery_code TEXT,
                       
            CONSTRAINT uniq_student_id UNIQUE (student_id),
            CONSTRAINT uniq_phone UNIQUE (phone_number),
            CONSTRAINT uniq_email UNIQUE (email)
        );
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS class (
            class_id TEXT NOT NULL,
            class_name TEXT NOT NULL,
            
                       
            CONSTRAINT uniq_class_id UNIQUE (class_id),
            CONSTRAINT uniq_class_name UNIQUE (class_name)
        );
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS buildings (
            building_id TEXT NOT NULL,
            building_name TEXT NOT NULL,
            status INTEGER NOT NULL,
            describe TEXT,
            
            CONSTRAINT uniq_building_id UNIQUE (building_id),
            CONSTRAINT uniq_building_name UNIQUE (building_name)
        );
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS areas (
            area_id TEXT NOT NULL,
            area_name TEXT NOT NULL,
            building_id TEXT NOT NULL,    
            status INTEGER NOT NULL,
            
            CONSTRAINT uniq_area_id UNIQUE (area_id),
        );
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS floors (
            floor_id TEXT NOT NULL,
            floor_name TEXT NOT NULL,
            area_id TEXT NOT NULL,
            status INTEGER NOT NULL,
            
            CONSTRAINT uniq_floor_id UNIQUE (floor_id),
        );
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS classrooms (
            classroom_id TEXT NOT NULL,
            classroom_name TEXT NOT NULL,
            floor_id TEXT NOT NULL,
            status INTEGER NOT NULL,
            capacity INTEGER,
            type TEXT,
            
            CONSTRAINT uniq_classroom_id UNIQUE (classroom_id)
        );
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            course_id INTEGER NOT NULL,
            course_name TEXT NOT NULL,
            teacher_id TEXT NOT NULL
            class TEXT NOT NULL,
            week_start TEXT NOT NULL,
            week_end TEXT NOT NULL,
                       
            CONSTRAINT uniq_course_id UNIQUE (course_id)
        );
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS timeslot (
            timeslot_id INTEGER NOT NULL,
            weekday INTEGER NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
                       
            CONSTRAINT uniq_timeslot_id UNIQUE (timeslot_id)
        );
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS schedule (
            schedule_id INTEGER NOT NULL,
            course_id INTEGER NOT NULL,
            teacher_id INTEGER NOT NULL,
            classroom_id INTEGER NOT NULL,
            timeslot_id INTEGER NOT NULL,
            
                       
            CONSTRAINT uniq_schedule_id UNIQUE (schedule_id)
        );
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS reservation (
            reservation_id INTEGER NOT NULL,
            classroom_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            data TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            status INTEGER NOT NULL,
                       
            CONSTRAINT uniq_schedule_id UNIQUE (reservation_id)
        );
        ''')

        conn.commit()
        conn.close()
        print(f"数据库 {db_name} 定义完成。")