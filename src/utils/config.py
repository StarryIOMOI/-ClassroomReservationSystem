import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, "data", "data.db")

# print("项目根目录:", BASE_DIR)
# print("数据库路径:", DB_PATH)