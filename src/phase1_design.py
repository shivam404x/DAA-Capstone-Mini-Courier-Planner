"""
Phase 1: Courier Problem Design and Planning
Design & Analysis of Algorithms (ETCCDA302)
K.R. Mangalam University, Gurugram

This module defines:
1. System Architecture & Integrated Data Flow.
2. Weighted Graph representation (Adjacency List).
3. Built-in Gurugram Delivery Network topology.
"""

from typing import Dict, List, Tuple, Optional, Set
import json


class RoadNetworkGraph:
    """
    Weighted road network graph using an adjacency list.
    Vertices (nodes) represent the Central Hub and Customer Delivery Points.
    Edges represent bidirectional road segments with travel distances (weights in km).
    """

    def __init__(self):
        # adj_list maps: node -> list of (neighbor_node, weight_km)
        self.adj_list: Dict[str, List[Tuple[str, float]]] = {}
        self.node_metadata: Dict[str, Dict[str, str]] = {}

    def add_node(self, node_id: str, name: str = "", zone: str = "") -> None:
        """Register a delivery node or hub in the network."""
        if node_id not in self.adj_list:
            self.adj_list[node_id] = []
            self.node_metadata[node_id] = {
                "name": name or node_id,
                "zone": zone or "General"
            }

    def add_edge(self, u: str, v: str, distance_km: float, bidirectional: bool = True) -> None:
        """Add a weighted road connection between node u and node v."""
        if u not in self.adj_list:
            self.add_node(u)
        if v not in self.adj_list:
            self.add_node(v)

        # Avoid duplicate edges
        self.adj_list[u] = [(n, w) for n, w in self.adj_list[u] if n != v]
        self.adj_list[u].append((v, float(distance_km)))

        if bidirectional:
            self.adj_list[v] = [(n, w) for n, w in self.adj_list[v] if n != u]
            self.adj_list[v].append((u, float(distance_km)))

    def get_neighbors(self, node_id: str) -> List[Tuple[str, float]]:
        """Return all adjacent neighbors and distance weights for a given node."""
        return self.adj_list.get(node_id, [])

    def get_nodes(self) -> List[str]:
        """Return list of all registered nodes in the graph."""
        return list(self.adj_list.keys())

    def get_edges(self) -> List[Tuple[str, str, float]]:
        """Return all unique edges in the graph."""
        seen = set()
        edges = []
        for u in self.adj_list:
            for v, w in self.adj_list[u]:
                edge_id = tuple(sorted([u, v]))
                if edge_id not in seen:
                    seen.add(edge_id)
                    edges.append((u, v, w))
        return edges

    def to_dict(self) -> Dict:
        """Serialize graph to dictionary."""
        return {
            "nodes": [
                {"id": k, **v} for k, v in self.node_metadata.items()
            ],
            "edges": [
                {"from": u, "to": v, "distance_km": w}
                for u, v, w in self.get_edges()
            ]
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "RoadNetworkGraph":
        """Deserialize graph from dictionary."""
        graph = cls()
        for node in data.get("nodes", []):
            graph.add_node(node["id"], node.get("name", ""), node.get("zone", ""))
        for edge in data.get("edges", []):
            graph.add_edge(edge["from"], edge["to"], edge["distance_km"], edge.get("bidirectional", True))
        return graph


def build_default_gurugram_graph() -> RoadNetworkGraph:
    """
    Constructs a realistic Gurugram delivery road network centered at
    Central Hub (KRMU Logistics Center / Sohna Road).
    """
    g = RoadNetworkGraph()

    # Define Nodes (Depot Hub + Key Gurugram / Cyber City Delivery Zones)
    nodes = [
        ("Hub", "Central Logistics Hub (Sohna Road)", "Depot"),
        ("Sec49", "Sector 49 Commercial Hub", "South Gurugram"),
        ("Sec47", "Sector 47 Residential Park", "South Gurugram"),
        ("SubhashChowk", "Subhash Chowk Junction", "Transit Hub"),
        ("Sec14", "Sector 14 Old Gurugram Market", "Central Gurugram"),
        ("Sec29", "Sector 29 Leisure Valley Sector", "Commercial Hub"),
        ("CyberCity", "DLF Cyber City Tech Park", "North Gurugram"),
        ("GolfCourse", "Golf Course Road Towers", "East Gurugram"),
        ("Sec56", "Sector 56 Metro Station Hub", "East Gurugram"),
        ("UdyogVihar", "Udyog Vihar Industrial Zone", "North Gurugram"),
        ("RajivChowk", "Rajiv Chowk Highway Crossing", "Central Highway"),
    ]

    for node_id, name, zone in nodes:
        g.add_node(node_id, name, zone)

    # Road Segments (Distances in Kilometers)
    road_edges = [
        ("Hub", "Sec49", 3.2),
        ("Hub", "SubhashChowk", 4.5),
        ("Sec49", "Sec47", 2.8),
        ("Sec49", "SohnaRoad" if "SohnaRoad" in [n[0] for n in nodes] else "Sec56", 6.1),
        ("Sec47", "SubhashChowk", 2.4),
        ("Sec47", "RajivChowk", 5.0),
        ("SubhashChowk", "RajivChowk", 3.5),
        ("RajivChowk", "Sec14", 4.2),
        ("RajivChowk", "Sec29", 5.8),
        ("Sec14", "Sec29", 3.9),
        ("Sec14", "UdyogVihar", 6.5),
        ("Sec29", "CyberCity", 4.1),
        ("Sec29", "GolfCourse", 4.8),
        ("CyberCity", "UdyogVihar", 3.0),
        ("CyberCity", "GolfCourse", 5.2),
        ("GolfCourse", "Sec56", 3.6),
        ("Sec56", "Sec49", 5.4),
    ]

    for u, v, w in road_edges:
        g.add_edge(u, v, w, bidirectional=True)

    return g


def get_architecture_overview() -> str:
    """Returns the formal architectural pipeline design of Mini-Courier Planner."""
    return """
================================================================================
          MINI-COURIER PLANNER - SYSTEM ARCHITECTURE (PHASE 1)
================================================================================
Problem Statement:
Given a list of customer parcels (with weights, deadlines, and priorities) and a 
road network graph of delivery locations, generate:
  1. An optimized packing manifest that respects vehicle capacity.
  2. An ordered delivery route minimizing total travel distance.

Algorithmic Integration Pipeline:
+------------------------------------------------------------------------------+
| [Input Dataset] Raw Parcels (ID, Destination, Weight, Deadline, Priority)     |
+------------------------------------------------------------------------------+
                                       │
                                       ▼
+------------------------------------------------------------------------------+
| PHASE 2A: PARCEL PRIORITIZATION (Sorting Algorithms)                        |
| • Implemented via Merge Sort (Stable, O(N log N)) & Quick Sort              |
| • Sort Criterion: Primary = Earliest Deadline, Secondary = Priority Score   |
+------------------------------------------------------------------------------+
                                       │
                                       ▼
+------------------------------------------------------------------------------+
| PHASE 2B: VEHICLE CAPACITY ALLOCATION (0/1 Knapsack Dynamic Programming)     |
| • State: DP[i][w] = Max utility using first i parcels within weight w        |
| • Backtracking reconstruction to select optimal subset of parcels            |
| • Output: Loaded parcels for current trip + Deferred parcels for next trip  |
+------------------------------------------------------------------------------+
                                       │
                                       ▼
+------------------------------------------------------------------------------+
| PHASE 3A: SHORTEST PATH CALCULATION (Dijkstra's Algorithm)                   |
| • Computes minimum distance & exact road path between Depot and Destinations |
| • Priority Queue (Min-Heap) implementation: O((V + E) log V)                 |
| • Generates All-Pairs Metric Distance Matrix for active stops                |
+------------------------------------------------------------------------------+
                                       │
                                       ▼
+------------------------------------------------------------------------------+
| PHASE 3B: ROUTE SEQUENCING (Nearest-Neighbor TSP Approximation)              |
| • Starting from Hub, greedily visit nearest unvisited customer destination    |
| • Returns to Hub to complete closed courier cycle                            |
| • Calculates total trip distance & full turn-by-turn navigation waypoints    |
+------------------------------------------------------------------------------+
                                       │
                                       ▼
+------------------------------------------------------------------------------+
| PHASE 4 & 5: BENCHMARKING, EMPIRICAL RUNTIME CHARTS & FINAL DEMONSTRATION    |
| • Performance scaling on Small, Medium, Large datasets                       |
| • Runtimes plotted and analyzed against theoretical Big-O bounds             |
+------------------------------------------------------------------------------+
"""
