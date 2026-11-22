# Mini-Courier Planner
**Course:** Design & Analysis of Algorithms (ETCCDA302)  
**Assessment:** Capstone Assignment  
**Language:** Python 3

## Problem
The application simulates a courier company. It prioritizes parcels, chooses a high-value set that fits the vehicle capacity, computes shortest road paths, and produces an approximate delivery tour.

## Algorithms used
1. **Merge Sort** — sorts parcels by descending priority and then ascending deadline. Time `O(n log n)`, auxiliary space `O(n)`.
2. **0/1 Knapsack (Dynamic Programming)** — selects parcels maximizing total value under a vehicle weight capacity. Time and space `O(nW)`.
3. **Dijkstra's Algorithm** — finds shortest paths in a weighted road graph using a min-heap. Time `O((V+E) log V)`.
4. **Nearest Neighbor TSP approximation** — repeatedly visits the nearest unvisited delivery point and returns to the depot. Time `O(k^2)`. This is a heuristic, not a guaranteed optimal TSP solution.

## Project structure
- `main.py` — complete application and algorithms
- `data/parcels.csv` — sample parcel dataset
- `results/sample_output.txt` — sample execution output
- `results/runtime_chart.png` — runtime comparison chart
- `report.docx` — formatted assignment report
- `performance_test.py` — reproducible performance experiment

## Requirements
- Python 3.8 or later
- No third-party packages are needed to run `main.py`.

## Run
Open a terminal in this folder and execute:
```bash
python main.py
```
For runtime experiments:
```bash
python performance_test.py
```

## Input format
CSV columns: `id,destination,weight,value,priority,deadline`.
- `weight`: parcel weight units
- `value`: parcel value score
- `priority`: larger number means higher priority
- `deadline`: smaller number means an earlier deadline
- `destination`: graph node (`A`, `B`, `C`, `D`, or `E`)

## Sample configuration
Vehicle capacity is 12 weight units. The road graph is defined in `build_graph()` in `main.py`; edge weights represent distance in km.

## Limitations and future improvements
- The road network and parcel dataset are illustrative, not live maps or GPS data.
- Nearest Neighbor is an approximation and can produce a longer route than the optimal TSP route.
- Future work: real map integration, time windows, multiple vehicles, traffic-aware weights, and a space-optimized 1D knapsack DP implementation.

## Viva preparation
- Why Merge Sort? It provides predictable `O(n log n)` performance.
- Why Knapsack DP? It considers combinations of parcels rather than choosing only by a local greedy rule.
- Why Dijkstra? All road edge weights are non-negative.
- Is Nearest Neighbor always optimal? No; it is a fast heuristic for TSP.
- What does W mean in `O(nW)`? The vehicle's integer capacity.
