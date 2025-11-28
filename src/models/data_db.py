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

        #==================================================
        #   学生和教师用户初始化
        #==================================================

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS teacher_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            teacher_id TEXT NOT NULL,
            permission_level INTEGER NOT NULL,
            password_hash TEXT NOT NULL,
            name TEXT NOT NULL,
            phone_number TEXT,
            email TEXT,
            class TEXT,
            club TEXT,
                       
            CONSTRAINT uniq_teacher_id UNIQUE (teacher_id),
            CONSTRAINT uniq_phone UNIQUE (phone_number),
            CONSTRAINT uniq_email UNIQUE (email)
        );
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS student_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            name TEXT NOT NULL,
            class TEXT NOT NULL,
            phone_number TEXT,
            email TEXT,
                       
            CONSTRAINT uniq_student_id UNIQUE (student_id),
            CONSTRAINT uniq_phone UNIQUE (phone_number),
            CONSTRAINT uniq_email UNIQUE (email)
        );
        ''')

        #==================================================
        #   学校教学楼教室信息初始化
        #==================================================

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS buildings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
                       
            CONSTRAINT uniq_name UNIQUE (name)
        );
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS areas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            building_id INTEGER NOT NULL,
            area_num TEXT NOT NULL,
                       
            FOREIGN KEY (building_id) REFERENCES buildings(id) ON DELETE CASCADE,
            CONSTRAINT uniq_building_area UNIQUE (building_id, area_num)
        );
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS classrooms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            area_id INTEGER NOT NULL,
            floor INTEGER NOT NULL,
            classroom_id TEXT NOT NULL,
                       
            FOREIGN KEY (area_id) REFERENCES areas(id) ON DELETE CASCADE,
            CONSTRAINT uniq_area_classroom UNIQUE (area_id, classroom_id)
        );
        ''')

        #==================================================
        #   预约时间表信息初始化
        #==================================================

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS time_slot (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            class_num TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            sort_order INTEGER NOT NULL,
            
            CONSTRAINT uniq_class_num UNIQUE (class_num),
            CONSTRAINT uniq_sort_order UNIQUE (sort_order)
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS schedule_slot (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
        
            classroom_id INTEGER NOT NULL,
            target_date TEXT NOT NULL,      -- 格式 YYYY-MM-DD
            slot_id INTEGER NOT NULL,
        
            status INTEGER DEFAULT 0,       -- 0:空闲(Free), 1:占用(Booked), 2:锁定/维修(Locked)
        
            user_id INTEGER,
            reason TEXT,

            FOREIGN KEY (classroom_id) REFERENCES classrooms(id),
            FOREIGN KEY (slot_id) REFERENCES time_slot(sort_order),
            FOREIGN KEY (user_id) REFERENCES teacher_users(id)
        );
        ''')

        conn.commit()
        conn.close()
        print(f"数据库 {db_name} (全量槽位模式) 定义完成。")