"""
Mini-Courier Planner - Main Interactive CLI & Demonstration
Design & Analysis of Algorithms (ETCCDA302)
K.R. Mangalam University, Gurugram
Faculty: Dr. Shweta Agarwal
"""

import sys
import os
import json
from typing import List

# Configure stdout for safe encoding on all platforms
try:
    if sys.stdout.encoding != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# Ensure package can be imported
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.models import Parcel
from src.phase1_design import build_default_gurugram_graph, get_architecture_overview
from src.phase2_prioritization import merge_sort_parcels, quick_sort_parcels, knapsack_01_dp, format_dp_table
from src.phase3_routing import compute_metric_distance_matrix, nearest_neighbor_tsp
from src.phase4_benchmark import run_comprehensive_benchmark, generate_all_runtime_charts, format_benchmark_table
from src.courier_system import MiniCourierPlanner


def load_dataset(filepath: str) -> tuple[str, int, List[Parcel]]:
    """Loads parcel dataset from a JSON file."""
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    name = data.get("dataset_name", os.path.basename(filepath))
    capacity = int(data.get("vehicle_capacity_kg", 50))
    parcels = [Parcel.from_dict(p) for p in data["parcels"]]
    return name, capacity, parcels


def run_pipeline_demo(dataset_file: str, show_dp_table: bool = True):
    """Executes the complete Mini-Courier Planner pipeline on a chosen dataset."""
    base_dir = os.path.dirname(__file__)
    full_path = os.path.join(base_dir, dataset_file)
    name, capacity, parcels = load_dataset(full_path)

    print("\n" + "=" * 80)
    print(f"  EXECUTING MINI-COURIER PLANNER: {name.upper()}")
    print("=" * 80)
    print(f"• Dataset Source:          {dataset_file}")
    print(f"• Total Parcels Submitted: {len(parcels)}")
    print(f"• Vehicle Capacity Limit:  {capacity} kg")

    planner = MiniCourierPlanner(graph=build_default_gurugram_graph(), hub_node="Hub")
    plan = planner.plan_trip(parcels, vehicle_capacity=capacity, sort_algo="merge_sort")

    report = planner.print_plan_summary(plan, show_dp_table=show_dp_table)
    print(report)


def run_interactive_custom_input():
    """Allows examiner/student to test with custom unseen parcel inputs on the fly."""
    print("\n" + "=" * 70)
    print("        INTERACTIVE CUSTOM PARCEL ENTRY (VIVA TESTING)")
    print("=" * 70)
    graph = build_default_gurugram_graph()
    available_nodes = [n for n in graph.get_nodes() if n != "Hub"]
    print("Available Delivery Nodes in Gurugram Network:")
    print("  " + ", ".join(available_nodes))

    try:
        cap_str = input("\nEnter Vehicle Capacity in kg (e.g. 25): ").strip()
        capacity = int(cap_str) if cap_str else 25

        count_str = input("Enter number of custom parcels to add (e.g. 3): ").strip()
        num_parcels = int(count_str) if count_str else 3

        custom_parcels = []
        for i in range(1, num_parcels + 1):
            print(f"\n--- Parcel #{i} ---")
            pid = f"CP{i:02d}"
            name = input(f"Recipient Name (default 'Customer_{i}'): ").strip() or f"Customer_{i}"
            dest = input(f"Destination Node from list (default '{available_nodes[(i-1)%len(available_nodes)]}'): ").strip()
            if dest not in available_nodes:
                dest = available_nodes[(i - 1) % len(available_nodes)]
            w_str = input("Weight in kg (default 5): ").strip()
            weight = int(w_str) if w_str else 5
            p_str = input("Priority 1-10 (default 8): ").strip()
            priority = int(p_str) if p_str else 8
            d_str = input("Deadline in hours (default 2.0): ").strip()
            deadline = float(d_str) if d_str else 2.0

            p = Parcel(
                id=pid,
                customer_name=name,
                destination=dest,
                weight=weight,
                priority=priority,
                deadline_hours=deadline
            )
            custom_parcels.append(p)

        planner = MiniCourierPlanner(graph=graph, hub_node="Hub")
        plan = planner.plan_trip(custom_parcels, vehicle_capacity=capacity)
        print("\n" + planner.print_plan_summary(plan, show_dp_table=True))

    except Exception as e:
        print(f"Error handling custom input: {e}")


def main_menu():
    """Main terminal menu for project demonstration."""
    while True:
        print("\n" + "=" * 80)
        print("    K.R. MANGALAM UNIVERSITY - DESIGN & ANALYSIS OF ALGORITHMS (ETCCDA302)")
        print("           INTELLIGENT MINI-COURIER PLANNER - INTERACTIVE CLI")
        print("          Student: Shivam Kumar Roy | Faculty: Dr. Shweta Agarwal")
        print("=" * 80)
        print("  [1] System Architecture & Algorithmic Pipeline Overview")
        print("  [2] Small Dataset Demonstration (with complete 2D DP Table Matrix)")
        print("  [3] Medium Dataset Demonstration (25 Parcels, City Van Route)")
        print("  [4] Large Dataset Demonstration (100 Parcels, Logistics Truck Route)")
        print("  [5] Unseen Dataset Evaluation (Viva Testing)")
        print("  [6] Interactive Live Custom Parcel Entry")
        print("  [7] Run Algorithmic Benchmarks & Regenerate Performance Charts")
        print("  [8] Run Complete Automated Unit Test Suite (15 Tests)")
        print("  [0] Exit")
        print("-" * 80)
        choice = input("Enter choice [0-8]: ").strip()

        if choice == "1":
            print(get_architecture_overview())
        elif choice == "2":
            run_pipeline_demo("data/sample_small.json", show_dp_table=True)
        elif choice == "3":
            run_pipeline_demo("data/sample_medium.json", show_dp_table=False)
        elif choice == "4":
            run_pipeline_demo("data/sample_large.json", show_dp_table=False)
        elif choice == "5":
            run_pipeline_demo("data/unseen_test.json", show_dp_table=True)
        elif choice == "6":
            run_interactive_custom_input()
        elif choice == "7":
            print("\nExecuting Comprehensive Algorithmic Benchmarks...")
            res = run_comprehensive_benchmark()
            print(format_benchmark_table(res))
            base_dir = os.path.dirname(__file__)
            chart_dir = os.path.join(base_dir, "output", "charts")
            charts = generate_all_runtime_charts(res, chart_dir)
            print("\nSuccessfully generated runtime PNG charts in output/charts/:")
            for c in charts:
                print(f"  • {os.path.basename(c)}")
        elif choice == "8":
            import unittest
            base_dir = os.path.dirname(__file__)
            tests_dir = os.path.join(base_dir, "tests")
            loader = unittest.TestLoader()
            suite = loader.discover(tests_dir)
            runner = unittest.TextTestRunner(verbosity=2)
            runner.run(suite)
        elif choice == "0":
            print("Exiting Mini-Courier Planner. Goodbye!")
            break
        else:
            print("Invalid choice, please enter 0 through 8.")


if __name__ == "__main__":
    main_menu()
