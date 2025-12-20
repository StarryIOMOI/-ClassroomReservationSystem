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

        #教室用户表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS teacher_users (
            status INTEGER NOT NULL, 
            teacher_id TEXT PRIMARY KEY,
            password_hash TEXT NOT NULL,
            name TEXT NOT NULL,
            phone_number TEXT,
            email TEXT,
            class_id TEXT,
            club_id TEXT,
            recovery_code TEXT,
                       
            CONSTRAINT uniq_teacher_id UNIQUE (teacher_id),
            CONSTRAINT uniq_phone UNIQUE (phone_number),
            CONSTRAINT uniq_email UNIQUE (email)
        );
        ''')

        #学生用户表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS student_users (
            status INTEGER NOT NULL, 
            student_id TEXT PRIMARY KEY,
            password_hash TEXT NOT NULL,
            name TEXT NOT NULL,
            class_id TEXT NOT NULL,
            phone_number TEXT,
            email TEXT,
            ecovery_code TEXT,
                       
            CONSTRAINT uniq_student_id UNIQUE (student_id),
            CONSTRAINT uniq_phone UNIQUE (phone_number),
            CONSTRAINT uniq_email UNIQUE (email)
        );
        ''')

        #班级表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS classes (
            class_id TEXT PRIMARY KEY,
            class_name TEXT NOT NULL,
            
                       
            CONSTRAINT uniq_class_id UNIQUE (class_id),
            CONSTRAINT uniq_class_name UNIQUE (class_name)
        );
        ''')

        #教学楼表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS buildings (
            building_id TEXT PRIMARY KEY,
            building_name TEXT NOT NULL,
            status INTEGER NOT NULL,
            description TEXT,
            
            CONSTRAINT uniq_building_id UNIQUE (building_id),
            CONSTRAINT uniq_building_name UNIQUE (building_name)
        );
        ''')

        #教学楼区域表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS areas (
            area_id TEXT PRIMARY KEY,
            area_name TEXT NOT NULL,
            building_id TEXT NOT NULL,    
            status INTEGER NOT NULL,
            
            CONSTRAINT uniq_area_id UNIQUE (area_id)
        );
        ''')

        #楼层表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS floors (
            floor_id TEXT PRIMARY KEY,
            floor_name TEXT NOT NULL,
            area_id TEXT NOT NULL,
            status INTEGER NOT NULL,
            
            CONSTRAINT uniq_floor_id UNIQUE (floor_id)
        );
        ''')

        #教室表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS classrooms (
            classroom_id TEXT PRIMARY KEY,
            classroom_name TEXT NOT NULL,
            floor_id TEXT NOT NULL,
            status INTEGER NOT NULL,
            capacity INTEGER,
            type TEXT,
            
            CONSTRAINT uniq_classroom_id UNIQUE (classroom_id)
        );
        ''')

        #学期表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS semester (
            semester_id TEXT PRIMARY KEY,
            semester_name TEXT NOT NULL,
            date_start TEXT NOT NULL,
            date_end TEXT NOT NULL,
            total_weeks TEXT NOT NULL,
                       
            CONSTRAINT uniq_semester_id UNIQUE (semester_id)
        );
        ''')

        #课程表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            course_id TEXT PRIMARY KEY,
            course_name TEXT NOT NULL,
            class_id TEXT NOT NULL,
            class_name TEXT NOT NULL,
            classroom_id TEXT NOT NULL,
            classroom_name TEXT NOT NULL,
            teacher_id TEXT NOT NULL,
            teacher_name TEXT NOY NULL,
            week_start TEXT NOT NULL,
            week_end TEXT NOT NULL,
            timeslot_id TEXT NOT NULL,
            semester_id TEXT NOT NULL,
                       
            CONSTRAINT uniq_course_id UNIQUE (course_id)
        );
        ''')

        #时间槽
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS timeslot (
            timeslot_id TEXT PRIMARY KEY,
            weekday INTEGER NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
                       
            CONSTRAINT uniq_timeslot_id UNIQUE (timeslot_id)
        );
        ''')

        #个人预约表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS reservation (
            reservation_id TEXT PRIMARY KEY,
            classroom_id TEXT NOT NULL,
            user_id TEXT NOT NULL,
            user_name TEXT NOT NULL,
            date TEXT NOT NULL,
            start TEXT NOT NULL,
            end TEXT NOT NULL,
            status INTEGER NOT NULL,
                       
            CONSTRAINT uniq_schedule_id UNIQUE (reservation_id)
        );
        ''')

        conn.commit()
        conn.close()
        print(f"数据库 {db_name} 定义完成。")