"""
Mini-Courier Planner
Design & Analysis of Algorithms (ETCCDA302)
Algorithms: Merge Sort, 0/1 Knapsack (Dynamic Programming),
Dijkstra's Shortest Path, and Nearest Neighbor TSP Approximation.
"""

import csv
import heapq
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "parcels.csv"

# -------------------- Data Loading --------------------

def load_parcels(filename=DATA_FILE):
    """Load parcel records from a CSV file."""
    parcels = []
    with open(filename, newline="", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            parcels.append({
                "id": row["id"],
                "destination": row["destination"],
                "weight": int(row["weight"]),
                "value": int(row["value"]),
                "priority": int(row["priority"]),
                "deadline": int(row["deadline"])
            })
    return parcels


# -------------------- Phase 2: Sorting --------------------

def merge_sort(parcels):
    """
    Sort parcels by higher priority first; for equal priority,
    earlier deadline comes first. Returns a new sorted list.
    Time: O(n log n), Auxiliary space: O(n).
    """
    if len(parcels) <= 1:
        return parcels[:]

    mid = len(parcels) // 2
    left = merge_sort(parcels[:mid])
    right = merge_sort(parcels[mid:])
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        left_key = (-left[i]["priority"], left[i]["deadline"])
        right_key = (-right[j]["priority"], right[j]["deadline"])
        if left_key <= right_key:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result


# -------------------- Phase 2: Dynamic Programming --------------------

def knapsack(parcels, capacity):
    """
    0/1 Knapsack DP. Selects parcels with maximum total value
    without exceeding the vehicle capacity.
    Time: O(n * capacity), Space: O(n * capacity).
    """
    n = len(parcels)
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        weight = parcels[i - 1]["weight"]
        value = parcels[i - 1]["value"]
        for current_capacity in range(capacity + 1):
            dp[i][current_capacity] = dp[i - 1][current_capacity]
            if weight <= current_capacity:
                candidate = value + dp[i - 1][current_capacity - weight]
                if candidate > dp[i][current_capacity]:
                    dp[i][current_capacity] = candidate

    selected = []
    remaining = capacity
    for i in range(n, 0, -1):
        if dp[i][remaining] != dp[i - 1][remaining]:
            parcel = parcels[i - 1]
            selected.append(parcel)
            remaining -= parcel["weight"]

    selected.reverse()
    return selected, dp[n][capacity], dp


# -------------------- Phase 3: Graph + Dijkstra --------------------

def build_graph():
    """Create an undirected weighted road network."""
    graph = {
        "Depot": {"A": 4, "B": 2},
        "A": {"Depot": 4, "B": 1, "C": 5, "D": 10},
        "B": {"Depot": 2, "A": 1, "C": 8, "D": 7, "E": 6},
        "C": {"A": 5, "B": 8, "D": 2, "E": 3},
        "D": {"A": 10, "B": 7, "C": 2, "E": 4},
        "E": {"B": 6, "C": 3, "D": 4}
    }
    return graph


def dijkstra(graph, start):
    """
    Find shortest distances and predecessor links from start.
    Uses a min-heap priority queue.
    Time: O((V + E) log V), Space: O(V).
    """
    distances = {node: float("inf") for node in graph}
    previous = {node: None for node in graph}
    distances[start] = 0
    queue = [(0, start)]

    while queue:
        current_distance, node = heapq.heappop(queue)
        if current_distance != distances[node]:
            continue

        for neighbor, weight in graph[node].items():
            new_distance = current_distance + weight
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous[neighbor] = node
                heapq.heappush(queue, (new_distance, neighbor))

    return distances, previous


def reconstruct_path(previous, start, destination):
    """Reconstruct a shortest path using Dijkstra predecessors."""
    path = []
    current = destination
    while current is not None:
        path.append(current)
        current = previous[current]
    path.reverse()
    if not path or path[0] != start:
        return []
    return path


def all_pairs_shortest_paths(graph):
    """Run Dijkstra from every graph node."""
    distances = {}
    paths = {}
    for source in graph:
        dist, previous = dijkstra(graph, source)
        distances[source] = dist
        paths[source] = {
            target: reconstruct_path(previous, source, target)
            for target in graph
        }
    return distances, paths


# -------------------- Phase 3: TSP Approximation --------------------

def nearest_neighbor_tsp(destinations, distances, start="Depot"):
    """
    Approximate a delivery tour by repeatedly visiting the nearest
    unvisited destination, then return to the depot.
    This is a heuristic and does not guarantee the optimal TSP tour.
    """
    remaining = set(destinations)
    route = [start]
    current = start
    total_distance = 0

    while remaining:
        next_node = min(remaining, key=lambda node: distances[current][node])
        total_distance += distances[current][next_node]
        route.append(next_node)
        remaining.remove(next_node)
        current = next_node

    if current != start:
        total_distance += distances[current][start]
        route.append(start)

    return route, total_distance


# -------------------- Complete Application --------------------

def run_planner():
    parcels = load_parcels()
    print("\n========== MINI-COURIER PLANNER ==========")
    print(f"Total parcels received: {len(parcels)}")

    sorted_parcels = merge_sort(parcels)
    print("\n1. PARCEL PRIORITIZATION (Merge Sort)")
    for parcel in sorted_parcels:
        print(f'{parcel["id"]}: priority={parcel["priority"]}, '
              f'deadline={parcel["deadline"]}, destination={parcel["destination"]}')

    capacity = 12
    selected, total_value, dp = knapsack(sorted_parcels, capacity)
    print(f"\n2. OPTIMAL PACKING (0/1 Knapsack, capacity={capacity})")
    for parcel in selected:
        print(f'{parcel["id"]}: weight={parcel["weight"]}, value={parcel["value"]}')
    print(f"Total selected weight: {sum(p['weight'] for p in selected)}")
    print(f"Maximum parcel value: {total_value}")

    graph = build_graph()
    distances, paths = all_pairs_shortest_paths(graph)
    print("\n3. SHORTEST PATHS (Dijkstra)")
    for destination in sorted({p["destination"] for p in selected}):
        print(f"Depot -> {destination}: {distances['Depot'][destination]} km "
              f"| Path: {' -> '.join(paths['Depot'][destination])}")

    destinations = sorted({p["destination"] for p in selected})
    if destinations:
        route, route_length = nearest_neighbor_tsp(
            destinations, distances, start="Depot"
        )
        print("\n4. DELIVERY TOUR (Nearest Neighbor TSP Approximation)")
        print(" -> ".join(route))
        print(f"Total tour distance (including return to depot): {route_length} km")
    else:
        print("\nNo parcels fit in the selected vehicle capacity.")

    print("\n5. ALGORITHM COMPLEXITIES")
    print("Merge Sort: O(n log n) time, O(n) auxiliary space")
    print("0/1 Knapsack: O(nW) time and O(nW) space")
    print("Dijkstra (heap): O((V+E) log V) time, O(V) extra space")
    print("Nearest Neighbor TSP: O(k^2) time, O(k) extra space")
    print("\n==========================================")

if __name__ == "__main__":
    run_planner()
