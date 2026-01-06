import sqlite3
import sys
import os
from core.Class import Buildings
from core.Class import Areas
from core.Class import Floors
from core.Class import Classrooms
# import hashlib

current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(current_dir)
from models import get_connection

#========================================
# 用户管理模块
#========================================

def create_teacher_user(teacher_id, name, password_hash = "123456", phone_number = None, email = None, class_id = None, club_id = None, status = 0):
    """
    向数据库添加教师用户
    修正说明: 数据库字段为 class_id 和 club_id
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        sql = '''
            INSERT INTO teacher_users 
            (status, teacher_id, password_hash, name, phone_number, email, class_id, club_id) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        '''
        
        cursor.execute(sql, (
            status,
            teacher_id, 
            password_hash,
            name, 
            phone_number, 
            email, 
            class_id,
            club_id
        ))
        
        conn.commit()
        print(f"教师 {name} (ID: {teacher_id}) 添加成功！")
        return True

    except sqlite3.IntegrityError as e:
        print(f"添加教师失败：主键或唯一约束冲突 (ID/电话/邮箱可能已存在)。\n详细信息：{e}")
        return False
    except Exception as e:
        print(f"添加教师失败：发生未知错误 {e}")
        return False
    finally:
        conn.close()

def create_student_user(student_id, name, class_id, password_hash = "123456", phone_number = None, email = None, status = 0):
    """
    向数据库添加学生用户
    修正说明: 数据库字段为 class_id
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        sql = '''
        INSERT INTO student_users 
        (status, student_id, password_hash, name, class_id, phone_number, email) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
        '''
        
        cursor.execute(sql, (
            status,
            student_id,
            password_hash,
            name,
            class_id,
            phone_number,
            email
        ))

        conn.commit()
        print(f"学生 {name} (ID: {student_id}) 添加成功！")
        return True
    
    except sqlite3.IntegrityError as e:
        print(f"添加学生失败：主键或唯一约束冲突。\n详细信息：{e}")
        return False
    except Exception as e:
        print(f"添加学生失败：发生未知错误 {e}")
        return False
    finally:
        conn.close()

#========================================
# 空间资源管理模块
#========================================

def create_building(building_id, building_name, status = 1, description = None):
    """向数据库添加教学楼"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        sql = '''
        INSERT INTO buildings 
        (building_id, building_name, status, description) 
        VALUES (?, ?, ?, ?)
        '''
        cursor.execute(sql, (building_id, building_name, status, description))
        conn.commit()
        print(f"教学楼 {building_name} 添加成功！")
        return True
    except sqlite3.IntegrityError as e:
        print(f"添加教学楼失败：ID或名称已存在。\n详细信息：{e}")
        return False
    except Exception as e:
        print(f"添加教学楼失败：{e}")
        return False
    finally:
        conn.close()

def create_area(area_id, area_name, building_id, status = 1):
    """向数据库添加教学楼区域"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        sql = '''
        INSERT INTO areas 
        (area_id, area_name, building_id, status) 
        VALUES (?, ?, ?, ?)
        '''
        cursor.execute(sql, (area_id, area_name, building_id, status))
        conn.commit()
        print(f"区域 {area_name} 添加成功！")
        return True
    except sqlite3.IntegrityError as e:
        print(f"添加区域失败：ID冲突或所属教学楼ID不存在。\n详细信息：{e}")
        return False
    except Exception as e:
        print(f"添加区域失败：{e}")
        return False
    finally:
        conn.close()

def create_floor(floor_id, floor_name, area_id, status = 1):
    """向数据库添加楼层"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        sql = '''
        INSERT INTO floors 
        (floor_id, floor_name, area_id, status) 
        VALUES (?, ?, ?, ?)
        '''
        cursor.execute(sql, (floor_id, floor_name, area_id, status))
        conn.commit()
        print(f"楼层 {floor_name} 添加成功！")
        return True
    except sqlite3.IntegrityError as e:
        print(f"添加楼层失败：ID冲突或所属区域ID不存在。\n详细信息：{e}")
        return False
    except Exception as e:
        print(f"添加楼层失败：{e}")
        return False
    finally:
        conn.close()

def create_classroom(classroom_id, classroom_name, floor_id, type, status = 1, capacity = 30):
    """向数据库添加教室"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        sql = '''
        INSERT INTO classrooms 
        (classroom_id, classroom_name, floor_id, status, capacity, type) 
        VALUES (?, ?, ?, ?, ?, ?)
        '''
        cursor.execute(sql, (classroom_id, classroom_name, floor_id, status, capacity, type))
        conn.commit()
        print(f"教室 {classroom_name} 添加成功！")
        return True
    except sqlite3.IntegrityError as e:
        print(f"添加教室失败：ID冲突或所属楼层ID不存在。\n详细信息：{e}")
        return False
    except Exception as e:
        print(f"添加教室失败：{e}")
        return False
    finally:
        conn.close()

#========================================
# 数据资源管理模块
#========================================

def create_class(class_id, class_name):
    """
    向数据库添加班级
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        sql = '''
        INSERT INTO classes (class_id, class_name) 
        VALUES (?, ?)
        '''
        cursor.execute(sql, (class_id, class_name))
        conn.commit()
        print(f"✅ 班级 '{class_name}' (ID: {class_id}) 添加成功！")
        return True

    except sqlite3.IntegrityError as e:
        print(f"❌ 添加失败：班级ID '{class_id}' 或 名称 '{class_name}' 已存在。")
        return False
        
    except Exception as e:
        print(f"❌ 添加失败：发生错误 {e}")
        return False
        
    finally:
        conn.close()

#========================================
# 加载数据
#========================================
def load_building_data(): 
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM buildings")
    building_rows = cursor.fetchall()

    buildings = [
        Buildings(row["building_id"], row["building_name"], row["status"])
        for row in building_rows
    ]

    conn.close()
    return buildings

def load_area_data(): 
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM areas")
    area_rows = cursor.fetchall()

    areas = [
        Areas(row["area_id"], row["area_name"], row["building_id"], row["status"])
        for row in area_rows
    ]

    conn.close()
    return areas

def load_floor_data(): 
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM floors")
    floor_rows = cursor.fetchall()

    floors = [
        Floors(row["floor_id"], row["floor_name"], row["area_id"], row["status"])
        for row in floor_rows
    ]

    conn.close()
    return floors

def load_classroom_data(): 
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM .classrooms")
    classroom_rows = cursor.fetchall()

    classrooms = [
        Classrooms(row["classroom_id"], row["classroom_name"], row["floor_id"], row["status"])
        for row in classroom_rows
    ]

    conn.close()
    return classrooms

