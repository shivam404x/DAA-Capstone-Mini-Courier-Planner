"""
Unit Tests for Nearest-Neighbor TSP Approximation
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
    from mini_courier_planner.src.phase1_design import build_default_gurugram_graph
    from mini_courier_planner.src.phase3_routing import (
        compute_metric_distance_matrix,
        nearest_neighbor_tsp,
        two_opt_optimize
    )
except ModuleNotFoundError:
    from src.phase1_design import build_default_gurugram_graph
    from src.phase3_routing import (
        compute_metric_distance_matrix,
        nearest_neighbor_tsp,
        two_opt_optimize
    )


class TestTSP(unittest.TestCase):

    def setUp(self):
        self.g = build_default_gurugram_graph()
        self.stops = ["Sec14", "CyberCity", "GolfCourse", "Sec49"]
        self.active_nodes = ["Hub"] + self.stops
        self.dist_matrix, _ = compute_metric_distance_matrix(self.g, self.active_nodes)

    def test_tour_starts_and_ends_at_hub(self):
        route, total_dist = nearest_neighbor_tsp("Hub", self.stops, self.dist_matrix)
        self.assertEqual(route[0], "Hub")
        self.assertEqual(route[-1], "Hub")
        self.assertGreater(total_dist, 0.0)

    def test_tour_visits_all_stops(self):
        route, total_dist = nearest_neighbor_tsp("Hub", self.stops, self.dist_matrix)
        visited = set(route)
        for stop in self.stops:
            self.assertIn(stop, visited)

    def test_two_opt_improvement(self):
        route, dist1 = nearest_neighbor_tsp("Hub", self.stops, self.dist_matrix)
        opt_route, dist2 = two_opt_optimize(route, self.dist_matrix)
        self.assertLessEqual(dist2, dist1, "2-Opt must not increase the route distance")


if __name__ == "__main__":
    unittest.main()
