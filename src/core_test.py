from core import Buildings
from core import Areas
from core import Floors
from core import Classrooms
from core import build_tree

def print_tree(node, indent=""):
    print(f"{indent}└── {node.name} (id={node.id}, type={node.type})")
    for i, child in enumerate(node.children.values()):
        if i == len(node.children) - 1:
            print_tree(child, indent + "    ")
        else:
            print_tree(child, indent + "│   ")

if __name__ == "__main__":
    # 示例数据
    buildings = [
        Buildings(1, "A栋 主楼", 1),
        Buildings(2, "B栋 实验楼", 1),
    ]

    areas = [
        Areas(101, "北区", 1, 1),
        Areas(102, "南区", 1, 1),
        Areas(201, "东区", 2, 1),
    ]

    floors = [
        Floors(1001, "1层", 101, 1),
        Floors(1002, "2层", 101, 1),
        Floors(1003, "1层", 102, 1),
        Floors(2001, "1层", 201, 1),
    ]

    classrooms = [
        Classrooms(5001, "101教室", 1001, 1),
        Classrooms(5002, "102教室", 1001, 1),
        Classrooms(5003, "201教室", 1002, 1),
        Classrooms(5004, "105教室", 1003, 1),
        Classrooms(5005, "实验室A", 2001, 1),
    ]

    # 构建树
    campus_tree = build_tree(buildings, areas, floors, classrooms)

    # 打印树结构
    print("校园层级结构：")
    print_tree(campus_tree)