"""
Phase 3: Route Maker and Graph Processing
Design & Analysis of Algorithms (ETCCDA302)
K.R. Mangalam University, Gurugram

This module implements:
1. Dijkstra's Algorithm using Min-Heap (Single Source Shortest Path).
2. All-Pairs Shortest Path Matrix calculation for delivery stops.
3. Nearest-Neighbor TSP Approximation Algorithm for tour construction.
4. Turn-by-Turn waypoint path stitching and route length calculation.
5. 2-Opt Local Search route optimization (Phase 4 enhancement).
"""

import heapq
from typing import Dict, List, Tuple, Set, Optional
from .phase1_design import RoadNetworkGraph


# ==============================================================================
# 1. DIJKSTRA'S SHORTEST PATH ALGORITHM
# ==============================================================================

def dijkstra_shortest_path(
    graph: RoadNetworkGraph,
    start_node: str
) -> Tuple[Dict[str, float], Dict[str, Optional[str]]]:
    """
    Computes shortest paths from start_node to all reachable nodes in the graph
    using Dijkstra's algorithm with a Min-Heap (priority queue).

    Complexity:
        - Time: O((V + E) * log V)
        - Space: O(V) for distance table and parent pointers.

    Parameters:
        graph: The RoadNetworkGraph instance.
        start_node: Origin vertex (e.g. 'Hub').

    Returns:
        distances: dict mapping node -> minimum distance from start_node.
        parents: dict mapping node -> predecessor node on the shortest path.
    """
    distances: Dict[str, float] = {node: float("inf") for node in graph.get_nodes()}
    parents: Dict[str, Optional[str]] = {node: None for node in graph.get_nodes()}

    if start_node not in distances:
        distances[start_node] = 0.0
        parents[start_node] = None

    distances[start_node] = 0.0

    # Priority queue stores tuples of (current_shortest_distance, node_id)
    pq: List[Tuple[float, str]] = [(0.0, start_node)]

    visited: Set[str] = set()

    while pq:
        curr_dist, u = heapq.heappop(pq)

        if u in visited:
            continue
        visited.add(u)

        for v, weight in graph.get_neighbors(u):
            new_dist = curr_dist + weight
            if new_dist < distances.get(v, float("inf")):
                distances[v] = round(new_dist, 4)
                parents[v] = u
                heapq.heappush(pq, (distances[v], v))

    return distances, parents


def reconstruct_path(parents: Dict[str, Optional[str]], start: str, end: str) -> List[str]:
    """Reconstructs the full node path from start to end using parent pointers."""
    if start == end:
        return [start]
    if parents.get(end) is None:
        return []

    path = []
    curr: Optional[str] = end
    while curr is not None:
        path.append(curr)
        if curr == start:
            break
        curr = parents.get(curr)

    if path and path[-1] == start:
        path.reverse()
        return path
    return []


# ==============================================================================
# 2. METRIC DISTANCE MATRIX COMPUTATION
# ==============================================================================

def compute_metric_distance_matrix(
    graph: RoadNetworkGraph,
    stops: List[str]
) -> Tuple[Dict[str, Dict[str, float]], Dict[str, Dict[str, List[str]]]]:
    """
    Computes all-pairs shortest paths between the specified subset of delivery stops
    using Dijkstra's algorithm.

    Returns:
        dist_matrix: dist_matrix[u][v] = shortest distance between u and v.
        path_matrix: path_matrix[u][v] = exact road nodes traversed from u to v.
    """
    unique_stops = list(dict.fromkeys(stops))
    dist_matrix: Dict[str, Dict[str, float]] = {}
    path_matrix: Dict[str, Dict[str, List[str]]] = {}

    for u in unique_stops:
        dist_matrix[u] = {}
        path_matrix[u] = {}
        distances, parents = dijkstra_shortest_path(graph, u)

        for v in unique_stops:
            dist_matrix[u][v] = distances.get(v, float("inf"))
            path_matrix[u][v] = reconstruct_path(parents, u, v)

    return dist_matrix, path_matrix


# ==============================================================================
# 3. NEAREST-NEIGHBOR TSP APPROXIMATION ALGORITHM
# ==============================================================================

def nearest_neighbor_tsp(
    start_node: str,
    delivery_stops: List[str],
    dist_matrix: Dict[str, Dict[str, float]]
) -> Tuple[List[str], float]:
    """
    Greedy Nearest-Neighbor TSP Approximation.
    Constructs a closed delivery route starting at start_node (Hub),
    visiting every unique delivery stop exactly once, and returning to start_node.

    Approximation Bound:
        Metric TSP NN ratio is bounded by 0.5 * (ceil(log2(N)) + 1) in general metric graphs.
        Extremely fast O(K^2) execution where K is number of delivery stops.

    Parameters:
        start_node: Central Depot / Hub.
        delivery_stops: List of customer destination nodes.
        dist_matrix: Precomputed pairwise shortest distances.

    Returns:
        ordered_route: Ordered sequence of stops, e.g. ['Hub', 'Sec14', 'Sec29', 'Hub'].
        total_distance: Total travel distance in kilometers.
    """
    # Remove duplicates and exclude hub from unvisited set
    unvisited = set(delivery_stops)
    if start_node in unvisited:
        unvisited.remove(start_node)

    if not unvisited:
        return [start_node, start_node], 0.0

    route = [start_node]
    current = start_node
    total_dist = 0.0

    while unvisited:
        # Pick the unvisited node with minimum distance from current
        next_node = min(unvisited, key=lambda node: dist_matrix[current].get(node, float("inf")))
        step_dist = dist_matrix[current].get(next_node, float("inf"))

        if step_dist == float("inf"):
            # Graph disconnected fallback
            next_node = next(iter(unvisited))
            step_dist = 0.0

        total_dist += step_dist
        route.append(next_node)
        unvisited.remove(next_node)
        current = next_node

    # Return to Central Hub
    return_dist = dist_matrix[current].get(start_node, float("inf"))
    if return_dist != float("inf"):
        total_dist += return_dist
    route.append(start_node)

    return route, round(total_dist, 2)


# ==============================================================================
# 4. TURN-BY-TURN PATH STITCHING
# ==============================================================================

def build_turn_by_turn_itinerary(
    route: List[str],
    path_matrix: Dict[str, Dict[str, List[str]]]
) -> List[str]:
    """
    Stitches individual Dijkstra shortest paths between consecutive route stops
    into an unbroken turn-by-turn road navigation path.
    """
    if len(route) <= 1:
        return route

    full_itinerary: List[str] = []
    for i in range(len(route) - 1):
        u, v = route[i], route[i + 1]
        leg = path_matrix.get(u, {}).get(v, [u, v])
        if not full_itinerary:
            full_itinerary.extend(leg)
        else:
            # Avoid repeating the joint node
            full_itinerary.extend(leg[1:])

    return full_itinerary


# ==============================================================================
# 5. OPTIMIZATION: 2-OPT LOCAL SEARCH REFINEMENT
# ==============================================================================

def two_opt_optimize(
    route: List[str],
    dist_matrix: Dict[str, Dict[str, float]],
    max_iterations: int = 100
) -> Tuple[List[str], float]:
    """
    2-Opt heuristic local search to remove self-intersections from the TSP route.
    Demonstrates route optimization beyond basic Nearest-Neighbor (Phase 4 requirement).
    """
    def calculate_total_length(r: List[str]) -> float:
        d = 0.0
        for i in range(len(r) - 1):
            d += dist_matrix[r[i]][r[i + 1]]
        return d

    best_route = list(route)
    best_dist = calculate_total_length(best_route)
    improved = True
    iterations = 0

    while improved and iterations < max_iterations:
        improved = False
        iterations += 1

        # We keep depot at index 0 and index -1 fixed
        for i in range(1, len(best_route) - 2):
            for j in range(i + 1, len(best_route) - 1):
                # Reverse sub-sequence between i and j
                new_route = best_route[:i] + best_route[i:j + 1][::-1] + best_route[j + 1:]
                new_dist = calculate_total_length(new_route)

                if new_dist < best_dist - 1e-4:
                    best_route = new_route
                    best_dist = new_dist
                    improved = True
                    break
            if improved:
                break

    return best_route, round(best_dist, 2)
