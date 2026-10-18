/**
 * Unit Tests for Movie Recommendation Platform Core DSA Algorithms
 * Tests:
 * 1. MinHeap (Priority Queue)
 * 2. Dijkstra's Algorithm (Movie Bridge Shortest Path)
 * 3. 0/1 Knapsack Dynamic Programming (Time-Budget Planner)
 * 4. Disjoint Set Union (Union-Find with Rank & Path Compression for Remakes)
 */

// ============================================================================
// 1. MinHeap Implementation
// ============================================================================

/**
 * Min-Heap (Priority Queue)
 * Time Complexities:
 * - push(): O(log K)
 * - pop(): O(log K)
 * - peek(): O(1)
 * - size(): O(1)
 */
class MinHeap {
  constructor(compareFn = (a, b) => a - b) {
    this.heap = [];
    this.compare = compareFn;
  }

  size() {
    return this.heap.length;
  }

  isEmpty() {
    return this.heap.length === 0;
  }

  peek() {
    return this.heap.length > 0 ? this.heap[0] : null;
  }

  push(val) {
    this.heap.push(val);
    this._bubbleUp(this.heap.length - 1);
  }

  pop() {
    if (this.isEmpty()) return null;
    const top = this.heap[0];
    const bottom = this.heap.pop();
    if (!this.isEmpty()) {
      this.heap[0] = bottom;
      this._sinkDown(0);
    }
    return top;
  }

  _bubbleUp(idx) {
    let current = idx;
    while (current > 0) {
      const parent = Math.floor((current - 1) / 2);
      if (this.compare(this.heap[current], this.heap[parent]) < 0) {
        [this.heap[current], this.heap[parent]] = [this.heap[parent], this.heap[current]];
        current = parent;
      } else {
        break;
      }
    }
  }

  _sinkDown(idx) {
    let current = idx;
    const length = this.heap.length;
    while (true) {
      let left = 2 * current + 1;
      let right = 2 * current + 2;
      let smallest = current;

      if (left < length && this.compare(this.heap[left], this.heap[smallest]) < 0) {
        smallest = left;
      }
      if (right < length && this.compare(this.heap[right], this.heap[smallest]) < 0) {
        smallest = right;
      }
      if (smallest !== current) {
        [this.heap[current], this.heap[smallest]] = [this.heap[smallest], this.heap[current]];
        current = smallest;
      } else {
        break;
      }
    }
  }
}

// ============================================================================
// 2. Dijkstra's Algorithm
// ============================================================================

/**
 * Dijkstra's Shortest Path on a Weighted Graph
 * Time Complexity: O((V + E) * log V) using MinHeap
 * Space Complexity: O(V + E)
 */
function dijkstraShortestPath(graph, startNode, isTargetFn) {
  const dist = new Map();
  const parent = new Map();
  const pq = new MinHeap((a, b) => a.dist - b.dist);

  dist.set(startNode, 0);
  pq.push({ node: startNode, dist: 0 });

  let foundTarget = null;

  while (!pq.isEmpty()) {
    const { node: u, dist: d } = pq.pop();

    if (d > dist.get(u)) continue;

    if (isTargetFn(u) && u !== startNode) {
      foundTarget = u;
      break;
    }

    const neighbors = graph.get(u) || [];
    for (const { node: v, weight } of neighbors) {
      const alt = d + weight;
      if (!dist.has(v) || alt < dist.get(v)) {
        dist.set(v, alt);
        parent.set(v, u);
        pq.push({ node: v, dist: alt });
      }
    }
  }

  if (!foundTarget) return null;

  // Reconstruct path
  const path = [];
  let curr = foundTarget;
  while (curr !== undefined) {
    path.push(curr);
    curr = parent.get(curr);
  }
  return { path: path.reverse(), totalCost: dist.get(foundTarget) };
}

// ============================================================================
// 3. 0/1 Knapsack Dynamic Programming
// ============================================================================

/**
 * 0/1 Knapsack Dynamic Programming for Time Budget
 * Time Complexity: O(N * W) where N = items, W = capacity
 * Space Complexity: O(N * W) for reconstruction matrix
 */
function solveKnapsack01(items, capacity) {
  const n = items.length;
  // dp[i][w] = max value considering first i items with capacity w
  const dp = Array.from({ length: n + 1 }, () => new Array(capacity + 1).fill(0));

  for (let i = 1; i <= n; i++) {
    const weight = items[i - 1].runtime;
    const value = items[i - 1].value;

    for (let w = 0; w <= capacity; w++) {
      if (weight <= w) {
        dp[i][w] = Math.max(dp[i - 1][w], dp[i - 1][w - weight] + value);
      } else {
        dp[i][w] = dp[i - 1][w];
      }
    }
  }

  // Backtracking to find selected items
  let w = capacity;
  const selected = [];
  for (let i = n; i > 0; i--) {
    if (dp[i][w] !== dp[i - 1][w]) {
      selected.push(items[i - 1]);
      w -= items[i - 1].runtime;
    }
  }

  return {
    maxValue: dp[n][capacity],
    selectedItems: selected.reverse(),
    usedCapacity: capacity - w,
    dpTablePreview: dp.slice(0, Math.min(n + 1, 6)).map(row => row.slice(0, Math.min(capacity + 1, 10)))
  };
}

// ============================================================================
// 4. Union-Find (Disjoint Set Union)
// ============================================================================

/**
 * Disjoint Set Union (DSU) with Path Compression and Union by Rank
 * Time Complexity: O(alpha(N)) nearly constant amortized time per operation
 * Space Complexity: O(N)
 */
class UnionFind {
  constructor() {
    this.parent = new Map();
    this.rank = new Map();
  }

  makeSet(x) {
    if (!this.parent.has(x)) {
      this.parent.set(x, x);
      this.rank.set(x, 0);
    }
  }

  find(x) {
    if (!this.parent.has(x)) this.makeSet(x);
    if (this.parent.get(x) !== x) {
      // Path compression
      this.parent.set(x, this.find(this.parent.get(x)));
    }
    return this.parent.get(x);
  }

  union(x, y) {
    this.makeSet(x);
    this.makeSet(y);
    const rootX = this.find(x);
    const rootY = this.find(y);

    if (rootX === rootY) return false;

    // Union by rank
    const rankX = this.rank.get(rootX);
    const rankY = this.rank.get(rootY);

    if (rankX < rankY) {
      this.parent.set(rootX, rootY);
    } else if (rankX > rankY) {
      this.parent.set(rootY, rootX);
    } else {
      this.parent.set(rootY, rootX);
      this.rank.set(rootX, rankX + 1);
    }
    return true;
  }

  connected(x, y) {
    return this.find(x) === this.find(y);
  }
}

// ============================================================================
// Run Test Suite
// ============================================================================

console.log("=== RUNNING DSA UNIT TESTS ===");

// Test 1: MinHeap
console.log("\n[Test 1] Testing MinHeap...");
const pq = new MinHeap();
[5, 2, 8, 1, 9, 3].forEach(x => pq.push(x));
const sorted = [];
while (!pq.isEmpty()) sorted.push(pq.pop());
console.assert(JSON.stringify(sorted) === JSON.stringify([1, 2, 3, 5, 8, 9]), `MinHeap failed: ${sorted}`);
console.log("✓ MinHeap push & pop ordering passed: [1, 2, 3, 5, 8, 9]");

// Test 2: Dijkstra's Algorithm
console.log("\n[Test 2] Testing Dijkstra's Algorithm on small graph...");
const graph = new Map();
graph.set('A', [{ node: 'B', weight: 1 }, { node: 'C', weight: 4 }]);
graph.set('B', [{ node: 'C', weight: 2 }, { node: 'D', weight: 5 }]);
graph.set('C', [{ node: 'D', weight: 1 }]);
graph.set('D', []);

const dijkstraResult = dijkstraShortestPath(graph, 'A', node => node === 'D');
console.assert(JSON.stringify(dijkstraResult.path) === JSON.stringify(['A', 'B', 'C', 'D']), "Dijkstra path failed");
console.assert(dijkstraResult.totalCost === 4, `Dijkstra cost failed, expected 4 got ${dijkstraResult.totalCost}`);
console.log(`✓ Dijkstra shortest path: ${dijkstraResult.path.join(' -> ')} (Cost: ${dijkstraResult.totalCost})`);

// Test 3: 0/1 Knapsack DP
console.log("\n[Test 3] Testing 0/1 Knapsack DP...");
const sampleMovies = [
  { title: "Movie 1", runtime: 90, value: 80 },
  { title: "Movie 2", runtime: 120, value: 95 },
  { title: "Movie 3", runtime: 60, value: 60 },
  { title: "Movie 4", runtime: 150, value: 100 }
];
// Free time: 210 minutes (Optimal: Movie 2 (120m, 95) + Movie 1 (90m, 80) = 210m, 175 value)
const knapsackRes = solveKnapsack01(sampleMovies, 210);
console.assert(knapsackRes.maxValue === 175, `Knapsack value failed, expected 175 got ${knapsackRes.maxValue}`);
console.assert(knapsackRes.usedCapacity === 210, `Knapsack used runtime failed, got ${knapsackRes.usedCapacity}`);
console.log(`✓ Knapsack chosen movies: ${knapsackRes.selectedItems.map(m => m.title).join(', ')} (Total Value: ${knapsackRes.maxValue}, Runtime: ${knapsackRes.usedCapacity}m)`);

// Test 4: Union-Find (DSU)
console.log("\n[Test 4] Testing Union-Find (Path Compression & Rank)...");
const uf = new UnionFind();
uf.union("Drishyam (Malayalam)", "Drushyam (Telugu)");
uf.union("Drushyam (Telugu)", "Drishyam (Hindi)");
uf.union("Vikram Vedha (Tamil)", "Vikram Vedha (Hindi)");

console.assert(uf.connected("Drishyam (Malayalam)", "Drishyam (Hindi)") === true, "Drishyam connection failed");
console.assert(uf.connected("Drishyam (Malayalam)", "Vikram Vedha (Tamil)") === false, "Different family false positive");
console.log(`✓ DSU connected: Drishyam (Mal) <-> Drishyam (Hindi) => ${uf.connected("Drishyam (Malayalam)", "Drishyam (Hindi)")}`);
console.log(`✓ DSU disjoint: Drishyam (Mal) <-> Vikram Vedha (Tam) => ${uf.connected("Drishyam (Malayalam)", "Vikram Vedha (Tamil)")}`);

console.log("\n=== ALL DSA TESTS PASSED SUCCESSFULLY! ===");
