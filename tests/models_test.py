from src.models.data_db import init_db, prepare_path

if __name__ == '__main__':
    prepare_path()
    init_db()