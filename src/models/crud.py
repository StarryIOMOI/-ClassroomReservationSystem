import sqlite3
import sys
import os
from src.core.Class import (
    Buildings, Areas, Floors,
    Semesters, Classrooms, Timeslots
    )
# import hashlib

current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(current_dir)
from src.models.data_db import get_connection

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

def create_semester(semester_id, semester_name, date_start, date_end, total_weeks):
    """
    向数据库添加学期
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        sql = '''
        INSERT INTO semester 
        (semester_id, semester_name, date_start, date_end, total_weeks) 
        VALUES (?, ?, ?, ?, ?)
        '''
        
        cursor.execute(sql, (semester_id, semester_name, date_start, date_end, total_weeks))
        
        conn.commit()
        print(f"✅ 学期 '{semester_name}' 添加成功！")
        return True

    except sqlite3.IntegrityError:
        print(f"❌ 添加失败：学期ID '{semester_id}' 已存在。")
        return False
        
    except Exception as e:
        print(f"❌ 添加失败：发生错误 {e}")
        return False
        
    finally:
        conn.close()

def create_course(course_id, course_name, class_id, classroom_id, teacher_id, semester_id, start_timeslot_id, end_timeslot_id, week_start, week_end):
    """
    添加课程 (自动查找关联的名称)
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT class_name FROM classes WHERE class_id = ?", (class_id,))
        res_class = cursor.fetchone()
        if not res_class:
            print(f"❌ 失败：班级ID '{class_id}' 不存在")
            return False
        class_name = res_class[0]

        cursor.execute("SELECT classroom_name FROM classrooms WHERE classroom_id = ?", (classroom_id,))
        res_room = cursor.fetchone()
        if not res_room:
            print(f"❌ 失败：教室ID '{classroom_id}' 不存在")
            return False
        classroom_name = res_room[0]

        cursor.execute("SELECT name FROM teacher_users WHERE teacher_id = ?", (teacher_id,))
        res_teacher = cursor.fetchone()
        if not res_teacher:
            print(f"❌ 失败：教师ID '{teacher_id}' 不存在")
            return False
        teacher_name = res_teacher[0]

        sql = '''
        INSERT INTO courses (
            course_id, course_name, 
            class_id, class_name, 
            classroom_id, classroom_name, 
            teacher_id, teacher_name, 
            week_start, week_end, start_timeslot_id,
            end_timeslot_id, semester_id
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        
        cursor.execute(sql, (
            course_id, course_name,
            class_id, class_name,
            classroom_id, classroom_name,
            teacher_id, teacher_name,
            str(week_start), str(week_end), 
            start_timeslot_id, end_timeslot_id,
            semester_id
        ))
        
        conn.commit()
        print(f"✅ 课程 '{course_name}' ({course_id}) 添加成功！")
        return True

    except sqlite3.IntegrityError as e:
        print(f"❌ 添加失败：课程ID已存在 或 违反唯一约束。详情: {e}")
        return False
    except Exception as e:
        print(f"❌ 添加失败：{e}")
        return False
    finally:
        conn.close()

def create_timeslot(timeslot_id, weekday, start_time, end_time):
    """
    添加课程时间段
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        sql = '''
        INSERT INTO timeslot (timeslot_id, weekday, start_time, end_time) 
        VALUES (?, ?, ?, ?)
        '''
        cursor.execute(sql, (timeslot_id, weekday, start_time, end_time))
        conn.commit()
        print(f"✅ 时间槽 '{timeslot_id}' (周{weekday} {start_time}-{end_time}) 添加成功")
        return True
    
    except sqlite3.IntegrityError:
        print(f"❌ 添加失败：时间槽ID '{timeslot_id}' 已存在")
        return False
    except Exception as e:
        print(f"❌ 添加失败：{e}")
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

    cursor.execute("SELECT * FROM classrooms")
    classroom_rows = cursor.fetchall()

    classrooms = [
        Classrooms(row["classroom_id"], row["classroom_name"], row["floor_id"], row["status"])
        for row in classroom_rows
    ]

    conn.close()
    return classrooms

def load_class_data(): 
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM classes")
    class_rows = cursor.fetchall()

    classes = [
        Classrooms(row["class_id"], row["class_name"])
        for row in class_rows
    ]

    conn.close()
    return classes

def load_semester_data():
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM semester")
    semester_rows = cursor.fetchall()

    semesters = [
        Semesters(row["semester_id"], row["semester_name"], row["date_start"], row["date_end"], row["total_week"])
        for row in semester_rows
    ]

    conn.close()
    return semesters

def load_timeslots_data():
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM timeslot")
    timeslot_rows = cursor.fetchall()

    timeslots = [
        Timeslots(row["timeslot_id"], row["weekday"], row["start_time"], row["end_time"])
        for row in timeslot_rows
    ]

    conn.close()
    return timeslots

def load_special_semester_data(semester_id):
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM  reservation
        WHERE semester_id = ?
    """, (semester_id,))

    semester_rows = cursor.fetchall()

    semesters = [
        Semesters(row["semester_id"], row["semester_name"], row["date_start"], row["date_end"], row["total_week"])
        for row in semester_rows
    ]

    conn.close()
    return semesters

#========================================
# 修改数据
#========================================
def activate_student_status(student_id, password):
    """
    激活学生账户：验证ID和密码，且仅当当前状态为0时，将其修改为1
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        sql_check = "SELECT password_hash, status, name FROM student_users WHERE student_id = ?"
        cursor.execute(sql_check, (student_id,))
        row = cursor.fetchone()

        if not row:
            print(f"❌ 激活失败：找不到学生 ID '{student_id}'")
            return False

        stored_password, current_status, name = row

        if str(stored_password) != str(password):
            print(f"❌ 激活失败：密码错误")
            return False

        if current_status != 0:
            print(f"⚠️ 激活失败：学生 '{name}' 当前状态为 {current_status} (非0)，无需激活")
            return False
        
        new_password = input("激活账号请输入新密码:")

        sql_update = "UPDATE student_users SET status = 1 WHERE student_id = ?"
        cursor.execute(sql_update, (student_id,))
        sql_update = "UPDATE student_users SET password_hash = ? WHERE student_id = ?"
        cursor.execute(sql_update, (new_password, student_id))
        conn.commit()
        
        print(f"✅ 成功：学生 '{name}' ({student_id}) 状态已激活 (0 -> 1)")
        return True

    except Exception as e:
        print(f"❌ 系统错误：{e}")
        return False
    finally:
        conn.close()


def activate_teacher_status(teacher_id, password):
    """
    激活教师账户：验证ID和密码，且仅当当前状态为0时，将其修改为1
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        sql_check = "SELECT password_hash, status, name FROM teacher_users WHERE teacher_id = ?"
        cursor.execute(sql_check, (teacher_id,))
        row = cursor.fetchone()

        if not row:
            print(f"❌ 激活失败：找不到教师 ID '{teacher_id}'")
            return False

        stored_password, current_status, name = row

        if str(stored_password) != str(password):
            print(f"❌ 激活失败：密码错误")
            return False

        if current_status != 0:
            print(f"⚠️ 激活失败：教师 '{name}' 当前状态为 {current_status} (非0)，无需激活")
            return False

        new_password = input("激活账号请输入新密码:")

        sql_update = "UPDATE teacher_users SET status = 1 WHERE teacher_id = ?"
        cursor.execute(sql_update, (teacher_id,))
        sql_update = "UPDATE teacher_users SET password_hash = ? WHERE teacher_id = ?"
        cursor.execute(sql_update, (new_password, teacher_id))
        conn.commit()
        
        print(f"✅ 成功：教师 '{name}' ({teacher_id}) 状态已激活 (0 -> 1)")
        return True

    except Exception as e:
        print(f"❌ 系统错误：{e}")
        return False
    finally:
        conn.close()

def new_student_password(student):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        sql_check = "SELECT password_hash, name FROM student_users WHERE student_id = ?"
        cursor.execute(sql_check, (student.id,))
        
        new_password1 = input("请输入新密码:")
        new_password2 = input("请确认新密码:")

        if new_password1 == new_password2:
            sql_update = "UPDATE student_users SET password_hash = ? WHERE student_id = ?"
            cursor.execute(sql_update, (new_password1, student.id))
            conn.commit()
        
            print(f"✅ 学生 '{student.name}' ({student.id})成功修改密码 ")
            return True
        
        else:
            print(f"❌ 修改失败：两次密码不相同")
            return

    except Exception as e:
        print(f"❌ 系统错误：{e}")
        return False
    finally:
        conn.close()

def new_teacher_password(teacher):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        sql_check = "SELECT password_hash, name FROM teacher_users WHERE teacher_id = ?"
        cursor.execute(sql_check, (teacher.id,))
        
        new_password1 = input("请输入新密码:")
        new_password2 = input("请确认新密码:")

        if new_password1 == new_password2:
            sql_update = "UPDATE teacher_users SET password_hash = ? WHERE teacher_id = ?"
            cursor.execute(sql_update, (new_password1, teacher.id))
            conn.commit()
        
            print(f"✅ 教师 '{teacher.name}' ({teacher.id})成功修改密码 ")
            return True
        
        else:
            print(f"❌ 修改失败：两次密码不相同")
            return

    except Exception as e:
        print(f"❌ 系统错误：{e}")
        return False
    finally:
        conn.close()

#========================================
# 临时数据
#========================================

courses_by_department = {
    "计算机": [
        ("计算机导论", "0101"),
        ("数据结构", "0102"),
        ("算法设计", "0103"),
        ("数据库系统", "0104"),
        ("计算机网络", "0105"),
        ("软件工程", "0106"),
        ("操作系统", "0107"),
        ("人工智能", "0108"),
        ("计算机图形学", "0109"),
        ("编译原理", "0110")
    ],
    "外语": [
        ("英语精读", "0201"),
        ("英语写作", "0202"),
        ("英语翻译", "0203"),
        ("英语口语", "0204"),
        ("英语文学", "0205"),
        ("法语入门", "0206"),
        ("德语基础", "0207"),
        ("日语初级", "0208"),
        ("西班牙语", "0209"),
        ("俄语基础", "0210")
    ],
    "数学": [
        ("高等数学", "0301"),
        ("线性代数", "0302"),
        ("概率论", "0303"),
        ("数理统计", "0304"),
        ("离散数学", "0305"),
        ("数学分析", "0306"),
        ("复变函数", "0307"),
        ("微分方程", "0308"),
        ("实变函数", "0309"),
        ("拓扑学", "0310")
    ],
    "物理": [
        ("大学物理", "0401"),
        ("力学", "0402"),
        ("电磁学", "0403"),
        ("光学", "0404"),
        ("热学", "0405"),
        ("量子力学", "0406"),
        ("相对论", "0407"),
        ("固体物理", "0408"),
        ("计算物理", "0409"),
        ("实验物理", "0410")
    ],
    "马克思": [
        ("马克思主义原理", "0501"),
        ("毛泽东思想概论", "0502"),
        ("中国特色社会主义理论", "0503"),
        ("思想道德修养", "0504"),
        ("中国近现代史纲要", "0505"),
        ("政治经济学", "0506"),
        ("科学社会主义", "0507"),
        ("哲学原理", "0508"),
        ("伦理学基础", "0509"),
        ("法学概论", "0510")
    ]
}

def print_course_table():
    """打印课程编号表"""
    print("课程编号表")
    print("=" * 50)
    print("课程,id")
    
    for dept, courses in courses_by_department.items():
        print(f"\n【{dept}学院】")
        
        for i in range(0, len(courses), 3):
            row_courses = courses[i:i+3]
            
            row_str = ""
            for course_name, course_id in row_courses:
                row_str += f"{course_name}:{course_id}  "
            
            print(row_str.rstrip())