"""
Unit Tests for Sorting Algorithms (Merge Sort & Quick Sort)
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
        merge_sort_parcels,
        quick_sort_parcels,
        parcel_sort_key
    )
except ModuleNotFoundError:
    from src.models import Parcel
    from src.phase2_prioritization import (
        merge_sort_parcels,
        quick_sort_parcels,
        parcel_sort_key
    )


class TestSortingAlgorithms(unittest.TestCase):

    def setUp(self):
        self.parcels = [
            Parcel(id="P1", customer_name="Alice", destination="Sec14", weight=5, priority=5, deadline_hours=4.0),
            Parcel(id="P2", customer_name="Bob", destination="CyberCity", weight=3, priority=9, deadline_hours=1.0),
            Parcel(id="P3", customer_name="Charlie", destination="Sec29", weight=6, priority=8, deadline_hours=2.5),
            Parcel(id="P4", customer_name="David", destination="GolfCourse", weight=2, priority=4, deadline_hours=1.0),
        ]

    def test_merge_sort_order(self):
        sorted_p = merge_sort_parcels(self.parcels)
        self.assertEqual(sorted_p[0].id, "P2")
        self.assertEqual(sorted_p[1].id, "P4")
        self.assertEqual(sorted_p[2].id, "P3")
        self.assertEqual(sorted_p[3].id, "P1")

    def test_quick_sort_order(self):
        sorted_p = quick_sort_parcels(self.parcels)
        self.assertEqual(sorted_p[0].id, "P2")
        self.assertEqual(sorted_p[1].id, "P4")
        self.assertEqual(sorted_p[2].id, "P3")
        self.assertEqual(sorted_p[3].id, "P1")

    def test_empty_and_single_element(self):
        self.assertEqual(merge_sort_parcels([]), [])
        self.assertEqual(quick_sort_parcels([]), [])

        single = [self.parcels[0]]
        self.assertEqual(merge_sort_parcels(single), single)
        self.assertEqual(quick_sort_parcels(single), single)

    def test_sorting_preserves_count(self):
        sorted_merge = merge_sort_parcels(self.parcels)
        sorted_quick = quick_sort_parcels(self.parcels)
        self.assertEqual(len(sorted_merge), len(self.parcels))
        self.assertEqual(len(sorted_quick), len(self.parcels))


if __name__ == "__main__":
    unittest.main()
