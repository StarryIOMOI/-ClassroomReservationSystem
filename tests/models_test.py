from src.models.data_db import init_db, prepare_path
from src.models.crud import load_special_semester_data

if __name__ == '__main__':
    # prepare_path()
    # init_db()
    semester = load_special_semester_data(2025-2026-1)
    print(f"{semester.id}{semester.name}{semester.start}{semester.end}{semester.week}")