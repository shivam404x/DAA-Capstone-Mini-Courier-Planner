"""
Integrated Mini-Courier Planner System Orchestrator
Design & Analysis of Algorithms (ETCCDA302)
K.R. Mangalam University, Gurugram

Orchestrates Phase 1 through Phase 3:
1. Parcel Prioritization (Merge Sort)
2. Capacity Packing (0/1 Knapsack DP)
3. Shortest Paths (Dijkstra)
4. Delivery Route (Nearest-Neighbor TSP)
"""

import time
from typing import List, Dict, Tuple, Optional
from .models import Parcel, DeliveryPlan
from .phase1_design import RoadNetworkGraph, build_default_gurugram_graph
from .phase2_prioritization import (
    merge_sort_parcels,
    quick_sort_parcels,
    knapsack_01_dp,
    format_dp_table
)
from .phase3_routing import (
    compute_metric_distance_matrix,
    nearest_neighbor_tsp,
    build_turn_by_turn_itinerary,
    two_opt_optimize
)


class MiniCourierPlanner:
    """
    Main integrated courier planning system.
    Combines sorting, dynamic programming, shortest-path graph search,
    and TSP route approximation into an end-to-end intelligent logistics optimizer.
    """

    def __init__(self, graph: Optional[RoadNetworkGraph] = None, hub_node: str = "Hub"):
        self.graph = graph if graph is not None else build_default_gurugram_graph()
        self.hub_node = hub_node

    def plan_trip(
        self,
        parcels: List[Parcel],
        vehicle_capacity: int,
        sort_algo: str = "merge_sort",
        enable_2opt: bool = True
    ) -> DeliveryPlan:
        """
        Executes the full courier planning pipeline and returns a DeliveryPlan.
        Runtimes of all phases are precisely tracked.
        """
        runtimes: Dict[str, float] = {}

        # -------------------------------------------------------------
        # STEP 1: PRIORITIZE PARCELS (Phase 2 Sorting)
        # -------------------------------------------------------------
        t0 = time.perf_counter()
        if sort_algo == "quick_sort":
            sorted_parcels = quick_sort_parcels(parcels)
        else:
            sorted_parcels = merge_sort_parcels(parcels)
        t1 = time.perf_counter()
        runtimes["Sorting"] = (t1 - t0) * 1000.0  # in ms

        # -------------------------------------------------------------
        # STEP 2: KNAPSACK CAPACITY OPTIMIZATION (Phase 2 DP)
        # -------------------------------------------------------------
        t2 = time.perf_counter()
        selected_parcels, deferred_parcels, dp_table, max_value = knapsack_01_dp(
            sorted_parcels,
            capacity=vehicle_capacity
        )
        t3 = time.perf_counter()
        runtimes["Knapsack_DP"] = (t3 - t2) * 1000.0  # in ms

        total_weight = sum(p.weight for p in selected_parcels)
        utilization = (total_weight / vehicle_capacity * 100.0) if vehicle_capacity > 0 else 0.0

        # -------------------------------------------------------------
        # STEP 3: SHORTEST PATHS & DISTANCE MATRIX (Phase 3 Dijkstra)
        # -------------------------------------------------------------
        destinations = [p.destination for p in selected_parcels]
        active_stops = [self.hub_node] + destinations

        t4 = time.perf_counter()
        dist_matrix, path_matrix = compute_metric_distance_matrix(self.graph, active_stops)
        t5 = time.perf_counter()
        runtimes["Dijkstra_AllPairs"] = (t5 - t4) * 1000.0  # in ms

        # -------------------------------------------------------------
        # STEP 4: ROUTE SEQUENCING (Phase 3 TSP Nearest-Neighbor)
        # -------------------------------------------------------------
        t6 = time.perf_counter()
        route, total_distance = nearest_neighbor_tsp(
            start_node=self.hub_node,
            delivery_stops=destinations,
            dist_matrix=dist_matrix
        )

        if enable_2opt and len(route) > 4:
            route, total_distance = two_opt_optimize(route, dist_matrix)

        itinerary = build_turn_by_turn_itinerary(route, path_matrix)
        t7 = time.perf_counter()
        runtimes["Route_Planning_TSP"] = (t7 - t6) * 1000.0  # in ms
        runtimes["Total_Pipeline"] = sum(runtimes.values())

        return DeliveryPlan(
            vehicle_capacity=vehicle_capacity,
            all_parcels=parcels,
            sorted_parcels=sorted_parcels,
            selected_parcels=selected_parcels,
            deferred_parcels=deferred_parcels,
            total_weight=total_weight,
            total_value=max_value,
            capacity_utilization_pct=round(utilization, 2),
            dp_table=dp_table,
            delivery_route=route,
            turn_by_turn_path=itinerary,
            total_route_distance_km=total_distance,
            stage_runtimes_ms=runtimes
        )

    def print_plan_summary(self, plan: DeliveryPlan, show_dp_table: bool = True) -> str:
        """Generates a comprehensive terminal report of the delivery plan."""
        lines = []
        lines.append("=" * 80)
        lines.append("        MINI-COURIER PLANNER: OPTIMIZED TRIP MANIFEST & ROUTE")
        lines.append("=" * 80)

        # 1. Prioritization summary
        lines.append("\n[1] PARCEL PRIORITIZATION (Deadline & Urgency Sorting)")
        lines.append(f"{'Rank':<5} {'ID':<6} {'Customer':<15} {'Destination':<14} {'Weight':<8} {'Deadline':<10} {'Priority':<9} {'Utility'}")
        lines.append("-" * 80)
        for rank, p in enumerate(plan.sorted_parcels, 1):
            lines.append(
                f"{rank:<5} {p.id:<6} {p.customer_name:<15} {p.destination:<14} {p.weight:>4} kg   "
                f"{p.deadline_hours:>4.1f} hrs    {p.priority:>4}/10    {p.value:>5}"
            )

        # 2. Knapsack Packing summary
        lines.append("\n[2] VEHICLE PACKING OPTIMIZATION (0/1 Knapsack Dynamic Programming)")
        lines.append(f"* Vehicle Maximum Weight Capacity: {plan.vehicle_capacity} kg")
        lines.append(f"* Total Loaded Weight:             {plan.total_weight} kg")
        lines.append(f"* Vehicle Capacity Utilization:    {plan.capacity_utilization_pct}%")
        lines.append(f"* Total Delivered Utility Score:   {plan.total_value} pts")
        lines.append(f"* Accepted Parcels for Trip:       {len(plan.selected_parcels)} items")
        for p in plan.selected_parcels:
            lines.append(f"    [LOADED]   [{p.id}] -> {p.customer_name} ({p.destination}) | {p.weight} kg, priority {p.priority}")

        if plan.deferred_parcels:
            lines.append(f"* Deferred Parcels (Next Trip):    {len(plan.deferred_parcels)} items")
            for p in plan.deferred_parcels:
                lines.append(f"    [DEFERRED] [{p.id}] -> {p.customer_name} ({p.destination}) | {p.weight} kg (exceeds capacity)")

        # Optional DP Table output evidence
        if show_dp_table and len(plan.sorted_parcels) <= 10 and plan.vehicle_capacity <= 30:
            lines.append("\n[2B] DYNAMIC PROGRAMMING 2D TABLE MATRIX:")
            lines.append(format_dp_table(plan.dp_table, plan.sorted_parcels, max_cols=plan.vehicle_capacity))

        # 3. Route & Dijkstra Path
        lines.append("\n[3] DELIVERY ROUTE & SHORTEST PATHS (Dijkstra + Nearest-Neighbor TSP)")
        lines.append(f"* Sequence of Delivery Stops:      {' -> '.join(plan.delivery_route)}")
        lines.append(f"* Total Route Distance:            {plan.total_route_distance_km:.2f} km")
        lines.append(f"* Turn-by-Turn Road Waypoints:     {' -> '.join(plan.turn_by_turn_path)}")

        # 4. Performance Runtimes
        lines.append("\n[4] ALGORITHMIC RUNTIME BREAKDOWN")
        for stage, duration in plan.stage_runtimes_ms.items():
            lines.append(f"  * {stage:<25}: {duration:>8.4f} ms")

        lines.append("=" * 80)
        report_str = "\n".join(lines)
        return report_str
