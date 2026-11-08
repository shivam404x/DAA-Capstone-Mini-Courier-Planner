"""
Phase 2: Package Prioritization and Box Filling
Design & Analysis of Algorithms (ETCCDA302)
K.R. Mangalam University, Gurugram

This module implements:
1. Merge Sort (Primary Algorithm - Stable O(N log N)).
2. Quick Sort (Comparison Algorithm - In-place O(N log N) average).
3. 0/1 Knapsack Dynamic Programming (Full 2D table with Backtracking).
4. Space-Optimized 1D Knapsack DP (Optimization analysis).
"""

from typing import List, Tuple, Dict, Any
from copy import deepcopy
from .models import Parcel


# ==============================================================================
# 1. PARCEL SORTING ALGORITHMS
# ==============================================================================

def parcel_sort_key(parcel: Parcel) -> Tuple[float, int]:
    """
    Comparison tuple for prioritization:
    - Primary: Delivery deadline ascending (earliest delivery deadline first).
    - Secondary: Priority descending (negative priority so higher priority comes first).
    """
    return (parcel.deadline_hours, -parcel.priority)


def merge_sort_parcels(parcels: List[Parcel]) -> List[Parcel]:
    """
    Sorts parcels using Merge Sort (Divide and Conquer).
    - Worst-case time complexity: O(N log N)
    - Space complexity: O(N)
    - Stability: Stable (preserves order of elements with equal keys).
    """
    if len(parcels) <= 1:
        return list(parcels)

    mid = len(parcels) // 2
    left = merge_sort_parcels(parcels[:mid])
    right = merge_sort_parcels(parcels[mid:])

    return _merge(left, right)


def _merge(left: List[Parcel], right: List[Parcel]) -> List[Parcel]:
    """Merge helper for Merge Sort."""
    merged: List[Parcel] = []
    i = j = 0

    while i < len(left) and j < len(right):
        if parcel_sort_key(left[i]) <= parcel_sort_key(right[j]):
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


def quick_sort_parcels(parcels: List[Parcel]) -> List[Parcel]:
    """
    Sorts parcels using Quick Sort with Median-of-Three pivot selection.
    - Average time complexity: O(N log N)
    - Worst-case time complexity: O(N^2) (rare with median-of-three)
    - Space complexity: O(log N) auxiliary call stack
    - Stability: Not inherently stable
    """
    items = list(parcels)
    _quick_sort_helper(items, 0, len(items) - 1)
    return items


def _quick_sort_helper(items: List[Parcel], low: int, high: int) -> None:
    if low < high:
        pivot_idx = _partition(items, low, high)
        _quick_sort_helper(items, low, pivot_idx - 1)
        _quick_sort_helper(items, pivot_idx + 1, high)


def _partition(items: List[Parcel], low: int, high: int) -> int:
    # Median-of-three pivot selection to prevent worst-case on presorted data
    mid = (low + high) // 2
    candidates = [(parcel_sort_key(items[i]), i) for i in (low, mid, high)]
    candidates.sort(key=lambda x: x[0])
    median_idx = candidates[1][1]
    items[median_idx], items[high] = items[high], items[median_idx]

    pivot_key = parcel_sort_key(items[high])
    i = low - 1
    for j in range(low, high):
        if parcel_sort_key(items[j]) <= pivot_key:
            i += 1
            items[i], items[j] = items[j], items[i]

    items[i + 1], items[high] = items[high], items[i + 1]
    return i + 1


# ==============================================================================
# 2. DYNAMIC PROGRAMMING: 0/1 KNAPSACK FOR VEHICLE PACKING
# ==============================================================================

def knapsack_01_dp(
    parcels: List[Parcel],
    capacity: int
) -> Tuple[List[Parcel], List[Parcel], List[List[int]], int]:
    """
    Solves the 0/1 Knapsack Problem using Dynamic Programming.

    Parameters:
        parcels: List of candidate parcels sorted by priority/deadline.
        capacity: Maximum weight capacity of the delivery vehicle/box (W).

    Returns:
        Tuple containing:
        - selected_parcels: Optimal subset of parcels to load.
        - deferred_parcels: Parcels left for subsequent delivery trips.
        - dp_table: Complete (N+1) x (W+1) dynamic programming matrix.
        - max_value: Maximum total priority value achieved.

    Complexity:
        - Time: O(N * W) where N is number of parcels, W is vehicle capacity.
        - Space: O(N * W) for explicit table reconstruction.
    """
    N = len(parcels)
    W = capacity

    # Step 1: Initialize DP table with zeros
    # dp[i][w] = Maximum utility using a subset of the first i parcels within weight w
    dp_table: List[List[int]] = [[0] * (W + 1) for _ in range(N + 1)]

    # Step 2: Fill the DP table
    for i in range(1, N + 1):
        item = parcels[i - 1]
        w_i = item.weight
        v_i = item.value

        for w in range(W + 1):
            if w_i <= w:
                # Option A: Do not include item i -> dp_table[i-1][w]
                # Option B: Include item i -> dp_table[i-1][w - w_i] + v_i
                dp_table[i][w] = max(
                    dp_table[i - 1][w],
                    dp_table[i - 1][w - w_i] + v_i
                )
            else:
                # Parcel is heavier than current capacity limit w
                dp_table[i][w] = dp_table[i - 1][w]

    max_value = dp_table[N][W]

    # Step 3: Backtrack to reconstruct the optimal parcel set
    selected: List[Parcel] = []
    remaining_w = W
    for i in range(N, 0, -1):
        # If value differs from the cell above, item i was selected
        if dp_table[i][remaining_w] != dp_table[i - 1][remaining_w]:
            item = parcels[i - 1]
            selected.append(item)
            remaining_w -= item.weight

    # Reverse to restore original prioritization sequence
    selected.reverse()

    selected_ids = {p.id for p in selected}
    deferred = [p for p in parcels if p.id not in selected_ids]

    return selected, deferred, dp_table, max_value


def knapsack_space_optimized_1d(parcels: List[Parcel], capacity: int) -> Tuple[int, List[int]]:
    """
    Space-Optimized 1D Dynamic Programming implementation.
    Reduces memory from O(N * W) to O(W).
    Demonstrated for Phase 4 optimization analysis.
    """
    dp = [0] * (capacity + 1)
    for p in parcels:
        w_i = p.weight
        v_i = p.value
        # Iterate backwards to avoid using the same item multiple times in 0/1 knapsack
        for w in range(capacity, w_i - 1, -1):
            dp[w] = max(dp[w], dp[w - w_i] + v_i)
    return dp[capacity], dp


def format_dp_table(dp_table: List[List[int]], parcels: List[Parcel], max_cols: int = 15) -> str:
    """
    Formats the 2D DP table as a clean text grid for reports and terminal evidence.
    Truncates width gracefully if capacity W is large.
    """
    N = len(parcels)
    W = len(dp_table[0]) - 1
    display_w = min(W, max_cols)

    header = f"{'Item / W':<16} | " + " | ".join(f"{w:>4}" for w in range(display_w + 1))
    separator = "-" * len(header)
    lines = [separator, header, separator]

    # Row 0: Base case (0 items)
    row0 = f"{'Base (0 items)':<16} | " + " | ".join(f"{dp_table[0][w]:>4}" for w in range(display_w + 1))
    lines.append(row0)

    for i in range(1, N + 1):
        p = parcels[i - 1]
        label = f"{p.id} (w={p.weight},v={p.value})"[:16]
        row_str = f"{label:<16} | " + " | ".join(f"{dp_table[i][w]:>4}" for w in range(display_w + 1))
        lines.append(row_str)

    lines.append(separator)
    if display_w < W:
        lines.append(f"... (Table truncated for display: showing weights 0 to {display_w} of {W} kg total)")
    return "\n".join(lines)
