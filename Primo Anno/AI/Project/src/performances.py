from src.search_algorithms import *


def plot_performances(cities: list, graph: Graph):
    """
    plot_performances is the main function invoked during performance plotting.
    It serves as a coordinator that integrates all performance computation routines and their visualization.
    For each algorithm, it calculates and plots the following metrics:
    - Number of expanded nodes
    - Processing time
    - Average memory usage
    - Peak memory usage
    - Maximum number of nodes allocated in memory during execution

    Inputs:
     - cities: list of location nodes
     - graph: graph structure used for performance analysis

    """

    nod_perf, time_perf, mem_perf, max_mem_perf, loc_nod_perf = performances_computation(cities, graph)
    results_nodes_a, results_nodes_d, results_nodes_bfs, results_nodes_dfs = perf_data_constructor(nod_perf)
    results_time_a, results_time_d, results_time_bfs, results_time_dfs = perf_data_constructor(time_perf)
    results_mem_a, results_mem_d, results_mem_bfs, results_mem_dfs = perf_data_constructor(mem_perf)
    res_max_mem_a, res_max_mem_d, res_max_mem_bfs, res_max_mem_dfs = perf_data_constructor(max_mem_perf)
    results_loc_nodes_a, results_loc_nodes_d, results_loc_nodes_bfs, results_loc_nodes_dfs = perf_data_constructor(
        loc_nod_perf)

    plot_constructor(results_nodes_a, results_nodes_d, results_nodes_bfs, results_nodes_dfs, "Expanded Nodes",
                     "Expanded Nodes")
    plot_constructor(results_time_a, results_time_d, results_time_bfs, results_time_dfs, "Processing Time",
                     "Processing Time  (s)")
    plot_constructor(results_mem_a, results_mem_d, results_mem_bfs, results_mem_dfs, "Mean Memory Usage",
                     "Memory Usage (KB)")
    plot_constructor(res_max_mem_a, res_max_mem_d, res_max_mem_bfs, res_max_mem_dfs, "Max Memory Usage",
                     "Memory Usage (KB)")
    plot_constructor(results_loc_nodes_a, results_loc_nodes_d, results_loc_nodes_bfs, results_loc_nodes_dfs,
                     "max Allocated Nodes", "Max Allocated Nodes")


def performances_computation(cities: list, graph: Graph):
    """
    This function computes key performance metrics for all algorithms across every possible path in the graph,
    then stores the results in their corresponding performance lists.

    Inputs:
     - cities: list of location nodes
     - graph: graph structure used for performance analysis

    Outputs:
     - node_perf: expanded node metrics
     - time_perf: processing time metrics
     - mem_perf: average memory usage metrics
     - max_mem_perf: peak memory usage metrics
     - loc_nod_perf: maximum number of nodes allocated in memory
    """

    nod_perf = []
    time_perf = []
    mem_perf = []
    max_mem_perf = []
    loc_nod_perf = []
    for location in cities:
        for location2 in cities:
            if location != location2:
                start = graph.get(location)
                goal = graph.get(location2)
                path_a, _, nodes_a, time_a, mean_mem_a, max_mem_a, allocated_nodes_a = astar(graph, start, goal)
                _, _, nodes_d, time_d, mean_mem_d, max_mem_d, allocated_nodes_d = dijkstra(graph, start, goal)
                _, _, nodes_bfs, time_bfs, mean_mem_bfs, max_mem_bfs, allocated_nodes_bfs = bfs(graph, start, goal)
                _, _, nodes_dfs, time_dfs, mean_mem_dfs, max_mem_dfs, allocated_nodes_dfs = dfs(graph, start, goal)

                add_perf_to_list(nod_perf, path_a, nodes_a, nodes_d, nodes_bfs, nodes_dfs)
                add_perf_to_list(time_perf, path_a, time_a, time_d, time_bfs, time_dfs)
                add_perf_to_list(mem_perf, path_a, mean_mem_a / 1024, mean_mem_d / 1024, mean_mem_bfs / 1024,
                                 mean_mem_dfs / 1024)
                add_perf_to_list(max_mem_perf, path_a, max_mem_a / 1024, max_mem_d / 1024, max_mem_bfs / 1024,
                                 max_mem_dfs / 1024)
                add_perf_to_list(loc_nod_perf, path_a, allocated_nodes_a, allocated_nodes_d, allocated_nodes_bfs,
                                 allocated_nodes_dfs)

    return nod_perf, time_perf, mem_perf, max_mem_perf, loc_nod_perf


def add_perf_to_list(perf_list, otp_path, data_a, data_d, data_bfs, data_dfs):
    """
    This helper function constructs a single entry for the performance lists generated in the
    `performance_computation` function. Each entry includes performance data for all algorithms
    on a given path, along with the optimal depth computed using A*.

    Specifically, the entry contains:
    - Optimal depth of the given path (computed with A*)
    - A* performance value for the selected parameter
    - Dijkstra performance value for the selected parameter
    - BFS performance value for the selected parameter
    - DFS performance value for the selected parameter

    Inputs:
     - perf_list: list to store the performance entry
     - otp_path: optimal depth of the given path computed using A*
     - data_a: A* performance metric for the given path
     - data_d: Dijkstra performance metric for the given path
     - data_bfs: BFS performance metric for the given path
     - data_dfs: DFS performance metric for the given path
    """

    perf_list.append({"depth": len(otp_path),
                      "A*": data_a,
                      "Dijkstra": data_d,
                      "BFS": data_bfs,
                      "DFS": data_dfs})


def perf_data_constructor(performances: list):
    """
    The data_construction function organizes all performance parameters stored in the performance lists
    by their corresponding optimal path depth. It then computes both the mean and standard deviation
    of each performance metric relative to the optimal path value.
    All computed results are saved into dedicated result dictionaries for each algorithm.

    Input:
     - performances: list containing all performance data entries

    Outputs:
     - results_a: dictionary with mean and standard deviation of performance metrics for the A* algorithm
     - results_d: dictionary with mean and standard deviation of performance metrics for the Dijkstra algorithm
     - results_bf: dictionary with mean and standard deviation of performance metrics for the BFS algorithm
     - results_df: dictionary with mean and standard deviation of performance metrics for the DFS algorithm
    """

    x_axis = {}
    for record in performances:
        depth = record["depth"]
        if depth not in x_axis:
            x_axis[depth] = {"A*": [], "Dijkstra": [], "BFS": [], "DFS": []}
        for algo in ["A*", "Dijkstra", "BFS", "DFS"]:
            x_axis[depth][algo].append(record[algo])

    results_a = {}
    results_d = {}
    results_bf = {}
    results_df = {}

    for depth, data in x_axis.items():
        results_a[depth] = [mean(data["A*"]), standard_deviation(data["A*"])]
        results_d[depth] = [mean(data["Dijkstra"]), standard_deviation(data["Dijkstra"])]
        results_bf[depth] = [mean(data["BFS"]), standard_deviation(data["BFS"])]
        results_df[depth] = [mean(data["DFS"]), standard_deviation(data["DFS"])]
    return results_a, results_d, results_bf, results_df


def plot_constructor(results_a, results_d, results_bfs, results_dfs, title: str, ylabel: str):
    """
    This function plots the mean and standard deviation of each algorithm’s performance data for direct comparison.

    Inputs:
     - results_a: dictionary containing mean and standard deviation of performance metrics for the A* algorithm
     - results_d: dictionary containing mean and standard deviation of performance metrics for the Dijkstra algorithm
     - results_bf: dictionary containing mean and standard deviation of performance metrics for the BFS algorithm
     - results_df: dictionary containing mean and standard deviation of performance metrics for the DFS algorithm
    """

    depths = sorted(results_a.keys())

    mean_a = [results_a[d][0] for d in depths]
    std_a = [results_a[d][1] for d in depths]

    mean_d = [results_d[d][0] for d in depths]
    std_d = [results_d[d][1] for d in depths]

    mean_bf = [results_bfs[d][0] for d in depths]
    std_bf = [results_bfs[d][1] for d in depths]

    mean_df = [results_dfs[d][0] for d in depths]
    std_df = [results_dfs[d][1] for d in depths]

    plt.figure(figsize=(10, 10))

    plt.errorbar(depths, mean_a, yerr=std_a, label='A*', color='blue', marker='o', capsize=5)
    plt.errorbar(depths, mean_d, yerr=std_d, label='Dijkstra', color='green', marker='o', capsize=5)
    plt.errorbar(depths, mean_bf, yerr=std_bf, label='BFS', color='orange', marker='o', capsize=5)
    plt.errorbar(depths, mean_df, yerr=std_df, label='DFS', color='red', marker='o', capsize=5)

    plt.xlabel('Solution Depth (Optimal Path Length)')
    plt.ylabel(f"{ylabel}")
    plt.title(f'Mean and Standard Deviation of {title} vs Solution Depth',
              fontsize=14, fontweight='bold')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.show()
