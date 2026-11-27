"""
Mini-Courier Planner - Artifact & Screenshot Generator
Design & Analysis of Algorithms (ETCCDA302)
K.R. Mangalam University

Generates terminal trace logs and publication-quality screenshot images
for Phase 5 evidence and submission.
"""

import os
import sys
import json
from PIL import Image, ImageDraw, ImageFont

# Add base directory to path
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, BASE_DIR)

from src.models import Parcel
from src.phase1_design import build_default_gurugram_graph, get_architecture_overview
from src.phase2_prioritization import knapsack_01_dp, format_dp_table
from src.phase3_routing import compute_metric_distance_matrix, nearest_neighbor_tsp
from src.phase4_benchmark import run_comprehensive_benchmark, generate_all_runtime_charts, format_benchmark_table
from src.courier_system import MiniCourierPlanner


def render_text_to_terminal_image(
    text_content: str,
    output_png_path: str,
    title: str = "Terminal Output",
    width: int = 1000,
    font_size: int = 14
):
    """
    Renders text to a clean developer-style dark-mode terminal window screenshot.
    """
    lines = text_content.splitlines()
    line_height = int(font_size * 1.5)
    header_height = 45
    padding = 20
    calc_height = header_height + (len(lines) * line_height) + (padding * 2)
    height = max(500, min(calc_height, 2200))

    img = Image.new("RGB", (width, height), color=(30, 30, 36))
    draw = ImageDraw.Draw(img)

    # Window Header Bar
    draw.rectangle([(0, 0), (width, header_height)], fill=(45, 45, 55))
    # macOS/Linux-style window action buttons
    draw.ellipse([(15, 16), (27, 28)], fill=(255, 95, 86))    # Close (Red)
    draw.ellipse([(35, 16), (47, 28)], fill=(255, 189, 46))   # Minimize (Yellow)
    draw.ellipse([(55, 16), (67, 28)], fill=(39, 201, 63))    # Expand (Green)

    # Header Title
    draw.text((80, 15), f"ETCCDA302 Capstone - {title}", fill=(200, 205, 215))

    # Content
    y_pos = header_height + padding
    for line in lines:
        if y_pos + line_height > height - padding:
            break

        # Subtle syntax highlighting for terminal readability
        if line.startswith("="):
            color = (100, 181, 246)
        elif line.startswith("[") or "PHASE" in line:
            color = (255, 209, 102)
        elif "✔" in line or "Loaded" in line:
            color = (106, 237, 140)
        elif "⏳" in line or "Deferred" in line:
            color = (240, 138, 93)
        elif line.startswith("•"):
            color = (220, 220, 220)
        else:
            color = (190, 195, 205)

        draw.text((padding, y_pos), line, fill=color)
        y_pos += line_height

    img.save(output_png_path)
    print(f"Rendered terminal screenshot: {output_png_path}")


def generate_all_artifacts():
    """Generates all output traces, charts, and screenshot evidence."""
    chart_dir = os.path.join(BASE_DIR, "output", "charts")
    screenshot_dir = os.path.join(BASE_DIR, "output", "screenshots")
    os.makedirs(chart_dir, exist_ok=True)
    os.makedirs(screenshot_dir, exist_ok=True)

    print("Step 1: Running Phase 4 Benchmarking & Generating Runtime Charts...")
    bench_results = run_comprehensive_benchmark()
    bench_text = format_benchmark_table(bench_results)
    generate_all_runtime_charts(bench_results, chart_dir)

    with open(os.path.join(BASE_DIR, "output", "trace_benchmark.txt"), "w", encoding="utf-8") as f:
        f.write(bench_text)

    render_text_to_terminal_image(
        bench_text,
        os.path.join(screenshot_dir, "screenshot_phase4_benchmark.png"),
        title="Performance Benchmarking & Complexity Scaling Analysis"
    )

    print("\nStep 2: Running Small Dataset Plan (Phase 2 & 3 Tracing)...")
    planner = MiniCourierPlanner(graph=build_default_gurugram_graph(), hub_node="Hub")
    with open(os.path.join(BASE_DIR, "data", "sample_small.json"), "r", encoding="utf-8") as f:
        small_data = json.load(f)
    small_parcels = [Parcel.from_dict(p) for p in small_data["parcels"]]
    small_plan = planner.plan_trip(small_parcels, vehicle_capacity=small_data["vehicle_capacity_kg"])
    small_summary = planner.print_plan_summary(small_plan, show_dp_table=True)

    with open(os.path.join(BASE_DIR, "output", "trace_small_run.txt"), "w", encoding="utf-8") as f:
        f.write(small_summary)

    render_text_to_terminal_image(
        small_summary,
        os.path.join(screenshot_dir, "screenshot_phase2_3_small_dataset.png"),
        title="Small Dataset Execution & Dynamic Programming Table Matrix"
    )

    print("\nStep 3: Running Unseen Dataset Evaluation (Viva Readiness)...")
    with open(os.path.join(BASE_DIR, "data", "unseen_test.json"), "r", encoding="utf-8") as f:
        unseen_data = json.load(f)
    unseen_parcels = [Parcel.from_dict(p) for p in unseen_data["parcels"]]
    unseen_plan = planner.plan_trip(unseen_parcels, vehicle_capacity=unseen_data["vehicle_capacity_kg"])
    unseen_summary = planner.print_plan_summary(unseen_plan, show_dp_table=True)

    with open(os.path.join(BASE_DIR, "output", "trace_unseen_run.txt"), "w", encoding="utf-8") as f:
        f.write(unseen_summary)

    render_text_to_terminal_image(
        unseen_summary,
        os.path.join(screenshot_dir, "screenshot_phase5_unseen_evaluation.png"),
        title="Unseen Dataset Evaluation & Route Optimization"
    )

    print("\nStep 4: Rendering Architecture Overview Screenshot (Phase 1)...")
    arch_text = get_architecture_overview()
    render_text_to_terminal_image(
        arch_text,
        os.path.join(screenshot_dir, "screenshot_phase1_architecture.png"),
        title="System Architecture, Road Graph & Algorithmic Pipeline"
    )

    print("\nAll artifacts and evidence successfully generated in 'mini_courier_planner/output/'!")


if __name__ == "__main__":
    generate_all_artifacts()
