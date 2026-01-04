import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, "data", "data.db")

def clear_screen():
    """跨平台清屏"""
    os.system('cls' if os.name == 'nt' else 'clear')

def pause():
    """暂停，等待用户按回车，用于展示操作结果"""
    input("\n按回车键继续...")

# print("项目根目录:", BASE_DIR)
# print("数据库路径:", DB_PATH)