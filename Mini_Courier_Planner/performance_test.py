"""Reproducible runtime experiment for Mini-Courier Planner."""
import random
import time
import csv
from pathlib import Path
from main import merge_sort, knapsack, build_graph, dijkstra

random.seed(42)
BASE = Path(__file__).resolve().parent

def make_parcels(n):
    nodes = ["A", "B", "C", "D", "E"]
    return [{
        "id": f"P{i}", "destination": random.choice(nodes),
        "weight": random.randint(1, 10), "value": random.randint(10, 100),
        "priority": random.randint(1, 5), "deadline": random.randint(1, 10)
    } for i in range(n)]

def measure(function, repeats=5):
    samples = []
    for _ in range(repeats):
        start = time.perf_counter()
        function()
        samples.append(time.perf_counter() - start)
    return sum(samples) / len(samples)

sizes = [10, 25, 50, 100, 200]
rows = []
graph = build_graph()
for n in sizes:
    parcels = make_parcels(n)
    sort_time = measure(lambda: merge_sort(parcels))
    knapsack_time = measure(lambda: knapsack(parcels, 50))
    dijkstra_time = measure(lambda: dijkstra(graph, "Depot"))
    rows.append([n, sort_time, knapsack_time, dijkstra_time])

with open(BASE / "results" / "runtime_results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["input_size", "merge_sort_seconds", "knapsack_seconds", "dijkstra_seconds"])
    writer.writerows(rows)

print("Average runtime over 5 repetitions (seconds)")
print("n, Merge Sort, Knapsack, Dijkstra")
for row in rows:
    print(row[0], *(f"{v:.8f}" for v in row[1:]))
print("Saved results/runtime_results.csv")
