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