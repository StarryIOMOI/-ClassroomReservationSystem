class RBTreeNode:
    def __init__(self, key, value):    #定义新节点格式
        self.key = key
        self.value = value
        self.color = 'red'    # 新节点默认为红色
        self.left = None
        self.right = None
        self.parent = None

class RBTree:
    def __init__(self):    #定义空节点
        self.nil = RBTreeNode(None, None)
        self.nil.color = 'black'
        self.nil.left = self.nil
        self.nil.right = self.nil
        self.nil.parent = self.nil
        self.root = self.nil

    def left_rotate(self, x):   #红黑树左旋
        y = x.right
        x.right = y.left
        if y.left != self.nil:
            y.left.parent = x
        y.parent = x.parent
        if x.parent == self.nil:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self, y):    #红黑树右旋
        x = y.left
        y.left = x.right
        if x.right != self.nil:
            x.right.parent = y
        x.parent = y.parent
        if y.parent == self.nil:
            self.root = x
        elif y == y.parent.right:
            y.parent.right = x
        else:
            y.parent.left = x
        x.right = y
        y.parent = x

    def rb_add(self, key, value):    #添加新节点
        if self.find_key(key) is not None:    #检查是否有重复键值
            print(f"错误：键值{key}已经存在，无法重复添加！")
            return
    
        z = RBTreeNode(key, value)    #将z设为哨兵节点，避免指向空值导致崩溃
        z.parent = self.nil
        z.left = self.nil
        z.right = self.nil

        y = self.nil
        x = self.root

        while x != self.nil:
            y = x
            if z.key < x.key:
                x = x.left
            else:
                x = x.right

        z.parent = y
        if y == self.nil:
            self.root = z
        elif z.key < y.key:
            y.left = z
        else:
            y.right = z
            
        z.left = self.nil
        z.right = self.nil

        self.add_rb_fixup(z)
    
    

    def rb_delete(self, key):    #删除特定节点
        z = self.root

        while z != self.nil:    #查找要删除的节点
            if key < z.key:
                z = z.left
            elif key > z.key:
                z = z.right
            else:
                break
            
        if z == self.nil:    #如果节点不存在
            print(f"错误：键值 {key} 不存在！")
            return
    
        y = z
        original_color = y.color

        if z.left == self.nil:
            x = z.right
            self.rb_delete_replace(z, x)
        elif z.right == self.nil:
            x = z.left
            self.rb_delete_replace(z, x)
        else:
            y = self.rb_delete_minimum(z.right)
            original_color = y.color
            x = y.right

            if y.parent == z:
                x.parent = y
            else:
                self.rb_delete_replace(y, x)
                y.right = z.right
                y.right.parent = y

            self.rb_delete_replace(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color

        if original_color == 'black':
            self.rb_delete_fixup(x)

    def print_tree(self):    #中序遍历打印红黑树
        if self.root == self.nil:
            print("红黑树为空。")
        else:
            print("红黑树内容 (中序遍历):")
            self.inorder_traversal_print(self.root)

    def add_rb_fixup(self, z):    #修复添加红黑树节点时造成的破坏
        while z.parent.color == 'red':
            if z.parent == z.parent.parent.left:    # 情况 A: 父节点是祖父节点的左孩子
                y = z.parent.parent.right   # 叔叔节点
                if y.color == 'red':    # Case 1: 叔叔是红色
                    z.parent.color = 'black'
                    y.color = 'black'
                    z.parent.parent.color = 'red'
                    z = z.parent.parent
                else:
                    if z == z.parent.right:    # Case 2: 当前节点是右孩子（三角关系）
                        z = z.parent
                        self.left_rotate(z)    # 当前节点变成左孩子
                    # Case 3: 当前节点是左孩子（直线关系）
                    z.parent.color = 'black'
                    z.parent.parent.color = 'red'
                    self.right_rotate(z.parent.parent)
            else:   # 情况 B: 父节点是祖父节点的右孩子 (与情况A对称)
                y = z.parent.parent.left  # 叔叔节点
                if y.color == 'red':    # Case 1: 叔叔是红色
                    z.parent.color = 'black'
                    y.color = 'black'
                    z.parent.parent.color = 'red'
                    z = z.parent.parent
                else:   # 叔叔是黑色
                    if z == z.parent.left:  # Case 2: 当前节点是左孩子（三角关系）
                        z = z.parent
                        self.right_rotate(z)    # 当前节点变成右孩子
                    # Case 3: 当前节点是右孩子（直线关系）
                    z.parent.color = 'black'
                    z.parent.parent.color = 'red'
                    self.left_rotate(z.parent.parent)
            if z == self.root:
                break
        self.root.color = "black"

    def rb_delete_fixup(self, x):    #修复删除红黑树节点时造成的破坏
        while x != self.root and x.color == 'black':
            if x == x.parent.left:
                u = x.parent.right

                if u.color == 'red':    # Case 1: x 的兄弟 u 是红色的
                    u.color = 'black'
                    x.parent.color = 'red'
                    self.left_rotate(x.parent)
                    u = x.parent.right
                
                if u.left.color == 'black' and u.right.color == 'black':    # Case 2: 当 x 的兄弟节点是黑色且他的两个子节点都是黑色
                    u.color = 'red'
                    x = x.parent    #现有节点已经符合规则，但整体仍然存在漏洞，将修改地点上移，寻求新的修改点
                else:
                    if u.right.color == 'red':    # Case 3: x 的兄弟节点 u 是黑色的，u 的左孩子是红色的，右孩子是黑色的
                        u.left.color = 'black'
                        u.color = 'red'
                        self.right_rotate(u)
                        u = x.parent.right
                    
                    u.color = x.parent.color    # Case 4: x 的兄弟节点 u 是黑色的，且 u 的右孩子是红色的
                    x.parent.color = 'black'
                    u.right.color = 'black'
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                u = x.parent.left

            if u.color == 'red':    # Case 1: x 的兄弟 u 是红色的
                u.color = 'black'
                x.parent.color = 'red'
                self.right_rotate(x.parent)
                u = x.parent.left

            if u.right.color == 'black' and u.left.color == 'black':    # Case 2: 当兄弟节点是黑色且他的两个子节点都是黑色
                u.color = 'red'
                x = x.parent    #现有节点已经符合规则，但整体仍然存在漏洞，将修改地点上移，寻求新的修改点
            else:
                if u.left.color == 'black':    # Case 3: x 的兄弟节点 u 是黑色的，u 的右孩子是红色的，左孩子是黑色的
                    u.right.color = 'black'
                    u.color = 'red'
                    self.left_rotate(u)
                    u = x.parent.left
                
                u.color = x.parent.color    # Case 4: x 的兄弟节点 u 是黑色的，且 u 的左孩子是红色的
                x.parent.color = 'black'
                u.left.color = 'black'
                self.right_rotate(x.parent)
                x = self.root

        x.color = 'black' 
    
    def rb_delete_replace(self, target_node, replace_node):    #替换特定节点
        if target_node.parent == self.nil:
            self.root = replace_node
        elif target_node == target_node.parent.left:
            target_node.parent.left = replace_node
        else:
            target_node.parent.right = replace_node
        
        replace_node.parent = target_node.parent

    def rb_delete_minimum(self, target_node):    #以目标节点为根，寻找其最小节点（即寻找目标节点子树中一个只有右子树的节点）
        while target_node.left != self.nil:
            target_node = target_node.left
        return target_node
    
    def find_key(self, key):    #查找特定节点
        target_node = self.root

        while target_node != self.nil:
            if key < target_node.key:
                target_node = target_node.left
            elif key > target_node.key:
                target_node = target_node.right
            else:
                return target_node
        
        return None
    
    def inorder_traversal_print(self, node):   #中序遍历红黑树
        if node != self.nil:
            self.inorder_traversal_print(node.left)
            print(f"  Key: {node.key}, Value: {node.value}, Color: {node.color}")
            self.inorder_traversal_print(node.right)