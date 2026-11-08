"""
Unit Tests for 0/1 Knapsack Dynamic Programming
Design & Analysis of Algorithms (ETCCDA302)
"""

import unittest
import sys
import os

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
parent_dir = os.path.abspath(os.path.join(base_dir, ".."))
for p in [base_dir, parent_dir]:
    if p not in sys.path:
        sys.path.insert(0, p)

try:
    from mini_courier_planner.src.models import Parcel
    from mini_courier_planner.src.phase2_prioritization import (
        knapsack_01_dp,
        knapsack_space_optimized_1d
    )
except ModuleNotFoundError:
    from src.models import Parcel
    from src.phase2_prioritization import (
        knapsack_01_dp,
        knapsack_space_optimized_1d
    )


class TestKnapsackDP(unittest.TestCase):

    def setUp(self):
        self.parcels = [
            Parcel(id="P1", customer_name="A", destination="Sec14", weight=2, priority=1, deadline_hours=1, value=3),
            Parcel(id="P2", customer_name="B", destination="Sec29", weight=3, priority=1, deadline_hours=1, value=4),
            Parcel(id="P3", customer_name="C", destination="CyberCity", weight=4, priority=1, deadline_hours=1, value=5),
            Parcel(id="P4", customer_name="D", destination="GolfCourse", weight=5, priority=1, deadline_hours=1, value=8),
        ]

    def test_knapsack_optimal_value(self):
        selected, deferred, table, max_val = knapsack_01_dp(self.parcels, capacity=5)
        self.assertEqual(max_val, 8)
        self.assertEqual(len(selected), 1)
        self.assertEqual(selected[0].id, "P4")
        self.assertEqual(sum(p.weight for p in selected), 5)
        self.assertEqual(len(deferred), 3)

    def test_knapsack_capacity_zero(self):
        selected, deferred, table, max_val = knapsack_01_dp(self.parcels, capacity=0)
        self.assertEqual(max_val, 0)
        self.assertEqual(len(selected), 0)
        self.assertEqual(len(deferred), len(self.parcels))

    def test_1d_vs_2d_dp_equivalence(self):
        for cap in [5, 7, 9, 14]:
            _, _, _, val_2d = knapsack_01_dp(self.parcels, capacity=cap)
            val_1d, _ = knapsack_space_optimized_1d(self.parcels, capacity=cap)
            self.assertEqual(val_2d, val_1d)


if __name__ == "__main__":
    unittest.main()
