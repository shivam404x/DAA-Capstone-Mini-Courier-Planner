# Mini-Courier Planner: Intelligent Logistics Optimization Engine

### Design & Analysis of Algorithms (ETCCDA302) — Capstone Project
**K.R. Mangalam University, Gurugram, Haryana**  
**Author:** Shivam Kumar Roy  
**Programme:** B.Tech Computer Science & Engineering (B.Tech CSE)  
**Project Supervisor:** Dr. Shweta Agarwal  

---

## 1. Project Overview

The **Mini-Courier Planner** is an integrated Python logistics engine that simulates an intelligent courier delivery dispatch system. Given an arbitrary batch of incoming packages with heterogeneous weights, deadlines, and urgency ratings, along with a weighted municipal road graph (modeled around Gurugram / NCR), the system autonomously calculates:
1. **An Optimal Vehicle Loading Plan:** Selects the highest-utility subset of packages that strictly respects vehicle carrying capacity.
2. **An Ordered Delivery Tour:** Computes the shortest travel tour starting at the Central Logistics Hub, visiting every selected customer destination, and returning to the Hub.

The software synthesizes four core computer science algorithm paradigms:
- **Divide and Conquer (Merge Sort & Quick Sort):** Orders parcels by deadline (earliest-first) and priority score.
- **Dynamic Programming (0/1 Knapsack):** Full 2D state matrix construction and backtracking to maximize delivered utility.
- **Graph Shortest Paths (Dijkstra's Algorithm):** Min-Heap priority queue implementation calculating all-pairs physical road distances.
- **Approximation Algorithms (Nearest-Neighbor TSP with 2-Opt):** Rapid closed-tour construction and route self-intersection elimination.

---

## 2. System Architecture & Algorithmic Pipeline

```text
[Raw Parcels Manifest & Gurugram Road Graph]
                     │
                     ▼
┌────────────────────────────────────────────────────────┐
│ STAGE 1: PARCEL PRIORITIZATION (Sorting Algorithms)    │
│ • Primary Sort Key: Earliest Delivery Deadline (asc)   │
│ • Secondary Sort Key: Priority Urgency Rating (desc)   │
│ • Implemented: Merge Sort (Stable) & Quick Sort        │
└────────────────────────────────────────────────────────┘
                     │
                     ▼
┌────────────────────────────────────────────────────────┐
│ STAGE 2: VEHICLE PAYLOAD ALLOCATION (0/1 Knapsack DP)  │
│ • Table Construction: DP[i][w] state matrix            │
│ • Exact Backtracking Reconstruction                   │
│ • Output: Manifest of Loaded vs. Deferred Parcels      │
└────────────────────────────────────────────────────────┘
                     │
                     ▼
┌────────────────────────────────────────────────────────┐
│ STAGE 3: METRIC DISTANCE MATRIX (Dijkstra's Algorithm) │
│ • Min-Heap Priority Queue on Road Network Graph        │
│ • Computes pairwise shortest paths between active stops│
│ • Reconstructs turn-by-turn physical road waypoints    │
└────────────────────────────────────────────────────────┘
                     │
                     ▼
┌────────────────────────────────────────────────────────┐
│ STAGE 4: TOUR SEQUENCING (Nearest-Neighbor TSP + 2Opt) │
│ • Greedy Nearest-Neighbor Closed Cycle Construction    │
│ • 2-Opt Iterative Edge-Swap Optimization               │
│ • Generates complete driver navigation schedule        │
└────────────────────────────────────────────────────────┘
                     │
                     ▼
[Optimized Packing Plan, Delivery Itinerary & Performance Metrics]
```

---

## 3. Directory Structure

```text
mini_courier_planner/
├── requirements.txt               # Dependencies file (Pillow>=9.0.0)
├── run.bat                        # Windows 1-click batch launcher
├── README.md                      # Project documentation and execution guide
├── REPORT.md                      # Comprehensive academic project report
├── REPORT.html                    # Visual interactive report dashboard
├── VIVA_PREP.md                   # Master Viva-Voce preparation guide
├── main.py                        # Interactive CLI menu application
├── generate_artifacts.py          # Script to regenerate charts & screenshots
├── .gitignore                     # Git configuration
│
├── data/                          # Input Datasets & Network Topology
│   ├── city_graph.json            # 11-node Gurugram road network topology
│   ├── sample_small.json          # 6 parcels, 20kg cap (DP Table tracing & Viva)
│   ├── sample_medium.json         # 25 parcels, 60kg cap (Van trip simulation)
│   ├── sample_large.json          # 100 parcels, 250kg cap (Truck trip simulation)
│   └── unseen_test.json           # 8 parcels, 25kg cap (Viva evaluation dataset)
│
├── src/                           # Core Algorithmic Source Code
│   ├── __init__.py
│   ├── models.py                  # Parcel, DeliveryPoint, DeliveryPlan classes
│   ├── phase1_design.py           # Adjacency List road graph & pipeline design
│   ├── phase2_prioritization.py   # Merge Sort, Quick Sort, 0/1 Knapsack DP
│   ├── phase3_routing.py          # Dijkstra (Min-Heap), Nearest-Neighbor TSP, 2-Opt
│   ├── phase4_benchmark.py        # Benchmark suite & Pillow chart generation engine
│   └── courier_system.py          # Unified end-to-end pipeline orchestrator
│
├── tests/                         # Automated Unit & Integration Tests
│   ├── __init__.py
│   ├── test_sorting.py            # Merge Sort vs Quick Sort correctness & stability
│   ├── test_knapsack.py           # 0/1 Knapsack DP optimality & constraints
│   ├── test_dijkstra.py           # Dijkstra shortest path & triangle inequality
│   ├── test_tsp.py                # Nearest-Neighbor TSP & 2-Opt tour tests
│   └── test_integrated.py         # End-to-end pipeline integration tests
│
└── output/                        # Evaluation Evidence & Verification Artifacts
    ├── charts/                    # Generated PNG Runtime Charts
    │   ├── sorting_comparison.png
    │   ├── knapsack_dp_scaling.png
    │   ├── graph_routing_scaling.png
    │   └── integrated_system_runtime.png
    ├── screenshots/               # Terminal Output PNG Screenshots
    │   ├── screenshot_phase1_architecture.png
    │   ├── screenshot_phase2_3_small_dataset.png
    │   ├── screenshot_phase4_benchmark.png
    │   └── screenshot_phase5_unseen_evaluation.png
    ├── trace_small_run.txt        # Verified text trace of small dataset
    ├── trace_unseen_run.txt       # Verified text trace of unseen viva dataset
    └── trace_benchmark.txt        # Verified benchmark timing table
```

---

## 4. Setup and Execution Instructions

### Prerequisites
- Python 3.8 or higher (tested and verified on Python 3.10)
- Core standard libraries: `json`, `heapq`, `dataclasses`, `time`, `random`, `unittest`
- Chart & screenshot generation: `Pillow>=9.0.0`

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the Interactive CLI
* **Windows (One-Click):** Double-click `run.bat`
* **Or via Terminal:**
  ```bash
  python main.py
  ```

This launches the interactive terminal menu:
```text
================================================================================
    K.R. MANGALAM UNIVERSITY - DESIGN & ANALYSIS OF ALGORITHMS (ETCCDA302)
           INTELLIGENT MINI-COURIER PLANNER - INTERACTIVE CLI
          Student: Shivam Kumar Roy | Faculty: Dr. Shweta Agarwal
================================================================================
  [1] System Architecture & Algorithmic Pipeline Overview
  [2] Small Dataset Demonstration (with complete 2D DP Table Matrix)
  [3] Medium Dataset Demonstration (25 Parcels, City Van Route)
  [4] Large Dataset Demonstration (100 Parcels, Logistics Truck Route)
  [5] Unseen Dataset Evaluation (Viva Testing)
  [6] Interactive Live Custom Parcel Entry
  [7] Run Algorithmic Benchmarks & Regenerate Performance Charts
  [8] Run Complete Automated Unit Test Suite (15 Tests)
  [0] Exit
--------------------------------------------------------------------------------
```

### Step 3: Run Automated Unit Tests
To verify all algorithmic invariants, stability, optimality, and edge cases:
```bash
python -m unittest discover -s tests -v
```
All 15 tests will execute and report `OK`.

### Step 4: View the Visual HTML Report
Double-click `REPORT.html` in any web browser to view the formatted report with embedded charts, screenshots, and mathematical formulas.

---

## 5. Algorithmic Complexity Summary

| Stage | Algorithm | Time Complexity | Space Complexity | Practical Role |
|---|---|:---:|:---:|---|
| **Prioritization** | Merge Sort | $\Theta(N \log N)$ | $\mathcal{O}(N)$ | Strict deadline-driven ordering with stability guarantee. |
| **Payload Loading** | 0/1 Knapsack DP | $\mathcal{O}(N \cdot W)$ | $\mathcal{O}(N \cdot W)$ | Maximize total delivery utility within vehicle weight limit. |
| **Network Paths** | Dijkstra (Min-Heap) | $\mathcal{O}((V+E)\log V)$ | $\mathcal{O}(V)$ | Minimum physical road distances across municipal graph. |
| **Tour Construction** | Nearest-Neighbor TSP | $\mathcal{O}(K^2)$ | $\mathcal{O}(K)$ | Rapid heuristic sequencing into closed delivery loop. |
| **Route Refinement** | 2-Opt Local Search | $\mathcal{O}(\text{iter} \cdot K^2)$ | $\mathcal{O}(K)$ | Eliminates crossing edges and shortens tour distance. |
