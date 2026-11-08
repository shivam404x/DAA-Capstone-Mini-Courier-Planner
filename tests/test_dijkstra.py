"""
Unit Tests for Dijkstra's Shortest Path Algorithm
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
    from mini_courier_planner.src.phase1_design import RoadNetworkGraph, build_default_gurugram_graph
    from mini_courier_planner.src.phase3_routing import dijkstra_shortest_path, reconstruct_path
except ModuleNotFoundError:
    from src.phase1_design import RoadNetworkGraph, build_default_gurugram_graph
    from src.phase3_routing import dijkstra_shortest_path, reconstruct_path


class TestDijkstra(unittest.TestCase):

    def setUp(self):
        self.g = RoadNetworkGraph()
        # Triangle graph: A --2-- B --3-- C, A --6-- C
        self.g.add_edge("A", "B", 2.0)
        self.g.add_edge("B", "C", 3.0)
        self.g.add_edge("A", "C", 6.0)

    def test_shortest_path_distance(self):
        distances, parents = dijkstra_shortest_path(self.g, "A")
        self.assertEqual(distances["A"], 0.0)
        self.assertEqual(distances["B"], 2.0)
        # Shortest to C should be A->B->C (2 + 3 = 5), not direct A->C (6)
        self.assertEqual(distances["C"], 5.0)

    def test_path_reconstruction(self):
        distances, parents = dijkstra_shortest_path(self.g, "A")
        path = reconstruct_path(parents, "A", "C")
        self.assertEqual(path, ["A", "B", "C"])

    def test_gurugram_graph_reachability(self):
        gurugram_g = build_default_gurugram_graph()
        distances, parents = dijkstra_shortest_path(gurugram_g, "Hub")
        for node in gurugram_g.get_nodes():
            self.assertLess(distances[node], float("inf"), f"Node {node} should be reachable from Hub")


if __name__ == "__main__":
    unittest.main()
