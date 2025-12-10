import sqlite3
from models import get_connection

class TreeNode:
    def __init__(self, id, name, type):
        self.id = id
        self.name = name
        self.type = type
        self.children = {}

    def add_child(self, node):
        self.children[node.id] = node

    def __repr__(self):
        return f"TreeNode(id={self.id}, name={self.name}, type={self.type}, children={len(self.children)})"
    
class Buildings:
        def __init__(self, building_id, building_name, status):
             self.id = building_id
             self.name = building_name
             self.status = status
             
class Areas:
     def __init__(self, area_id, area_name, building_id, status):
          self.id = area_id
          self.name = area_name
          self.building_id = building_id
          self.status = status

class Floors:
     def __init__(self, floor_id, floor_name, area_id, status):
          self.id = floor_id
          self.name = floor_name
          self.area_id = area_id
          self.status = status

class Classrooms:
     def __init__(self, classroom_id, classroom_name, floor_id, status):
          self.id = classroom_id
          self.name = classroom_name
          self.floor_id = floor_id
          self.status = status

def load_data(): 
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

    cursor.execute("SELECT * FROM classrooms")
    classroom_rows = cursor.fetchall()

    classrooms = [
        Classrooms(row["classroom_id"], row["classroom_name"], row["floor_id"], row["status"])
        for row in classroom_rows
    ]

    conn.close()
    return buildings, classrooms

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