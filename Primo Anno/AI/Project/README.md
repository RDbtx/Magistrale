# THE ELDER WALKER

**The Elder Walker** is my **final project** for the *Artificial Intelligence* course.  
It implements and compares several **map search algorithms** over the world map of **Skyrim**, allowing pathfinding between 139 locations.

## Project Overview

This project explores and visualizes **graph-based search algorithms** in a fantasy setting.  
Each city or landmark in Skyrim is represented as a **node**, and paths between
them are represented as **edges** with traversal costs.  

The system allows users to:
- Select a **start** and **destination** city.
- Compute and visualize the **optimal path**.
- Compare the **performance** of multiple search strategies based on node expansions and path lengths.

## Implemented Algorithms

The project implements and analyzes four classical search algorithms:

| Algorithm | Description |
|------------|-------------|
| **A\*** | Uses both actual cost and heuristic estimates to find the optimal path efficiently. |
| **Dijkstra** | Finds the shortest path by exploring all nodes with increasing cumulative cost. |
| **Breadth-First Search (BFS)** | Explores all nodes at the current depth before moving deeper. Guarantees optimal paths only for unweighted graphs. |
| **Depth-First Search (DFS)** | Explores as far as possible along each branch before backtracking. Not guaranteed to find the optimal path. |


##  How It Works

1. The map of Skyrim is loaded as a **graph** structure (nodes = cities, edges = paths).  
2. The user selects a start and goal location.  
3. The user choose one of the algorithms to find a path.  
4. The system measures:
   - Path length (depth)
   - Number of expanded nodes
   - Processing time
   - Path Cost
5. The data is then visualized using **matplotlib**.
