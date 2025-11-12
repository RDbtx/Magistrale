import json
import math

import matplotlib.pyplot as plt


class Location:
    """
    Class representing a location of the map
    """

    def __init__(self, name: str, x: float, y: float):
        self.name = name
        self.x = x
        self.y = y

    def coords(self):
        return (self.x, self.y)


class Graph:
    """
    Class representing the whole map
    """

    def __init__(self) -> None:
        self.nodes = {}
        self.adjacent = {}

    def add_location(self, name: str, x: float, y: float):
        """
        Adds a location to the map. It is used when creating the map
        from the json file to load the data in memory.

        Inputs:
        - name: the name of the location
        - x: the x coordinate of the location
        - y: the y coordinate of the location

        Outputs:
        - loc: A Location object that represents the location
        """

        if name in self.nodes:
            return self.nodes[name]
        loc = Location(name, x, y)
        self.nodes[name] = loc
        self.adjacent[loc] = {}
        return loc

    def connect(self, a: str, b: str, distance: float):
        """
        Creates the connection between two locations.

        Inputs:
        - a: the first location
        - b: the second location
        - distance: the cost of the path between the two locations

        """
        a_loc = self.nodes[a]
        b_loc = self.nodes[b]
        self.adjacent[a_loc][b_loc] = float(distance)

    def neighbors(self, node: Location):
        """
        Returns a list of all the neighboring locations from the current node.

        Inputs:
        - node: the current node

        Outputs:
        - neighbors: A list of all neighboring locations

        """
        return self.adjacent.get(node, {})

    def locations(self):
        """
        Returns a dictionary containig all the addresses of each location object.
        contained inside the graph
        """
        return self.nodes.values()

    def get(self, name: str):
        """
        Returns the location object corresponding to the given name.

        Input:
        - name: the name of the location

        Output:
        - loc: The location object corresponding to the given name
        """
        return self.nodes[name]

    def get_names(self):
        """
        Returns a sorted list of all the locations of the map.

        Output:
        - names: a sorted list of all locations of the map
        """
        cities = []
        for elem in self.nodes.keys():
            cities.append(elem)

        for elem in sorted(cities):
            print(elem)
        return sorted(cities)


def reconstruct_path(came_from: dict, start: Location, goal: Location):
    """
    Reconstructs the path from the start node to the goal node after a search algorithm is
    called.

    Inputs:
    - came_from: A dictionary mapping each node to the node it was reached from
    - start: the starting node
    - goal: the goal node

    Output:
    - path: A list of all the nodes encountered from the starting location to the destination
    """
    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path


def load_graph_from_json(path: str) -> Graph:
    """
    Creates a graph  object from the data contained in the json file.

    -Input:
    - path: the path to the json file

    Output:
    - g: the graph object that represents the whole map
    """
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    g = Graph()


    for name, info in data.items():
        g.add_location(name, info["x"], info["y"])


    for name, info in data.items():
        for nbr, dist in info["neighbors"].items():
            g.connect(name, nbr, dist)

    return g


def plot_graph(g: Graph):
    """
    Plots the given graph trough matplotlib.

    -Input:
    - g: the graph object

    """
    pos = {n: (n.x, n.y) for n in g.locations()}

    fig, ax = plt.subplots(figsize=(20, 20))
    ax.set_title("Skyrim", fontweight="bold", fontsize="20")
    ax.set_aspect('equal', adjustable='box')
    ax.set_xticks([])
    ax.set_yticks([])


    for u in g.locations():
        for v, w in g.neighbors(u).items():
            if u.name < v.name:
                x1, y1 = pos[u]
                x2, y2 = pos[v]
                ax.plot([x1, x2], [y1, y2], 'gray', linewidth=1)
                mx, my = (x1 + x2) / 2, (y1 + y2) / 2
                ax.text(mx, my, f"{w:.1f}", fontsize=8, color='gray')

    xs = [n.x for n in g.locations()]
    ys = [n.y for n in g.locations()]
    ax.scatter(xs, ys, s=60, color='blue', zorder=3)

    for n in g.locations():
        ax.text(n.x, n.y + 15, n.name, fontsize=9, ha='center', va='bottom', fontweight='bold')

    plt.tight_layout()
    plt.show()


def load_graph_and_plot(json_path: str):
    """
    Loads a graph and plots it using matplotlib

    Input:
    - json_path: the path to the json file

    Output:
    - g: the Graph object
    """
    g = load_graph_from_json(json_path)
    plot_graph(g)
    return g


def mean(data: list) -> float:
    """
    Calculates the mean value of a list of numbers.

    Input:
    - data: a list of numbers

    Output:
    - mean: the mean of the list of numbers

    """

    return sum(data) / len(data)


def standard_deviation(data: list):
    """
    Computes the standard deviation of a list of numbers.

    Input:
    - data: a list of numbers

    Output:
    - std: the standard deviation of the list of numbers
    """
    deviations = []
    for d in data:
        deviations.append(pow(d - mean(data), 2))
    deviation_sum = sum(deviations)
    variance = deviation_sum / len(data)
    standard_deviation = math.sqrt(variance)
    return standard_deviation


def plot_path(path: list, algorithm_name: str, start: Location, goal: Location):
    """
    This functions plots the given path to create a visual representation of the algorithm output.

    Inputs:
    - path: the path to the path
    - algorithm_name: the name of the algorithm
    - start: the starting location
    - goal: the goal location

    """
    x_coords, y_coords = [], []
    for loc in path:
        x_coord, y_coord = loc.coords()
        x_coords.append(x_coord)
        y_coords.append(y_coord)
        names = [loc.name for loc in path]

    plt.figure(figsize=(10, 10))
    plt.scatter(x_coords, y_coords, marker='o', color='blue', zorder=3)
    plt.setp(plt.xticks([]), visible=False)
    plt.setp(plt.yticks([]), visible=False)
    plt.plot(x_coords, y_coords, marker='o', linestyle='-', color='gray', linewidth=2)

    for i, name in enumerate(names):
        plt.text(x_coords[i] + 5, y_coords[i] + 10, name, fontsize=9, fontweight='bold')

    plt.title(f"{algorithm_name} Generated Path [{start.name} -> {goal.name}]", fontweight='bold')
    plt.grid(False)

    plt.show()
