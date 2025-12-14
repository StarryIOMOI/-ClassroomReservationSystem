class SegmentTree:
    def __init__(self, size):
        self.size = size
        # tree: 记录区间状态 (0:空闲, 1:被占用)
        # 只要区间内有任意一个时间片被占用，该节点就为 1 (OR逻辑)
        self.tree = [0] * (4 * size)
        # lazy: 延迟标记 (-1:无操作, 0:置空, 1:置满)
        self.lazy = [-1] * (4 * size)

    def _push_up(self, node):
        """父节点状态 = 左孩子 OR 右孩子"""
        self.tree[node] = self.tree[2 * node] | self.tree[2 * node + 1]

    def _push_down(self, node):
        """下发 Lazy Tag"""
        if self.lazy[node] != -1:
            tag = self.lazy[node]
            left, right = 2 * node, 2 * node + 1
            
            self.tree[left] = tag
            self.tree[right] = tag
            self.lazy[left] = tag
            self.lazy[right] = tag
            
            self.lazy[node] = -1

    def update(self, node, start, end, l, r, val):
        """区间修改：将 [l, r] 设置为 val"""
        if l <= start and end <= r:
            self.tree[node] = val
            self.lazy[node] = val
            return

        self._push_down(node)
        mid = (start + end) // 2
        
        if l <= mid:
            self.update(2 * node, start, mid, l, r, val)
        if r > mid:
            self.update(2 * node + 1, mid + 1, end, l, r, val)
            
        self._push_up(node)

    def query(self, node, start, end, l, r):
        """区间查询：返回 1 表示有冲突, 0 表示完全空闲"""
        if l <= start and end <= r:
            return self.tree[node]

        self._push_down(node)
        mid = (start + end) // 2
        res = 0
        
        if l <= mid:
            res |= self.query(2 * node, start, mid, l, r)
        if r > mid:
            res |= self.query(2 * node + 1, mid + 1, end, l, r)
            
        return res

    def book(self, l, r):
        # 先查是否有冲突
        if self.query(1, 0, self.size - 1, l, r) == 1:
            return False
        # 无冲突，执行占用
        self.update(1, 0, self.size - 1, l, r, 1)
        return True

    def cancel(self, l, r):
        self.update(1, 0, self.size - 1, l, r, 0)