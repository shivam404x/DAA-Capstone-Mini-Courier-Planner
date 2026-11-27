"""
Phase 4: Performance Testing and Optimization
Design & Analysis of Algorithms (ETCCDA302)
K.R. Mangalam University, Gurugram

This module executes empirical benchmarking across multiple problem sizes (N),
records runtimes of all major algorithmic steps, analyzes Big-O scaling,
and generates publication-grade PNG charts using Pillow.
"""

import time
import random
from typing import List, Dict, Tuple
from PIL import Image, ImageDraw, ImageFont

from .models import Parcel
from .phase1_design import RoadNetworkGraph, build_default_gurugram_graph
from .phase2_prioritization import (
    merge_sort_parcels,
    quick_sort_parcels,
    knapsack_01_dp,
    knapsack_space_optimized_1d
)
from .phase3_routing import (
    compute_metric_distance_matrix,
    nearest_neighbor_tsp,
    two_opt_optimize
)


def generate_synthetic_parcels(count: int, nodes: List[str], seed: int = 100) -> List[Parcel]:
    """Generates synthetic parcels for performance scaling."""
    rnd = random.Random(seed)
    parcels = []
    dest_candidates = [n for n in nodes if n != "Hub"]
    for i in range(1, count + 1):
        pid = f"P{i:04d}"
        dest = rnd.choice(dest_candidates)
        weight = rnd.randint(1, 15)
        priority = rnd.randint(1, 10)
        deadline = round(rnd.uniform(1.0, 24.0), 2)
        urgency = max(1, int(24 - deadline))
        val = priority * 10 + urgency
        parcels.append(Parcel(
            id=pid,
            customer_name=f"Customer_{i}",
            destination=dest,
            weight=weight,
            priority=priority,
            deadline_hours=deadline,
            value=val
        ))
    return parcels


def run_comprehensive_benchmark() -> Dict[str, List]:
    """
    Benchmarks all algorithms across varying input sizes N = [10, 25, 50, 100, 250, 500].
    Returns recorded execution times in milliseconds.
    """
    input_sizes = [10, 25, 50, 100, 250, 500]
    graph = build_default_gurugram_graph()
    nodes = graph.get_nodes()

    results = {
        "sizes": input_sizes,
        "merge_sort_ms": [],
        "quick_sort_ms": [],
        "knapsack_2d_ms": [],
        "knapsack_1d_ms": [],
        "dijkstra_ms": [],
        "tsp_nn_ms": [],
        "tsp_2opt_ms": []
    }

    for n in input_sizes:
        capacity = max(20, n * 2)
        parcels = generate_synthetic_parcels(n, nodes, seed=n)

        # 1. Merge Sort vs Quick Sort
        t0 = time.perf_counter()
        _ = merge_sort_parcels(parcels)
        t1 = time.perf_counter()
        results["merge_sort_ms"].append((t1 - t0) * 1000.0)

        t0 = time.perf_counter()
        _ = quick_sort_parcels(parcels)
        t1 = time.perf_counter()
        results["quick_sort_ms"].append((t1 - t0) * 1000.0)

        # 2. Knapsack 2D DP vs 1D DP
        # Use a capped subset for 2D knapsack at large sizes to maintain snappy interactive test
        knapsack_items = parcels[:min(n, 120)]
        k_cap = min(capacity, 150)

        t0 = time.perf_counter()
        selected, _, _, _ = knapsack_01_dp(knapsack_items, k_cap)
        t1 = time.perf_counter()
        results["knapsack_2d_ms"].append((t1 - t0) * 1000.0)

        t0 = time.perf_counter()
        _ = knapsack_space_optimized_1d(knapsack_items, k_cap)
        t1 = time.perf_counter()
        results["knapsack_1d_ms"].append((t1 - t0) * 1000.0)

        # 3. Dijkstra All-Pairs
        active_stops = ["Hub"] + list({p.destination for p in selected})
        t0 = time.perf_counter()
        dist_matrix, _ = compute_metric_distance_matrix(graph, active_stops)
        t1 = time.perf_counter()
        results["dijkstra_ms"].append((t1 - t0) * 1000.0)

        # 4. Nearest Neighbor TSP vs 2-Opt
        stops = [p.destination for p in selected]
        t0 = time.perf_counter()
        route, _ = nearest_neighbor_tsp("Hub", stops, dist_matrix)
        t1 = time.perf_counter()
        results["tsp_nn_ms"].append((t1 - t0) * 1000.0)

        t0 = time.perf_counter()
        _ = two_opt_optimize(route, dist_matrix)
        t1 = time.perf_counter()
        results["tsp_2opt_ms"].append((t1 - t0) * 1000.0)

    return results


def draw_chart(
    title: str,
    x_labels: List[str],
    series: List[Tuple[str, List[float], Tuple[int, int, int]]],
    output_path: str,
    y_axis_label: str = "Execution Time (ms)",
    width: int = 900,
    height: int = 550
) -> None:
    """
    Renders a high-resolution graphical line chart with a legend and grid
    directly into a PNG image using Pillow.
    """
    img = Image.new("RGB", (width, height), color=(250, 252, 255))
    draw = ImageDraw.Draw(img)

    margin_left = 90
    margin_right = 50
    margin_top = 70
    margin_bottom = 80

    plot_w = width - margin_left - margin_right
    plot_h = height - margin_top - margin_bottom

    # Determine max Y value
    max_y = max(max(vals) for _, vals, _ in series if vals)
    if max_y <= 0:
        max_y = 1.0
    # Add 20% headroom
    max_y *= 1.25

    # Draw Chart Title
    draw.text((margin_left, 20), title, fill=(20, 30, 60))

    # Draw Axes
    x_axis_y = margin_top + plot_h
    draw.line([(margin_left, margin_top), (margin_left, x_axis_y)], fill=(120, 130, 140), width=2)
    draw.line([(margin_left, x_axis_y), (margin_left + plot_w, x_axis_y)], fill=(120, 130, 140), width=2)

    # Horizontal grid lines
    num_y_ticks = 5
    for i in range(num_y_ticks + 1):
        val = (max_y / num_y_ticks) * i
        y_pos = x_axis_y - int((val / max_y) * plot_h)
        draw.line([(margin_left, y_pos), (margin_left + plot_w, y_pos)], fill=(225, 230, 238), width=1)
        draw.text((margin_left - 75, y_pos - 7), f"{val:5.2f}", fill=(80, 90, 100))

    # Y-axis label
    draw.text((margin_left - 80, margin_top - 25), y_axis_label, fill=(40, 50, 70))

    # X-axis ticks & labels
    num_x = len(x_labels)
    x_step = plot_w / max(1, num_x - 1) if num_x > 1 else plot_w

    x_coords = []
    for idx, label in enumerate(x_labels):
        x_pos = margin_left + int(idx * x_step)
        x_coords.append(x_pos)
        draw.line([(x_pos, x_axis_y), (x_pos, x_axis_y + 6)], fill=(120, 130, 140), width=2)
        draw.text((x_pos - 15, x_axis_y + 12), f"N={label}", fill=(50, 60, 70))

    # Draw lines and points for each series
    legend_x = margin_left + 15
    legend_y = margin_top + 10

    for s_idx, (name, values, color) in enumerate(series):
        pts = []
        for idx, val in enumerate(values):
            x = x_coords[idx]
            y = x_axis_y - int((val / max_y) * plot_h)
            pts.append((x, y))

        # Draw connecting line
        for k in range(len(pts) - 1):
            draw.line([pts[k], pts[k + 1]], fill=color, width=3)

        # Draw circle dots
        for (x, y) in pts:
            r = 4
            draw.ellipse([(x - r, y - r), (x + r, y + r)], fill=color, outline=(255, 255, 255), width=1)

        # Legend Entry
        l_y = legend_y + (s_idx * 22)
        draw.line([(legend_x, l_y + 6), (legend_x + 25, l_y + 6)], fill=color, width=3)
        draw.ellipse([(legend_x + 9, l_y + 3), (legend_x + 16, l_y + 9)], fill=color)
        draw.text((legend_x + 35, l_y), name, fill=(30, 30, 30))

    # Student & University Watermark
    footer = "K.R. Mangalam University | ETCCDA302 Capstone Project | Shivam Kumar Roy"
    draw.text((margin_left, height - 30), footer, fill=(130, 140, 160))

    img.save(output_path)


def generate_all_runtime_charts(results: Dict[str, List], output_dir: str) -> List[str]:
    """Generates all required PNG charts and returns their file paths."""
    x_labels = [str(n) for n in results["sizes"]]
    generated_files = []

    # Chart 1: Merge Sort vs Quick Sort
    p1 = f"{output_dir}/sorting_comparison.png"
    draw_chart(
        title="Sorting Performance: Merge Sort vs. Quick Sort",
        x_labels=x_labels,
        series=[
            ("Merge Sort O(N log N) Stable", results["merge_sort_ms"], (41, 128, 185)),
            ("Quick Sort O(N log N) In-place", results["quick_sort_ms"], (231, 76, 60))
        ],
        output_path=p1
    )
    generated_files.append(p1)

    # Chart 2: 0/1 Knapsack DP Scaling (2D Table vs 1D Optimized)
    p2 = f"{output_dir}/knapsack_dp_scaling.png"
    draw_chart(
        title="Dynamic Programming: 0/1 Knapsack (2D Table vs 1D Optimized)",
        x_labels=x_labels,
        series=[
            ("Knapsack 2D DP Table O(N*W)", results["knapsack_2d_ms"], (142, 68, 173)),
            ("Knapsack 1D Memory-Optimized O(W)", results["knapsack_1d_ms"], (39, 174, 96))
        ],
        output_path=p2
    )
    generated_files.append(p2)

    # Chart 3: Graph Routing (Dijkstra vs TSP Nearest-Neighbor)
    p3 = f"{output_dir}/graph_routing_scaling.png"
    draw_chart(
        title="Graph Algorithms: Dijkstra All-Pairs vs TSP Nearest-Neighbor",
        x_labels=x_labels,
        series=[
            ("Dijkstra Shortest Paths O((V+E)log V)", results["dijkstra_ms"], (243, 156, 18)),
            ("Nearest-Neighbor TSP O(K^2)", results["tsp_nn_ms"], (22, 160, 133)),
            ("2-Opt Route Refinement", results["tsp_2opt_ms"], (192, 57, 43))
        ],
        output_path=p3
    )
    generated_files.append(p3)

    # Chart 4: Integrated Pipeline End-to-End Comparison
    total_runtimes = [
        results["merge_sort_ms"][i] + results["knapsack_2d_ms"][i] + results["dijkstra_ms"][i] + results["tsp_nn_ms"][i]
        for i in range(len(results["sizes"]))
    ]
    p4 = f"{output_dir}/integrated_system_runtime.png"
    draw_chart(
        title="Integrated Mini-Courier Planner: End-to-End Pipeline Runtime",
        x_labels=x_labels,
        series=[
            ("Total Pipeline Execution Time (ms)", total_runtimes, (44, 62, 80))
        ],
        output_path=p4
    )
    generated_files.append(p4)

    return generated_files


def format_benchmark_table(results: Dict[str, List]) -> str:
    """Prints a formatted ASCII comparison table for the report and terminal."""
    lines = []
    lines.append("=" * 95)
    lines.append("       PHASE 4: EMPIRICAL BENCHMARKING & COMPLEXITY ANALYSIS")
    lines.append("=" * 95)
    header = (
        f"{'Input (N)':<10} | {'MergeSort(ms)':<14} | {'QuickSort(ms)':<14} | "
        f"{'Knapsack2D(ms)':<14} | {'Dijkstra(ms)':<12} | {'TSP-NN(ms)':<11} | {'2-Opt(ms)':<10}"
    )
    sep = "-" * 95
    lines.extend([header, sep])

    for i, n in enumerate(results["sizes"]):
        row = (
            f"N={n:<8} | {results['merge_sort_ms'][i]:<14.4f} | {results['quick_sort_ms'][i]:<14.4f} | "
            f"{results['knapsack_2d_ms'][i]:<14.4f} | {results['dijkstra_ms'][i]:<12.4f} | "
            f"{results['tsp_nn_ms'][i]:<11.4f} | {results['tsp_2opt_ms'][i]:<10.4f}"
        )
        lines.append(row)

    lines.append(sep)
    lines.append("\nTheoretical Complexity Mapping:")
    lines.append("  * Sorting: Merge Sort = O(N log N) guaranteed, Quick Sort = O(N log N) avg, O(N^2) worst-case.")
    lines.append("  * Knapsack DP: 2D Table = O(N * W) time, O(N * W) space. 1D Table = O(N * W) time, O(W) space.")
    lines.append("  * Shortest Path: Dijkstra with Min-Heap = O((V + E) log V) time, O(V) space.")
    lines.append("  * Route Sequencing: Nearest-Neighbor TSP = O(K^2) time where K <= V is number of delivery stops.")
    lines.append("=" * 95)
    return "\n".join(lines)
