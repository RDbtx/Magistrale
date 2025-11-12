import heapq
from collections import deque
from itertools import count
from src.utils import *
import time
import tracemalloc

COST_PER_PIXEL = 10  # scaled cost per pixel distance


def bfs(graph: Graph, start: Location, goal: Location):
    """
    A breath first search algorithm. Uses double ended queque (deque) list
    to implement a FIFO logic inside the algorithm

    Inputs:
    - graph: the graph to search
    - start: the starting location of the search
    - goal: the destination of the search

    Outputs:
    - path: the path from start to goal
    - number of jumps: the number of jumps from start to goal
    - explored nodes: the number of explored nodes
    """
    process_time = time.time()
    queue = deque([start])
    visited = {start}
    came_from = {}
    nodes_expanded = 0
    mem_alloc = []
    nodes_allocated = []
    tracemalloc.start()

    while queue:
        node = queue.popleft()
        nodes_expanded += 1
        nodes_allocated.append(len(queue))
        max_nodes_allocated = max(nodes_allocated)

        if node == goal:
            path = reconstruct_path(came_from, start, goal)
            process_time = time.time() - process_time
            if mem_alloc:
                mean_alloc = sum(mem_alloc) / len(mem_alloc)
                max_alloc = max(mem_alloc)
            else:
                max_alloc, mean_alloc = 0, 0
            tracemalloc.stop()
            return path, len(path) - 1, nodes_expanded, process_time, mean_alloc, max_alloc, max_nodes_allocated

        for nbr in graph.neighbors(node):
            if nbr not in visited:
                visited.add(nbr)
                came_from[nbr] = node
                queue.append(nbr)

        mem_alloc.append(tracemalloc.get_traced_memory()[0])

    process_time = time.time() - process_time
    if mem_alloc:
        mean_alloc = sum(mem_alloc) / len(mem_alloc)
        max_alloc = max(mem_alloc)
    else:
        max_alloc, mean_alloc = 0, 0
    tracemalloc.stop()
    return [], 0, nodes_expanded, process_time, mean_alloc, max_alloc, max_nodes_allocated


def dfs(graph, start, goal):
    """
    Depth-First Search with dead-end removal.

    Inputs:
    - graph: adjacency-based graph object with .neighbors(node)
    - start: starting node
    - goal: target node

    Outputs:
    - path: the path from start to goal (list)
    - number of jumps: len(path)-1
    - explored nodes: count of expanded nodes
    - process_time: total time in seconds
    - mean_alloc / max_alloc: memory stats from tracemalloc
    - max_nodes_allocated: peak stack size
    """

    process_time = time.time()
    tracemalloc.start()

    stack = [start]
    visited = {start}
    came_from = {start: None}
    dead_ends = set()
    mem_alloc = []
    nodes_allocated = []
    nodes_expanded = 0

    while stack:
        node = stack[-1]
        nodes_expanded += 1
        nodes_allocated.append(len(stack))
        max_nodes_allocated = max(nodes_allocated)

        if node == goal:
            process_time = time.time() - process_time
            mem_alloc.append(tracemalloc.get_traced_memory()[0])
            tracemalloc.stop()

            path = reconstruct_path(came_from, start, goal)
            if mem_alloc:
                mean_alloc = sum(mem_alloc) / len(mem_alloc)
                max_alloc = max(mem_alloc)
            else:
                max_alloc, mean_alloc = 0, 0
            return path, len(path) - 1, nodes_expanded, process_time, mean_alloc, max_alloc, max_nodes_allocated

        found_next = False
        for nbr in graph.neighbors(node):
            if nbr not in visited and nbr not in dead_ends:
                visited.add(nbr)
                came_from[nbr] = node
                stack.append(nbr)
                found_next = True
                break

        if not found_next:
            dead_ends.add(node)
            stack.pop()

        mem_alloc.append(tracemalloc.get_traced_memory()[0])

    process_time = time.time() - process_time
    if mem_alloc:
        mean_alloc = sum(mem_alloc) / len(mem_alloc)
        max_alloc = max(mem_alloc)
    else:
        max_alloc, mean_alloc = 0, 0
    tracemalloc.stop()

    return [], 0, nodes_expanded, process_time, mean_alloc, max_alloc,max_nodes_allocated


def dijkstra(graph: Graph, start: Location, goal: Location):
    """
    A Dijkstra search algorithm. Computes the shortest path between two nodes in a weighted graph.
    It uses the heapq library to implement a priority queue ensuring that the
    next node selected for expansion always has the smallest cost. It also uses itertools.count
    to implement tiebreakers in the heap.

    Inputs:
    - graph: the graph to search
    - start: the starting location of the search
    - goal: the destination of the search

    Outputs:
    - path: the path from start to goal
    - total cost of the journey: the cost of the journey
    - explored nodes: the number of explored nodes
    """
    process_time = time.time()
    dist = {start: 0.0}
    came_from = {}
    priorityqueue = []
    counter = count()
    heapq.heappush(priorityqueue, (0.0, next(counter), start))
    visited = set()
    mem_alloc = []
    nodes_expanded = 0
    nodes_allocated = []
    tracemalloc.start()

    while priorityqueue:
        cost, _, node = heapq.heappop(priorityqueue)
        if node in visited:
            continue
        visited.add(node)
        nodes_expanded += 1
        nodes_allocated.append(len(priorityqueue))
        max_nodes_allocated = max(nodes_allocated)

        if node == goal:
            process_time = time.time() - process_time
            if mem_alloc:
                mean_alloc = sum(mem_alloc) / len(mem_alloc)
                max_alloc = max(mem_alloc)
            else:
                max_alloc, mean_alloc = 0, 0
            tracemalloc.stop()
            return reconstruct_path(came_from, start,
                                    goal), cost, nodes_expanded, process_time, mean_alloc, max_alloc, max_nodes_allocated

        for neighbor, weight in graph.neighbors(node).items():
            new_cost = cost + weight
            if new_cost < dist.get(neighbor, math.inf):
                dist[neighbor] = new_cost
                came_from[neighbor] = node
                heapq.heappush(priorityqueue, (new_cost, next(counter), neighbor))

        mem_alloc.append(tracemalloc.get_traced_memory()[0])

    process_time = time.time() - process_time
    if mem_alloc:
        mean_alloc = sum(mem_alloc) / len(mem_alloc)
        max_alloc = max(mem_alloc)
    else:
        max_alloc, mean_alloc = 0, 0
    tracemalloc.stop()
    return [], math.inf, nodes_expanded, process_time, mean_alloc, max_alloc, max_nodes_allocated


def heu_euclidean(location1: Location, location2: Location):
    """
    A Euclidean heuristic function that computes the Euclidean distance between
    two locations of the graph.

    Inputs:
    - location1: the first location
    - location2: the second location

    Output:
    - distance: the Euclidean distance
    """
    Location1_coordinates, Location2_coordinates = location1.coords(), location2.coords()
    if Location1_coordinates is None or Location2_coordinates is None:
        return 0.0
    (x1, y1), (x2, y2) = Location1_coordinates, Location2_coordinates
    euclidean_distance = math.sqrt(pow((x1 - x2), 2) + pow((y1 - y2), 2))
    return COST_PER_PIXEL * euclidean_distance


def astar(graph: Graph, start: Location, goal: Location, heuristic=None):
    """
    A A* search algorithm. Finds the optimal path by combining Dijkstra’s cost-based search with
    a heuristic estimate of the remaining distance.
    It uses the heapq library to implement a priority queue ensuring that the
    next node selected for expansion always has the smallest cost. It also uses itertools.count
    to implement tiebreakers in the heap.

    Inputs:
    - graph: the graph to search
    - start: the starting location of the search
    - goal: the destination of the search
    - heuristic: the heuristic function to use

    Outputs:
    - path: the path from start to goal
    - total cost of the journey: the cost of the journey
    - explored nodes: the number of explored nodes
    """
    if heuristic is None:
        heuristic = heu_euclidean

    process_time = time.time()
    g_score = {start: 0.0}
    came_from = {}
    priorityqueue = []
    counter = count()
    heapq.heappush(priorityqueue, (heuristic(start, goal), next(counter), start))
    closed = set()
    mem_alloc = []
    nodes_expanded = 0
    nodes_allocated = []
    tracemalloc.start()

    while priorityqueue:
        _, __, node = heapq.heappop(priorityqueue)
        if node in closed:
            continue
        closed.add(node)
        nodes_expanded += 1
        nodes_allocated.append(len(priorityqueue))
        max_nodes_allocated = max(nodes_allocated)

        if node == goal:
            process_time = time.time() - process_time
            if mem_alloc:
                mean_alloc = sum(mem_alloc) / len(mem_alloc)
                max_alloc = max(mem_alloc)
            else:
                max_alloc, mean_alloc = 0, 0
            tracemalloc.stop()
            return reconstruct_path(came_from, start, goal), g_score[
                node], nodes_expanded, process_time, mean_alloc, max_alloc, max_nodes_allocated

        for neighbor, weight in graph.neighbors(node).items():
            tentative_g = g_score[node] + weight
            if tentative_g < g_score.get(neighbor, math.inf):
                came_from[neighbor] = node
                g_score[neighbor] = tentative_g
                f = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(priorityqueue, (f, next(counter), neighbor))

        mem_alloc.append(tracemalloc.get_traced_memory()[0])

    process_time = time.time() - process_time
    if mem_alloc:
        mean_alloc = sum(mem_alloc) / len(mem_alloc)
        max_alloc = max(mem_alloc)
    else:
        max_alloc, mean_alloc = 0, 0
    tracemalloc.stop()
    return [], math.inf, nodes_expanded, process_time, mean_alloc, max_alloc, max_nodes_allocated
