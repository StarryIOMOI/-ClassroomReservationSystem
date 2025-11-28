import sqlite3
import sys
import os

current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(current_dir)
from models import get_connection

def add_teacher_user(teacher_id, permission_level, password_hash, name, phone_number, email, class_name, club):
    """向数据库添加教师用户"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        sql = '''
            INSERT INTO teacher_users 
            (teacher_id, permission_level, password_hash, name, phone_number, email, class, club) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        '''
        
        cursor.execute(sql, (
            teacher_id, 
            permission_level, 
            password_hash, 
            name, 
            phone_number, 
            email, 
            class_name,
            club
        ))
        
        conn.commit()
        print(f"教师 {name} 添加成功！")
        return True

    except sqlite3.IntegrityError as e:
        print(f"添加失败：数据冲突。详细信息：{e}")
        return False
        
    except Exception as e:
        print(f"添加失败：发生未知错误 {e}")
        return False
        
    finally:
        conn.close()

def add_student_users(student_id, password_hash, name, class_name, phone_number, email):
    """向数据库添加学生用户"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        sql = '''
        INSERT INTO student_users 
        (student_id, password_hash, name, class, phone_number, email) 
        VALUES (?, ?, ?, ?, ?, ?)
        '''
        
        cursor.execute(sql, (
            student_id,
            password_hash,
            name,
            class_name,
            phone_number,
            email
        ))

        conn.commit()
        print(f"教师 {name} 添加成功！")
        return True
    
    except sqlite3.IntegrityError as e:
        print(f"添加失败：数据冲突。详细信息：{e}")
        return False
        
    except Exception as e:
        print(f"添加失败：发生未知错误 {e}")
        return False

    finally:
        conn.close()

def add_buildings(name):
    """向数据库添加教学楼"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        sql = '''
        INSERT INTO buildings 
        (name) 
        VALUES (?)
        '''
        
        cursor.execute(sql, (
            name
        ))

        cursor.execute(sql, (name,)) 
        conn.commit()
        print(f"教学楼 {name} 添加成功！")
        return True
    
    except sqlite3.IntegrityError as e:
        print(f"添加失败：数据冲突。详细信息：{e}")
        return False
        
    except Exception as e:
        print(f"添加失败：发生未知错误 {e}")
        return False

    finally:
        conn.close()

def add_areas(building_id, area_num):
    """向数据库添加教学楼区域"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        sql = '''
        INSERT INTO areas
        (building_id, area_num) 
        VALUES (?, ?)
        '''
        
        cursor.execute(sql, (
            building_id,
            area_num
        ))

        conn.commit()
        print(f"区域 {area_num} (Building ID: {building_id}) 添加成功！")
        return True
    
    except sqlite3.IntegrityError as e:
        print(f"添加失败：数据冲突。详细信息：{e}")
        return False
        
    except Exception as e:
        print(f"添加失败：发生未知错误 {e}")
        return False

    finally:
        conn.close()

def add_classrooms(area_id, floor, classroom_id):
    """向数据库添加教室"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        sql = '''
        INSERT INTO buildings 
        (area_id, floor, classroom_id) 
        VALUES (?, ?, ?)
        '''
        
        cursor.execute(sql, (
            area_id,
            floor,
            classroom_id
        ))
    
    except sqlite3.IntegrityError as e:
        print(f"添加失败：数据冲突。详细信息：{e}")
        return False
        
    except Exception as e:
        print(f"添加失败：发生未知错误 {e}")
        return False

    finally:
        conn.close()

def add_time_slot(class_num, start_time, end_time, sort_order):
    """向数据库添加课时时间段"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        sql = '''
        INSERT INTO time_slot 
        (class_num, start_time, end_time, sort_order)
        VALUES (?, ?, ?, ?)
        '''
        
        cursor.execute(sql, (
            class_num,
            start_time,
            end_time,
            sort_order
        ))
    
    except sqlite3.IntegrityError as e:
        print(f"添加失败：数据冲突。详细信息：{e}")
        return False
        
    except Exception as e:
        print(f"添加失败：发生未知错误 {e}")
        return False

    finally:
        conn.close()

def add_schedule_slot(classroom_id, target_date, slot_id, status, user_id, reason):
    """向数据库添加预约槽"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        sql = '''
        INSERT INTO schedule_slot 
        (classroom_id, target_date, slot_id, status, user_id, reason)
        VALUES (?, ?, ?, ?, ?, ?)
        '''
        
        cursor.execute(sql, (
            classroom_id,
            target_date,
            slot_id,
            status,
            user_id,
            reason
        ))
    
    except sqlite3.IntegrityError as e:
        print(f"添加失败：数据冲突。详细信息：{e}")
        return False
        
    except Exception as e:
        print(f"添加失败：发生未知错误 {e}")
        return False

    finally:
        conn.close()