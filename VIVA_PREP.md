# Viva-Voce & Demonstration Master Guide
# Mini-Courier Planner (ETCCDA302 Capstone)
**K.R. Mangalam University | Dr. Shweta Agarwal**

This document provides complete, line-by-line preparation for every potential viva question and live coding challenge specified in the course assessment guidelines.

---

## Question 1: Explain the Working of Any Implemented Algorithm

### 1.1 Merge Sort (Parcel Prioritization)
- **Concept:** Divide and Conquer algorithm.
- **Step 1 (Divide):** Recursively splits the array into two halves at `mid = len(arr) // 2` until single-element subarrays remain.
- **Step 2 (Conquer):** Recursively sorts both sub-arrays.
- **Step 3 (Combine / Merge):** Merges the two sorted halves using two pointers (`i` and `j`). It compares `parcel_sort_key(left[i])` with `parcel_sort_key(right[j])`. The smaller key (earliest deadline; or if equal, highest priority) is placed into the output list.
- **Code Reference:** `src/phase2_prioritization.py` (lines 33–69).

### 1.2 0/1 Knapsack Dynamic Programming (Vehicle Packing)
- **Concept:** Solves the combinatorial optimization problem where items cannot be divided (0 = leave, 1 = take).
- **Table Definition:** `dp_table[i][w]` represents the maximum utility attainable using a subset of the first `i` parcels within a weight limit of `w` kg.
- **Recurrence:**
  $$\text{dp}[i][w] = \begin{cases}
  \text{dp}[i-1][w] & \text{if } w_i > w \\
  \max(\text{dp}[i-1][w], \text{dp}[i-1][w - w_i] + v_i) & \text{if } w_i \le w
  \end{cases}$$
- **Backtracking:** Traces from `dp[N][W]` backwards to `dp[0][0]`. If `dp[i][w] != dp[i-1][w]`, parcel `i` was packed, and the remaining capacity is reduced by `w_i`.
- **Code Reference:** `src/phase2_prioritization.py` (lines 100–165).

### 1.3 Dijkstra's Shortest Path Algorithm (Road Network Distances)
- **Concept:** Greedy graph search using a Min-Heap priority queue (`heapq`).
- **Working:**
  1. Initializes distances to all nodes as $\infty$, with `dist[start_node] = 0`.
  2. Extracts vertex $u$ with minimum distance from the heap.
  3. Relaxes all adjacent edges $(u, v)$: if $\text{dist}[u] + \text{weight}(u, v) < \text{dist}[v]$, updates $\text{dist}[v]$ and sets `parent[v] = u`, pushing $( \text{dist}[v], v )$ to the heap.
  4. Continues until the queue is empty.
- **Code Reference:** `src/phase3_routing.py` (lines 20–68).

### 1.4 Nearest-Neighbor TSP Approximation (Tour Sequencing)
- **Concept:** Greedy heuristic for the Traveling Salesperson Problem.
- **Working:**
  1. Starts at Central Hub (`Hub`).
  2. Iteratively selects the unvisited customer destination that has the minimum shortest road distance from the current node.
  3. Marks the destination as visited and moves there.
  4. Once all parcel destinations have been visited, returns to `Hub` to close the loop.
- **Code Reference:** `src/phase3_routing.py` (lines 108–162).

---

## Question 2: Trace the Algorithm Using a Given Input

### Example Trace: 0/1 Knapsack DP
**Given Input:**
- Vehicle Capacity $W = 6\text{ kg}$
- 3 Parcels:
  - $P_1$: Weight $w_1 = 2\text{ kg}$, Value $v_1 = 30$
  - $P_2$: Weight $w_2 = 3\text{ kg}$, Value $v_2 = 40$
  - $P_3$: Weight $w_3 = 4\text{ kg}$, Value $v_3 = 60$

**Step-by-Step DP Matrix Construction:**

| $i$ \ $w$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **$i=0$ (Base)** | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **$i=1$ ($w_1=2, v_1=30$)** | 0 | 0 | 30 | 30 | 30 | 30 | 30 |
| **$i=2$ ($w_2=3, v_2=40$)** | 0 | 0 | 30 | 40 | 40 | 70 | 70 |
| **$i=3$ ($w_3=4, v_3=60$)** | 0 | 0 | 30 | 40 | 60 | 70 | **90** |

**Calculations for row $i=3$:**
- For $w=4$: $\max(\text{dp}[2][4], \text{dp}[2][0] + 60) = \max(40, 60) = 60$.
- For $w=5$: $\max(\text{dp}[2][5], \text{dp}[2][1] + 60) = \max(70, 0 + 60) = 70$.
- For $w=6$: $\max(\text{dp}[2][6], \text{dp}[2][2] + 60) = \max(70, 30 + 60) = 90$.

**Backtracking:**
1. Start at cell $(3, 6) = 90$. Cell $(2, 6) = 70 \ne 90 \implies$ **Take $P_3$**. Remaining $w = 6 - 4 = 2$.
2. Inspect cell $(2, 2) = 30$. Cell $(1, 2) = 30 = 30 \implies$ **Skip $P_2$**. Remaining $w = 2$.
3. Inspect cell $(1, 2) = 30$. Cell $(0, 2) = 0 \ne 30 \implies$ **Take $P_1$**. Remaining $w = 2 - 2 = 0$.
4. **Selected Set:** $\{P_1, P_3\}$, Total Weight = $2 + 4 = 6\text{ kg}$, Total Utility = $30 + 60 = 90$.

---

## Question 3: How to Modify the Code to Handle Different Inputs

### 3.1 Changing Vehicle Capacity
- In `main.py`, choose Option `[6]` (Interactive Live Input) and enter the desired capacity (e.g. `50`).
- Or pass `vehicle_capacity` directly in code:
  ```python
  plan = planner.plan_trip(parcels, vehicle_capacity=80)
  ```

### 3.2 Adding a New Road Edge or Delivery Sector
In `src/phase1_design.py` or before calling the planner:
```python
# Add new sector
graph.add_node("Sec82", "Sector 82 New Gurugram", "South-West")
# Connect to existing road network
graph.add_edge("Sec49", "Sec82", distance_km=4.8, bidirectional=True)
```

### 3.3 Prioritizing Pure Weight over Deadlines
In `src/phase2_prioritization.py`, modify `parcel_sort_key`:
```python
# To sort primarily by lowest weight first:
def parcel_sort_key(parcel: Parcel):
    return (parcel.weight, parcel.deadline_hours)
```

---

## Question 4: Identify Time and Space Complexity

| Algorithm | Best-Case Time | Average Time | Worst-Case Time | Auxiliary Space | Reason |
|---|:---:|:---:|:---:|:---:|---|
| **Merge Sort** | $\mathcal{O}(N \log N)$ | $\mathcal{O}(N \log N)$ | $\mathcal{O}(N \log N)$ | $\mathcal{O}(N)$ | Always divides array evenly and copies during merge. |
| **Quick Sort** | $\mathcal{O}(N \log N)$ | $\mathcal{O}(N \log N)$ | $\mathcal{O}(N^2)$ | $\mathcal{O}(\log N)$ | Degrades if pivot is extreme minimum or maximum. |
| **0/1 Knapsack DP** | $\mathcal{O}(N \cdot W)$ | $\mathcal{O}(N \cdot W)$ | $\mathcal{O}(N \cdot W)$ | $\mathcal{O}(N \cdot W)$ | Fills an $(N+1) \times (W+1)$ matrix cell by cell. |
| **1D Knapsack DP** | $\mathcal{O}(N \cdot W)$ | $\mathcal{O}(N \cdot W)$ | $\mathcal{O}(N \cdot W)$ | $\mathcal{O}(W)$ | Reuses single 1D array by reverse iteration. |
| **Dijkstra (Heap)** | $\mathcal{O}((V+E)\log V)$ | $\mathcal{O}((V+E)\log V)$ | $\mathcal{O}((V+E)\log V)$ | $\mathcal{O}(V)$ | Each vertex popped once; each edge relaxed at most once. |
| **Nearest Neighbor TSP** | $\mathcal{O}(K^2)$ | $\mathcal{O}(K^2)$ | $\mathcal{O}(K^2)$ | $\mathcal{O}(K)$ | Evaluates remaining unvisited nodes at each of $K$ steps. |

---

## Question 5: Why One Algorithm Performs Differently From Another

### 5.1 Merge Sort vs. Quick Sort
- **Cache Locality:** Quick Sort operates in-place inside contiguous arrays without allocating extra lists, resulting in superior hardware cache hit rates and faster constant factors ($\approx 1.5\times$ faster in practice).
- **Stability:** Merge Sort is stable (it preserves the relative ordering of equal keys), which is vital for multi-key sorting (deadline + priority). Quick Sort swaps equal keys across pivots, losing stability.

### 5.2 2D Knapsack DP vs. 1D Knapsack DP
- **2D DP:** Stores all previous states, allowing exact backtracking to extract the list of chosen parcels. Space is $\mathcal{O}(N \cdot W)$.
- **1D DP:** Overwrites previous rows by iterating backwards ($w = W \dots w_i$). It only computes the maximum numerical value without extra memory, reducing space to $\mathcal{O}(W)$.

### 5.3 Nearest-Neighbor TSP vs. Exact TSP (Held-Karp Dynamic Programming)
- **Exact TSP (Held-Karp):** Requires $\mathcal{O}(2^K \cdot K^2)$ time. For $K = 25$, $2^{25} \approx 33,554,432$, taking minutes to hours.
- **Nearest-Neighbor TSP:** Runs in $\mathcal{O}(K^2)$ ($< 0.05\text{ ms}$ for $K = 25$) and provides an approximation bound of $\approx \frac{1}{2}(\log_2 K + 1)$ in metric graphs, which 2-Opt further improves.

---

## Question 6: Running the Program Using an Unseen Dataset

During your viva/demonstration:
1. Launch the interactive menu:
   ```bash
   python mini_courier_planner/main.py
   ```
2. Select **Option [5]** to run the pre-configured unseen evaluation dataset (`data/unseen_test.json`).
3. Or select **Option [6]** to manually enter live values requested by the examiner (custom parcel IDs, destinations, weights, deadlines, and vehicle capacity).
4. Explain the resulting output:
   - Sorted priority list.
   - 0/1 Knapsack loaded vs. deferred parcels.
   - Dijkstra shortest paths and final TSP delivery sequence.

---

## Question 7: Identify and Correct Common Errors

### Error Case A: Off-by-One in Knapsack DP Matrix
- **Problem:** If range is set to `range(W)` instead of `range(W + 1)`, capacity $W$ is never reached.
- **Fix:** Matrix must have dimensions $(N + 1) \times (W + 1)$ so index $W$ represents the full capacity.

### Error Case B: Repeating Items in 1D Knapsack DP
- **Problem:** If inner loop iterates forward `for w in range(w_i, W + 1):`, the same parcel can be added multiple times (unbounded knapsack).
- **Fix:** Iterate backwards `for w in range(W, w_i - 1, -1):` so each parcel is considered at most once.

### Error Case C: Negative Weights in Dijkstra
- **Problem:** Dijkstra assumes greedy monotonicity. Negative edge weights invalidate edge relaxation.
- **Fix:** Road network distances are strictly non-negative physical kilometers ($w \ge 0$). If negative weights existed, Bellman-Ford algorithm would be required.

### Error Case D: Disconnected Graph Node
- **Problem:** If an isolated delivery node has no road path to `Hub`, `dist[v] == inf`.
- **Fix:** The prototype checks `dist_matrix[u][v] == inf` and flags unreachable nodes, avoiding crashes in TSP routing.
