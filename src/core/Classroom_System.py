import sqlite3
from src.core.Tree import TreeNode
from src.models.crud import (
    load_building_data, load_area_data,
    load_floor_data, load_classroom_data
    )

def build_tree():
    buildings = load_building_data()
    areas = load_area_data()
    floors = load_floor_data()
    classrooms = load_classroom_data()

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

def query_building_by_id(root_node):
    print("\n--- 查询教学楼详情 ---")
    user_input = input("请输入教学楼 ID: ").strip()

    if not user_input.isdigit():
        print("❌ 错误: 请输入纯数字 ID。")
        return

    target_id = int(user_input)

    target_building = root_node.children.get(target_id)

    if target_building:
        print(f"\n✅ 找到教学楼，结构如下:\n")
        print_tree_recursive(target_building)
        print("\n" + "-"*30)
    else:
        print(f"❌ 未找到 ID 为 {target_id} 的教学楼。")