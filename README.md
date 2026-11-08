# Mini-Courier Planner: Intelligent Logistics Optimization Prototype

### Design & Analysis of Algorithms (ETCCDA302) — Capstone Assignment
**K.R. Mangalam University, Gurugram, Haryana**  
**Programme:** B.Tech Computer Science & Engineering (B.Tech CSE & Specializations)  
**Faculty In-Charge:** Dr. Shweta Agarwal  
**Assessment Type:** Coding-based Capstone (100 Marks scaled down to 10 marks)  
**Mapped Course Outcomes:** CO1, CO2, CO3, CO4 | **Bloom's Level:** L5 (Create / Evaluate)  
**Submission Mode:** Zosima Platform / File Upload / GitHub Repository Link  

---

## 1. Project Overview & Problem Statement

The **Mini-Courier Planner** is an integrated Python logistics engine that simulates an intelligent courier delivery system. Given an arbitrary set of incoming parcels with varied weights, deadlines, and customer priorities, along with a weighted road network graph of city delivery destinations (modeled around Gurugram / NCR), the system autonomously generates:
1. **An Optimal Packing Plan**: Selects the highest-utility subset of parcels that fits strictly within the courier vehicle's weight limit.
2. **An Ordered Delivery Route**: Computes the shortest travel sequence starting from the Central Hub, visiting every selected customer destination, and returning to the Hub.

The project synthesizes all core algorithmic paradigms covered in the course:
- **Divide and Conquer / Sorting:** Merge Sort and Quick Sort for parcel deadline and priority ordering.
- **Dynamic Programming:** 0/1 Knapsack Problem with full 2D table state transitions and backtracking.
- **Graph Shortest Paths:** Dijkstra's Algorithm using Min-Heap priority queues.
- **Approximation Algorithms & Heuristics:** Nearest-Neighbor TSP approximation and 2-Opt local search route refinement.

---

## 2. Five-Phase Capstone Mapping (100 Marks)

| Phase | Phase Title | Marks | Implemented Components | Deliverables & Evidence |
|---|---|:---:|---|---|
| **Phase 1** | Courier Problem Design and Planning | **20** | `src/models.py`, `src/phase1_design.py` | Data schemas (Parcel, RoadNetworkGraph), pipeline architecture diagram, Gurugram road network topology. |
| **Phase 2** | Package Prioritization and Box Filling | **20** | `src/phase2_prioritization.py` | Merge Sort (stable $O(N \log N)$), Quick Sort, 0/1 Knapsack DP table generation, backtracking, packing manifest. |
| **Phase 3** | Route Maker and Graph Processing | **20** | `src/phase3_routing.py` | Dijkstra's Single Source Shortest Path ($O((V+E)\log V)$), All-Pairs distance matrix, Nearest-Neighbor TSP, Turn-by-Turn waypoint navigation. |
| **Phase 4** | Performance Testing and Optimization | **20** | `src/phase4_benchmark.py` | Empirical benchmarks on $N \in [10, 500]$, Big-O scaling analysis, 4 generated PNG runtime charts, 1D DP & 2-Opt optimizations. |
| **Phase 5** | Final Report and Demonstration | **20** | `main.py`, `REPORT.md`, `VIVA_PREP.md`, `generate_artifacts.py` | Interactive CLI, automated test suite, unseen dataset evaluation, terminal screenshots, and viva documentation. |

---

## 3. Directory Structure

```text
mini_courier_planner/
├── data/
│   ├── city_graph.json             # 11-node Gurugram road network topology
│   ├── sample_small.json           # 6 parcels, 20kg cap (DP Table tracing & Viva)
│   ├── sample_medium.json          # 25 parcels, 60kg cap (Delivery van simulation)
│   ├── sample_large.json           # 100 parcels, 250kg cap (Logistics truck simulation)
│   └── unseen_test.json            # 8 parcels, 25kg cap (Unseen examiner dataset)
├── src/
│   ├── __init__.py                 # Package exports
│   ├── models.py                   # Data models (Parcel, DeliveryPlan, DeliveryPoint)
│   ├── phase1_design.py            # Graph data structure & system architecture
│   ├── phase2_prioritization.py    # Merge Sort, Quick Sort, 0/1 Knapsack DP
│   ├── phase3_routing.py           # Dijkstra's Algorithm, Nearest-Neighbor TSP, 2-Opt
│   ├── phase4_benchmark.py         # Empirical benchmarking & Pillow chart engine
│   └── courier_system.py           # Unified end-to-end pipeline orchestrator
├── tests/
│   ├── test_sorting.py             # Correctness & stability unit tests
│   ├── test_knapsack.py            # DP optimality & capacity constraint tests
│   ├── test_dijkstra.py            # Shortest paths & triangle inequality tests
│   ├── test_tsp.py                 # Closed tour & 2-Opt improvement tests
│   └── test_integrated.py          # End-to-end pipeline integration tests
├── output/
│   ├── charts/                     # Generated PNG runtime charts (Phase 4)
│   │   ├── sorting_comparison.png
│   │   ├── knapsack_dp_scaling.png
│   │   ├── graph_routing_scaling.png
│   │   └── integrated_system_runtime.png
│   ├── screenshots/                # Terminal output screenshots (Phase 5)
│   │   ├── screenshot_phase1_architecture.png
│   │   ├── screenshot_phase2_3_small_dataset.png
│   │   ├── screenshot_phase4_benchmark.png
│   │   └── screenshot_phase5_unseen_evaluation.png
│   ├── trace_small_run.txt         # Formatted text trace of small dataset run
│   ├── trace_unseen_run.txt        # Formatted text trace of unseen viva run
│   └── trace_benchmark.txt         # Formatted text table of performance timings
├── main.py                         # Interactive CLI menu
├── generate_artifacts.py           # Script to regenerate all charts & screenshots
├── README.md                       # This file
├── REPORT.md                       # Academic Capstone Report (Phases 1-5)
└── VIVA_PREP.md                    # Viva-Voce preparation guide
```

---

## 4. Setup and Execution Instructions

### Prerequisites
- Python 3.8+ (tested and verified on Python 3.10)
- Built-in libraries used: `json`, `time`, `heapq`, `dataclasses`, `unittest`, `random`
- Rendering library for charts/screenshots: `Pillow` (`PIL`)

### Running the Interactive Menu
From the repository root or `mini_courier_planner` directory, run:
```bash
python mini_courier_planner/main.py
```
This opens the terminal menu:
```text
================================================================================
    K.R. MANGALAM UNIVERSITY - DESIGN & ANALYSIS OF ALGORITHMS (ETCCDA302)
          CAPSTONE ASSIGNMENT: MINI-COURIER PLANNER PROTOTYPE
================================================================================
  [1] Phase 1: View System Architecture & Problem Design
  [2] Phase 2 & 3: Run Small Dataset Demo (with full DP Matrix evidence)
  [3] Phase 2 & 3: Run Medium Dataset Demo (25 Parcels, Van Trip)
  [4] Phase 2 & 3: Run Large Dataset Demo (100 Parcels, Truck Trip)
  [5] Viva Test: Run Unseen Dataset Evaluation (Phase 5 Evidence)
  [6] Interactive: Enter Custom Parcel Dataset Live
  [7] Phase 4: Run Empirical Benchmarks & Regenerate Runtime PNG Charts
  [8] Run Complete Automated Test Suite (unittest)
  [0] Exit
--------------------------------------------------------------------------------
```

### Running the Automated Unit Test Suite
To verify the mathematical correctness and edge cases of every implemented algorithm:
```bash
python -m unittest discover -s mini_courier_planner/tests
```
All 15 unit and integration tests will execute and report `OK`.

### Regenerating Charts and Screenshots
To re-run benchmarks and re-render all PNG charts and screenshots in `output/`:
```bash
python mini_courier_planner/generate_artifacts.py
```

---

## 5. Algorithmic Summary

| Stage | Algorithm | Time Complexity | Space Complexity | Practical Role |
|---|---|:---:|:---:|---|
| **Phase 2A** | Merge Sort | $\mathcal{O}(N \log N)$ | $\mathcal{O}(N)$ | Strict deadline-driven ordering with stability. |
| **Phase 2B** | 0/1 Knapsack DP | $\mathcal{O}(N \cdot W)$ | $\mathcal{O}(N \cdot W)$ | Maximize total delivery utility within box weight limit. |
| **Phase 3A** | Dijkstra (Min-Heap) | $\mathcal{O}((V+E)\log V)$ | $\mathcal{O}(V)$ | Minimum physical road distances between stops. |
| **Phase 3B** | Nearest-Neighbor TSP | $\mathcal{O}(K^2)$ | $\mathcal{O}(K)$ | Rapid heuristic ordering of stops into a closed loop. |
| **Phase 3C** | 2-Opt Local Search | $\mathcal{O}(\text{iter} \cdot K^2)$ | $\mathcal{O}(K)$ | Eliminates crossing edges and shortens total route. |
