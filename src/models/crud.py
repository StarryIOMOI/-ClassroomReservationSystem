import sqlite3
import sys
import os
# import hashlib

current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(current_dir)
from models import get_connection

#========================================
#添加模块
#========================================
def create_teacher_user(teacher_id, name, phone_number = None, email = None, class_name = None, club = None, password_hash = 12345, status = 0):     #服务对象：管理员（添加教师）
    """向数据库添加教师用户"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        sql = '''
            INSERT INTO teacher_users 
            (status, teacher_id, password_hash, name, phone_number, email, class, club) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        '''
        
        cursor.execute(sql, (
            status,
            teacher_id, 
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

def create_student_users(student_id, name, class_name, password_hash = 12345, phone_number = None, email = None, status = 0):    #服务对象：管理员（添加学生）
    """向数据库添加学生用户"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        sql = '''
        INSERT INTO student_users 
        (status, student_id, password_hash, name, class, phone_number, email) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
        '''
        
        cursor.execute(sql, (
            status,
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

