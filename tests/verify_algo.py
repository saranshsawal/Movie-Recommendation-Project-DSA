import json

print("Testing Python environment...")

# Test MinHeap
class MinHeap:
    def __init__(self):
        self.heap = []
    def push(self, val):
        self.heap.append(val)
        self._up(len(self.heap) - 1)
    def pop(self):
        if not self.heap: return None
        top = self.heap[0]
        bot = self.heap.pop()
        if self.heap:
            self.heap[0] = bot
            self._down(0)
        return top
    def _up(self, i):
        while i > 0:
            p = (i - 1) // 2
            if self.heap[i] < self.heap[p]:
                self.heap[i], self.heap[p] = self.heap[p], self.heap[i]
                i = p
            else: break
    def _down(self, i):
        n = len(self.heap)
        while True:
            l, r, s = 2*i + 1, 2*i + 2, i
            if l < n and self.heap[l] < self.heap[s]: s = l
            if r < n and self.heap[r] < self.heap[s]: s = r
            if s != i:
                self.heap[i], self.heap[s] = self.heap[s], self.heap[i]
                i = s
            else: break

h = MinHeap()
for x in [5, 2, 8, 1, 9, 3]: h.push(x)
res = []
while h.heap: res.append(h.pop())
assert res == [1, 2, 3, 5, 8, 9]
print("[PASS] MinHeap verified:", res)

# Test Knapsack DP
items = [{'runtime': 90, 'value': 80}, {'runtime': 120, 'value': 95}, {'runtime': 60, 'value': 60}]
capacity = 210
n = len(items)
dp = [[0]*(capacity+1) for _ in range(n+1)]
for i in range(1, n+1):
    w = items[i-1]['runtime']
    v = items[i-1]['value']
    for cap in range(capacity+1):
        if w <= cap: dp[i][cap] = max(dp[i-1][cap], dp[i-1][cap-w] + v)
        else: dp[i][cap] = dp[i-1][cap]
assert dp[n][capacity] == 175
print("[PASS] 0/1 Knapsack DP verified. Max value:", dp[n][capacity])

# Test Union Find
class UnionFind:
    def __init__(self):
        self.p, self.r = {}, {}
    def find(self, x):
        if x not in self.p:
            self.p[x] = x
            self.r[x] = 0
        if self.p[x] != x:
            self.p[x] = self.find(self.p[x])
        return self.p[x]
    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry: return False
        if self.r[rx] < self.r[ry]: self.p[rx] = ry
        elif self.r[rx] > self.r[ry]: self.p[ry] = rx
        else:
            self.p[ry] = rx
            self.r[rx] += 1
        return True

uf = UnionFind()
uf.union("Drishyam (Mal)", "Drushyam (Tel)")
uf.union("Drushyam (Tel)", "Drishyam (Hin)")
assert uf.find("Drishyam (Mal)") == uf.find("Drishyam (Hin)")
print("[PASS] Union-Find Path Compression & Rank verified.")
print("[ALL DSA TESTS PASSED!]")

