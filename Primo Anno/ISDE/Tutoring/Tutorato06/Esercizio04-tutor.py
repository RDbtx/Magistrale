from abc import abstractmethod, ABC


class Cities:
    """Utility class for storing the city names as strings."""
    Cagliari = "Cagliari"
    Rome = "Rome"
    Milan = "Milan"
    Paris = "Paris"


class CityState(ABC):

    def _travel(self, city, traveler):
        self._action(city, traveler)
        self._change_state(city, traveler)

    def _action(self, city, traveler):
        if city in self._destinations:
            print(f"Traveling to {city}")
            price, duration = self._destinations[city]
            traveler.price_payed += price
            traveler.time_traveled += duration
        else:
            print(f"Destination {city} is not available from here. Not traveling.")

    def _change_state(self, city, traveler):
        if city in self._destinations:
            traveler.set_state(states[city])


class Cagliari(CityState):
    _destinations = {
        Cities.Rome: [30, 45],
        Cities.Milan: [40, 60],
    }
    name = Cities.Cagliari


class Rome(CityState):
    _destinations = {
        Cities.Cagliari: [30, 45],
        Cities.Milan: [20, 30],
        Cities.Paris: [150, 100],
    }
    name = Cities.Rome


class Milan(CityState):
    _destinations = {
        Cities.Cagliari: [40, 60],
        Cities.Rome: [20, 30],
        Cities.Paris: [50, 100]
    }
    name = Cities.Milan


class Paris(CityState):
    _destinations = {
        Cities.Rome: [50, 100],
        Cities.Milan: [50, 100]
    }
    name = Cities.Paris


states = {Cities.Cagliari: Cagliari(),
          Cities.Rome: Rome(),
          Cities.Milan: Milan(),
          Cities.Paris: Paris()
          }


class Traveler:
    def __init__(self, name):
        self.name = name
        self.state = Cagliari()
        self.price_payed = 0
        self.time_traveled = 0

    def travel(self, city):
        self.state._travel(city, self)

    def set_state(self, new_state):
        self.state = new_state


class Planner:
    def __init__(self, strategy):
        self.strategy = strategy

    def choose_route(self, routes):
        best_route = self.strategy.choose_route(routes)
        print(f"{self.strategy}, best route: {best_route}")


class Strategy(ABC):
    @staticmethod
    @abstractmethod
    def choose_route(routes):
        pass


class CheapStrategy(Strategy):
    def choose_route(routes):
        best_route = 0  # will store the index of the best route
        best_price = 20000  # will store the best price
        for i, route in enumerate(routes):
            t = Traveler("Cheap Traveler")
            for destination in route:
                t.travel(destination)

            if t.state.name == route[-1]:
                if t.price_payed < best_price:
                    best_price = t.price_payed
                    best_route = i
        return routes[best_route]


class FastStrategy(Strategy):
    def choose_route(routes):
        best_route = 0  # will store the index of the best route
        best_duration = 20000  # will store the lowest duration

        for i, route in enumerate(routes):
            t = Traveler("Fast Traveler")
            for destination in route:
                t.travel(destination)

            if t.state.name == route[-1]:
                if t.time_traveled < best_duration:
                    best_duration = t.time_traveled
                    best_route = i
        return routes[best_route]