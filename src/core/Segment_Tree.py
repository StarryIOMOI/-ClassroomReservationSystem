class LessonSegmentTree:
    def __init__(self, total_slots):
        self.n = total_slots
        self.tree = [0] * (4 * (self.n + 1))
        self.lazy = [-1] * (4 * (self.n + 1))

    def pushdown(self, node, start, end):
        if self.lazy[node] != -1:
            mid = (start + end) // 2
            left, right = 2 * node, 2 * node + 1

            val = self.lazy[node]

            self.tree[left] = self.lazy[node] * (mid - start + 1)
            self.lazy[left] = val
            
            self.tree[right] = self.lazy[node] * (end - mid)
            self.lazy[right] = val
            
            self.lazy[node] = -1

    def update(self, L, R, val):
        self._update(1, 1, self.n, L, R, val)

    def _update(self, node, start, end, L, R, val):
        if L <= start and end <= R:
            self.tree[node] = val * (end - start + 1)
            self.lazy[node] = val
            return

        self.pushdown(node, start, end)
        mid = (start + end) // 2
        
        if L <= mid:
            self._update(2 * node, start, mid, L, R, val)
        if R > mid:
            self._update(2 * node + 1, mid + 1, end, L, R, val)
            
        self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]

    def query(self, L, R):
        return self._query(1, 1, self.n, L, R)

    def _query(self, node, start, end, L, R):
        if L <= start and end <= R:
            return self.tree[node]
        
        self.pushdown(node, start, end)
        mid = (start + end) // 2
        res = 0
        
        if L <= mid:
            res += self._query(2 * node, start, mid, L, R)
        if R > mid:
            res += self._query(2 * node + 1, mid + 1, end, L, R)
            
        return res