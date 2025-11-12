from src.search_algorithms import *
from src.performances import plot_performances

map_location = "../map.json"

if __name__ == "__main__":
    map = load_graph_and_plot(map_location)

    print("\n---- THE ELDER WALKER ----")
    print("\nCities and locations of Skyrim:\n")
    cities = map.get_names()

    print("Total number of locations:", len(cities))

    working = True
    while working:

        menu_decisions = [0, 1, 2, 3]
        print("\nWhat do you want to do?")
        print("1- Create your journey")
        print("2- Show Skyrim Map")
        print("3- Show Algorithms' Overall Performances")
        print("0- Close the program")

        decision = 5
        while decision not in menu_decisions:
            decision = int(input("select your decision [1/2/3/0]: "))

        print("\n")
        if decision == 1:
            starting_location = ""
            destination = ""
            while starting_location not in cities:
                starting_location = input("Enter your starting location: ")
            while destination not in cities:
                destination = input("Enter your goal location: ")

            start = map.get(starting_location)
            goal = map.get(destination)

            algorithm_decisions = [1, 2, 3, 4]
            print("\nWhat algorithm do you want to use?")
            print("1- A*")
            print("2- Dijkstra")
            print("3- Breath first search")
            print("4- Depth first search")
            algorithm_decision = 5
            while algorithm_decision not in algorithm_decisions:
                algorithm_decision = int(input("select your algorithm [1/2/3/4]: "))

            print("\n")
            print("\nCalculating your journey...")

            if algorithm_decision == 1:
                path, cost, nodes_a, time_a, mean_alloc, max_alloc, _ = astar(map, start, goal)
                print("A*:", " -> ".join(n.name for n in path),
                      f"\n\n---- PERFORMANCES ----"
                      f"\ntotal cost: {cost:.2f}"
                      f"\nNodes expanded: {nodes_a}"
                      f"\nprocessing time: {time_a} s"
                      f"\nmean memory allocated: {mean_alloc / 1024:.2f} KB"
                      f"\nmax memory allocated: {max_alloc / 1024:.2f} KB")
                plot_path(path, "A*", start, goal)

            if algorithm_decision == 2:
                path, cost, nodes_d, time_d, mean_alloc, max_alloc, _ = dijkstra(map, start, goal)
                print("DIJKSTRA:", " -> ".join(n.name for n in path),
                      f"\n\n---- PERFORMANCES ----"
                      f"\ntotal cost: {cost:.2f}"
                      f"\nNodes expanded: {nodes_d}"
                      f"\nprocessing time: {time_d} s"
                      f"\nmean memory allocated: {mean_alloc / 1024:.2f} KB"
                      f"\nmax memory allocated: {max_alloc / 1024:.2f} KB")
                plot_path(path, "DIJKSTRA", start, goal)

            if algorithm_decision == 3:
                path, cost, nodes_bf, time_bf, mean_alloc, max_alloc, _ = bfs(map, start, goal)
                print("BFS:", " -> ".join(n.name for n in path),
                      f"\n\n---- PERFORMANCES ----"
                      f"\ntotal cost: {cost:.2f}"
                      f"\nNodes expanded: {nodes_bf}"
                      f"\nprocessing time: {time_bf} s"
                      f"\nmean memory allocated: {mean_alloc / 1024:.2f} KB"
                      f"\nmax memory allocated: {max_alloc / 1024:.2f} KB")
                plot_path(path, "BFS", start, goal)
            if algorithm_decision == 4:
                path, cost, nodes_df, time_df, mean_alloc, max_alloc, _ = dfs(map, start, goal)
                print("DFS:", " -> ".join(n.name for n in path),
                      f"\n\n---- PERFORMANCES ----"
                      f"\ntotal cost: {cost:.2f}"
                      f"\nNodes expanded: {nodes_df}"
                      f"\nprocessing time: {time_df} s"
                      f"\nmean memory allocated: {mean_alloc / 1024:.2f} KB"
                      f"\nmax memory allocated: {max_alloc / 1024:.2f} KB")
                plot_path(path, "DFS", start, goal)

        elif decision == 2:
            print("\nCities and locations of Skyrim:")
            _ = map.get_names()
            print("Total number of locations:", len(cities))

        elif decision == 3:
            print("\n---- PERFORMACES -----")
            print("Performances report generation...")
            plot_performances(cities, map)

        elif decision == 0:
            print("\nClosing the program...")
            working = False
