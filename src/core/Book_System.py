import sqlite3
from core import Classrooms
from core import Courses
from core import Semesters
from models import get_connection

def load_classroom_data(): 
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()