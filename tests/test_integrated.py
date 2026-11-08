"""
Integration Tests for Mini-Courier Planner
Design & Analysis of Algorithms (ETCCDA302)
"""

import unittest
import json
import sys
import os

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
parent_dir = os.path.abspath(os.path.join(base_dir, ".."))
for p in [base_dir, parent_dir]:
    if p not in sys.path:
        sys.path.insert(0, p)

try:
    from mini_courier_planner.src.models import Parcel
    from mini_courier_planner.src.phase1_design import build_default_gurugram_graph
    from mini_courier_planner.src.courier_system import MiniCourierPlanner
except ModuleNotFoundError:
    from src.models import Parcel
    from src.phase1_design import build_default_gurugram_graph
    from src.courier_system import MiniCourierPlanner


class TestIntegratedSystem(unittest.TestCase):

    def setUp(self):
        self.planner = MiniCourierPlanner(graph=build_default_gurugram_graph(), hub_node="Hub")
        self.data_dir = os.path.join(base_dir, "data")

    def test_sample_small_pipeline(self):
        file_path = os.path.join(self.data_dir, "sample_small.json")
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        parcels = [Parcel.from_dict(p) for p in data["parcels"]]
        capacity = data["vehicle_capacity_kg"]

        plan = self.planner.plan_trip(parcels, vehicle_capacity=capacity)

        # Verification of constraints
        self.assertLessEqual(plan.total_weight, capacity)
        self.assertEqual(plan.total_weight, sum(p.weight for p in plan.selected_parcels))
        self.assertGreater(len(plan.selected_parcels), 0)
        self.assertEqual(plan.delivery_route[0], "Hub")
        self.assertEqual(plan.delivery_route[-1], "Hub")
        self.assertGreater(plan.total_route_distance_km, 0.0)

    def test_unseen_dataset_pipeline(self):
        file_path = os.path.join(self.data_dir, "unseen_test.json")
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        parcels = [Parcel.from_dict(p) for p in data["parcels"]]
        capacity = data["vehicle_capacity_kg"]

        plan = self.planner.plan_trip(parcels, vehicle_capacity=capacity)
        self.assertLessEqual(plan.total_weight, capacity)
        self.assertGreater(plan.total_value, 0)
        self.assertIn("Hub", plan.delivery_route)


if __name__ == "__main__":
    unittest.main()
