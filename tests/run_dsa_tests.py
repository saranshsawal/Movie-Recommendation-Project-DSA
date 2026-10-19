import heapq
import json
import sys

# Force UTF-8 if available or use safe ASCII
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

class MinHeap:
    def __init__(self):
        self.heap = []

    def push(self, val):
        heapq.heappush(self.heap, val)

    def pop(self):
        return heapq.heappop(self.heap) if self.heap else None

    def is_empty(self):
        return len(self.heap) == 0


def dijkstra_shortest_path(graph, start, target_fn):
    dist = {start: 0}
    prev = {}
    pq = [(0, start)]

    while pq:
        d, u = heapq.heappop(pq)
        if target_fn(u):
            path = []
            curr = u
            while curr in prev:
                path.append(curr)
                curr = prev[curr]
            path.append(start)
            path.reverse()
            return {"path": path, "total_cost": d}

        if d > dist.get(u, float('inf')):
            continue

        for edge in graph.get(u, []):
            v = edge["node"]
            w = edge["weight"]
            alt = d + w
            if alt < dist.get(v, float('inf')):
                dist[v] = alt
                prev[v] = u
                heapq.heappush(pq, (alt, v))

    return {"path": [], "total_cost": float('inf')}


def solve_knapsack_01(items, capacity):
    n = len(items)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        runtime = items[i - 1]["runtime"]
        val = items[i - 1]["value"]
        for w in range(capacity + 1):
            if runtime <= w:
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - runtime] + val)
            else:
                dp[i][w] = dp[i - 1][w]

    selected = []
    rem_cap = capacity
    for i in range(n, 0, -1):
        if dp[i][rem_cap] != dp[i - 1][rem_cap]:
            selected.append(items[i - 1])
            rem_cap -= items[i - 1]["runtime"]

    selected.reverse()
    return {
        "max_value": dp[n][capacity],
        "used_capacity": capacity - rem_cap,
        "selected_items": selected
    }


class UnionFind:
    def __init__(self):
        self.parent = {}
        self.rank = {}

    def make_set(self, x):
        if x not in self.parent:
            self.parent[x] = x
            self.rank[x] = 0

    def find(self, x):
        self.make_set(x)
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        rx = self.find(x)
        ry = self.find(y)
        if rx == ry:
            return False
        if self.rank[rx] < self.rank[ry]:
            self.parent[rx] = ry
        elif self.rank[rx] > self.rank[ry]:
            self.parent[ry] = rx
        else:
            self.parent[ry] = rx
            self.rank[rx] += 1
        return True

    def connected(self, x, y):
        return self.find(x) == self.find(y)


if __name__ == "__main__":
    print("=" * 60)
    print("RUNNING CINEMATCH CORE DSA TESTS (NATIVE RUNNER)")
    print("=" * 60)

    # Test 1: MinHeap
    print("\n[Test 1] Testing MinHeap...")
    pq = MinHeap()
    for x in [5, 2, 8, 1, 9, 3]:
        pq.push(x)
    sorted_res = []
    while not pq.is_empty():
        sorted_res.append(pq.pop())
    assert sorted_res == [1, 2, 3, 5, 8, 9], f"MinHeap failed: {sorted_res}"
    print(f"[PASS] MinHeap push & pop ordering verified: {sorted_res}")

    # Test 2: Dijkstra
    print("\n[Test 2] Testing Dijkstra's Algorithm on small graph...")
    graph = {
        'A': [{'node': 'B', 'weight': 1}, {'node': 'C', 'weight': 4}],
        'B': [{'node': 'C', 'weight': 2}, {'node': 'D', 'weight': 5}],
        'C': [{'node': 'D', 'weight': 1}],
        'D': []
    }
    d_res = dijkstra_shortest_path(graph, 'A', lambda node: node == 'D')
    assert d_res["path"] == ['A', 'B', 'C', 'D'], f"Dijkstra path failed: {d_res['path']}"
    assert d_res["total_cost"] == 4, f"Dijkstra cost failed: {d_res['total_cost']}"
    print(f"[PASS] Dijkstra shortest path: {' -> '.join(d_res['path'])} (Cost: {d_res['total_cost']})")

    # Test 3: Knapsack
    print("\n[Test 3] Testing 0/1 Knapsack DP...")
    sample_movies = [
        {"title": "Movie 1", "runtime": 90, "value": 80},
        {"title": "Movie 2", "runtime": 120, "value": 95},
        {"title": "Movie 3", "runtime": 60, "value": 60},
        {"title": "Movie 4", "runtime": 150, "value": 100}
    ]
    k_res = solve_knapsack_01(sample_movies, 210)
    assert k_res["max_value"] == 175, f"Knapsack value failed: {k_res['max_value']}"
    assert k_res["used_capacity"] == 210, f"Knapsack capacity failed: {k_res['used_capacity']}"
    print(f"[PASS] Knapsack chosen movies: {', '.join(m['title'] for m in k_res['selected_items'])} (Total Value: {k_res['max_value']}, Runtime: {k_res['used_capacity']}m)")

    # Test 4: Union-Find
    print("\n[Test 4] Testing Union-Find (Path Compression & Rank)...")
    uf = UnionFind()
    uf.union("Drishyam (Malayalam)", "Drushyam (Telugu)")
    uf.union("Drushyam (Telugu)", "Drishyam (Hindi)")
    uf.union("Vikram Vedha (Tamil)", "Vikram Vedha (Hindi)")

    assert uf.connected("Drishyam (Malayalam)", "Drishyam (Hindi)") is True
    assert uf.connected("Drishyam (Malayalam)", "Vikram Vedha (Tamil)") is False
    print(f"[PASS] DSU connected: Drishyam (Mal) <-> Drishyam (Hindi) => True")
    print(f"[PASS] DSU disjoint: Drishyam (Mal) <-> Vikram Vedha (Tam) => False")

    print("\n" + "=" * 60)
    print("ALL DSA TESTS PASSED SUCCESSFULLY! (100% PASS RATE)")
    print("=" * 60)
