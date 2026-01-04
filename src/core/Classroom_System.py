import sqlite3
from .Tree import TreeNode
from .Class import Buildings
from .Class import Areas
from .Class import Floors
from .Class import Classrooms
from src.models import get_connection

def load_classroom_data(): 
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM buildings")
    building_rows = cursor.fetchall()

    buildings = [
        Buildings(row["building_id"], row["building_name"], row["status"])
        for row in building_rows
    ]

    cursor.execute("SELECT * FROM areas")
    area_rows = cursor.fetchall()

    areas = [
        Areas(row["area_id"], row["area_name"], row["building_id"], row["status"])
        for row in area_rows
    ]

    cursor.execute("SELECT * FROM floors")
    floor_rows = cursor.fetchall()

    floors = [
        Floors(row["floor_id"], row["floor_name"], row["area_id"], row["status"])
        for row in floor_rows
    ]

    cursor.execute("SELECT * FROM .classrooms")
    classroom_rows = cursor.fetchall()

    classrooms = [
        Classrooms(row["classroom_id"], row["classroom_name"], row["floor_id"], row["status"])
        for row in classroom_rows
    ]

    conn.close()
    return buildings, areas, floors, classrooms

def build_tree(buildings, areas, floors, classrooms):
    root = TreeNode(0, "Campus", "Campus")

    building_nodes = {}
    area_nodes = {}
    floor_nodes = {}

    for b in buildings: 
        bnode = TreeNode(b.id, b.name, "building")
        building_nodes[b.id] = bnode
        root.add_child(bnode)

    for a in areas:
        building_node = building_nodes[a.building_id]
        anode = TreeNode(a.id, a.name, "area")
        area_nodes[a.id] = anode
        building_node.add_child(anode)

    for f in floors:
        area_node = area_nodes[f.area_id]
        fnode = TreeNode(f.id, f.name, "floor")
        floor_nodes[f.id] = fnode
        area_node.add_child(fnode)

    for c in classrooms:
        floor_node = floor_nodes[c.floor_id]
        cnode = TreeNode(c.id, c.name, "classroom")
        floor_node.add_child(cnode)

    return root


def print_all_buildings_summary(root_node):
    all_buildings = root_node.children.values()
    
    print(f"📋 教学楼列表 (共 {len(all_buildings)} 栋)")
    print("-" * 50)
    print(f"{'ID':<5} | {'名称':<20} | {'下辖区域数':<10}")
    print("-" * 50)

    for node in all_buildings:
        print(f"{node.id:<5} | {node.name:<20} | {len(node.children):<10}")

    print("-" * 50)

def print_tree_recursive(node, prefix="", is_last=True):
    if prefix == "":
        connector = ""
    else:
        connector = "└── " if is_last else "├── "
    
    print(f"{prefix}{connector}[{node.type}] {node.name} (ID: {node.id})")

    if prefix == "":
        child_prefix = "" 
    else:
        child_prefix = prefix + ("    " if is_last else "│   ")

    children = list(node.children.values())
    count = len(children)
    
    for i, child in enumerate(children):
        is_last_child = (i == count - 1)
        print_tree_recursive(child, child_prefix, is_last_child)