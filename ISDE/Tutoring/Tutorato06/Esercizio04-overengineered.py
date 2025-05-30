from abc import ABC, abstractmethod


# implemented trough dijkstra algorithm
class Planner(ABC):

    @abstractmethod
    def find_route(self, current_state: 'States', destination: str):
        pass


class PlannerCheap(Planner):
    def find_route(self, current_state: 'States', destination: str):
        # Priority queue for Dijkstra's algorithm (manually implemented as a sorted list)
        # Each element is (cost, current_state, path)
        starting_state = current_state
        queue = [(0, current_state, [current_state.name])]  # (cost, current_state, path)
        visited = set()

        while queue:
            # Find the state with the lowest cost
            queue.sort(key=lambda x: x[0])  # Sort by cost (manually ensure priority queue)
            current_cost, current_state, path = queue.pop(0)  # Get the lowest-cost state

            # If we reach the destination, print the path and total cost
            if current_state.name == destination:
                print(f"\nCheapest path from {starting_state.name} to {destination}:")
                print(" -> ".join(path))
                print(f"Total cost = {current_cost}")
                return  # Exit once the destination is found

            # Mark the current state as visited
            if current_state.name in visited:
                continue
            visited.add(current_state.name)

            # Explore possible destinations from the current state
            for dest, details in current_state.possible_destinations.items():
                if dest not in visited:
                    new_cost = current_cost + details["price"]
                    new_path = path + [dest]
                    next_state = details.get("state", None)
                    if next_state is None:
                        # Dynamically create state if not already instantiated
                        next_state = globals()[dest.capitalize()]()
                    queue.append((new_cost, next_state, new_path))

        # If the queue is exhausted without finding the destination
        print(f"Cannot find a path from {starting_state.name} to {destination}.")


class PlannerFast(Planner):
    def find_route(self, current_state: 'States', destination: str):
        # Priority queue for Dijkstra's algorithm (manually implemented as a sorted list)
        # Each element is (cost, current_state, path)
        starting_state = current_state
        queue = [(0, current_state, [current_state.name])]  # (cost, current_state, path)
        visited = set()

        while queue:
            # Find the state with the lowest cost
            queue.sort(key=lambda x: x[0])  # Sort by cost (manually ensure priority queue)
            current_time, current_state, path = queue.pop(0)  # Get the lowest-cost state

            # If we reach the destination, print the path and total cost
            if current_state.name == destination:
                print(f"\nFastest path from {starting_state.name} to {destination}:")
                print(" -> ".join(path))
                print(f"Time needed = {current_time}")
                return  # Exit once the destination is found

            # Mark the current state as visited
            if current_state.name in visited:
                continue
            visited.add(current_state.name)

            # Explore possible destinations from the current state
            for dest, details in current_state.possible_destinations.items():
                if dest not in visited:
                    new_cost = current_time + details["time"]
                    new_path = path + [dest]
                    next_state = details.get("state", None)
                    if next_state is None:
                        # Dynamically create state if not already instantiated
                        next_state = globals()[dest.capitalize()]()
                    queue.append((new_cost, next_state, new_path))

        # If the queue is exhausted without finding the destination
        print(f"Cannot find a path from {starting_state.name} to {destination}.")


class Traveler:
    def __init__(self, nome: str, state: 'States') -> None:
        self.nome = nome
        self.state = state
        self.expenses = 0
        self.flight_time = 0

    def __repr__(self) -> str:
        return self.nome

    def about(self) -> None:
        print("\nTraveler's data:")
        print(f"{self} is actually in {self.state}")
        print(f"actual flight time = {self.flight_time}")
        print(f"total expenses = {self.expenses}")

    def moveto_cagliari(self) -> None:
        self.state.cagliari(self)

    def moveto_roma(self) -> None:
        self.state.roma(self)

    def moveto_milano(self) -> None:
        self.state.milano(self)

    def moveto_parigi(self) -> None:
        self.state.parigi(self)


class States(ABC):
    @abstractmethod
    def __init__(self):
        self.name = ""
        self.possible_destinations = {}
        pass

    @abstractmethod
    def cagliari(self, traveler: 'Traveler') -> None:
        pass

    @abstractmethod
    def roma(self, traveler: 'Traveler') -> None:
        pass

    @abstractmethod
    def milano(self, traveler: 'Traveler') -> None:
        pass

    @abstractmethod
    def parigi(self, traveler: 'Traveler') -> None:
        pass


class Cagliari(States):
    def __init__(self) -> None:
        self.name = "cagliari"
        self.possible_destinations = {"roma": {"price": 30, "time": 45},
                                      "milano": {"price": 30, "time": 45}}

    def __repr__(self):
        return self.name

    def cagliari(self, traveler: 'Traveler') -> None:
        print(f"{traveler} is already in {self}")

    def roma(self, traveler: 'Traveler') -> None:
        print(f"{traveler} moved from {traveler.state} to roma")
        traveler.expenses += self.possible_destinations["roma"]["price"]
        traveler.flight_time += self.possible_destinations["roma"]["time"]
        traveler.state = Roma()

    def milano(self, traveler: 'Traveler') -> None:
        print(f"\n{traveler} moved from {traveler.state} to milano")
        traveler.expenses += self.possible_destinations["milano"]["price"]
        traveler.flight_time += self.possible_destinations["milano"]["time"]
        traveler.state = Milano()

    def parigi(self, traveler: 'Traveler') -> None:
        print(f"there are no flights between {self} and paris")


class Roma(States):
    def __init__(self) -> None:
        self.name = "roma"
        self.possible_destinations = {"cagliari": {"state": Cagliari(), "price": 30, "time": 45},
                                      "milano": {"state": Milano(), "price": 20, "time": 30},
                                      "parigi": {"state": Parigi(), "price": 150, "time": 100}}

    def __repr__(self):
        return self.name

    def cagliari(self, traveler: 'Traveler') -> None:
        print(f"\n{traveler} moved from {traveler.state} to cagliari")
        traveler.expenses += self.possible_destinations["cagliari"]["price"]
        traveler.flight_time += self.possible_destinations["cagliari"]["time"]
        traveler.state = Cagliari()

    def roma(self, traveler: 'Traveler') -> None:
        print(f"{traveler} is aready in {self}")

    def milano(self, traveler: 'Traveler') -> None:
        print(f"\n{traveler} moved from {traveler.state} to milano")
        traveler.expenses += self.possible_destinations["milano"]["price"]
        traveler.flight_time += self.possible_destinations["milano"]["time"]
        traveler.state = self.possible_destinations["milano"]["state"]

    def parigi(self, traveler: 'Traveler') -> None:
        print(f"\n{traveler} moved from {traveler.state} to parigi")
        traveler.expenses += self.possible_destinations["parigi"]["price"]
        traveler.flight_time += self.possible_destinations["parigi"]["time"]
        traveler.state = Parigi()


class Milano(States):
    def __init__(self) -> None:
        self.name = "milano"
        self.possible_destinations = {"cagliari": {"price": 40, "time": 65},
                                      "roma": {"price": 20, "time": 30},
                                      "parigi": {"price": 50, "time": 100}}

    def __repr__(self):
        return self.name

    def cagliari(self, traveler: 'Traveler') -> None:
        print(f"\n{traveler} moved from {traveler.state} to cagliari")
        traveler.expenses += self.possible_destinations["cagliari"]["price"]
        traveler.flight_time += self.possible_destinations["cagliari"]["time"]
        traveler.state = Cagliari()

    def roma(self, traveler: 'Traveler') -> None:
        print(f"\n{traveler} moved from {traveler.state} to roma")
        traveler.expenses += self.possible_destinations["roma"]["price"]
        traveler.flight_time += self.possible_destinations["roma"]["time"]
        traveler.state = Roma()

    def milano(self, traveler: 'Traveler') -> None:
        print(f"{traveler} is aready in {self}")

    def parigi(self, traveler: 'Traveler') -> None:
        print(f"\n{traveler} moved from {traveler.state} to parigi")
        traveler.expenses += self.possible_destinations["parigi"]["price"]
        traveler.flight_time += self.possible_destinations["parigi"]["time"]
        traveler.state = Parigi()


class Parigi(States):
    def __init__(self) -> None:
        self.name = "parigi"
        self.possible_destinations = {"roma": {"price": 50, "time": 100},
                                      "milano": {"price": 50, "time": 100},
                                      }

    def __repr__(self):
        return self.name

    def cagliari(self, traveler: 'Traveler') -> None:
        print(f"there are no flights between {self} and cagliari")

    def roma(self, traveler: 'Traveler') -> None:
        print(f"\n{traveler} moved from {traveler.state} to roma")
        traveler.expenses += self.possible_destinations["roma"]["price"]
        traveler.flight_time += self.possible_destinations["roma"]["time"]
        traveler.state = Roma()

    def milano(self, traveler: 'Traveler') -> None:
        print(f"\n{traveler} moved from {traveler.state} to milano")
        traveler.expenses += self.possible_destinations["milano"]["price"]
        traveler.flight_time += self.possible_destinations["milano"]["time"]
        traveler.state = Milano()

    def parigi(self, traveler: 'Traveler') -> None:
        print(f"{traveler} is aready in {self}")


if __name__ == "__main__":

    plannermoney = PlannerCheap()
    plannermoney.find_route(Cagliari(), "parigi")
    plannertime = PlannerFast()
    plannertime.find_route(Cagliari(), "parigi")

    #fastroute
    traveler1 = Traveler("Giovanni", Cagliari())
    traveler1.moveto_roma()
    traveler1.moveto_parigi()
    traveler1.about()

    #cheapestroute
    traveler2 = Traveler("Marco", Cagliari())
    traveler2.moveto_milano()
    traveler2.moveto_parigi()
    traveler2.about()
