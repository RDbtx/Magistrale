from typing import Dict, List, Callable
from abc import ABC, abstractmethod


class Strategy(ABC):
    @abstractmethod
    def alert(self) -> None:
        pass


class StrategyLog(Strategy):
    def alert(self) -> str:
        return f"stock log has been updated!"


class StrategyAlert(Strategy):
    def alert(self) -> str:
        return f"depot manager has been alerted!"


class Subscriber:

    def __init__(self, strategy, name: str) -> None:
        self._strategy = strategy
        self.name = name

    def __repr__(self) -> str:
        return self.name

    def update(self, message: str) -> None:
        if "out of stock" in message:
            self._strategy = StrategyAlert()
        else:
            self._strategy = StrategyLog()
        print(f"{self}: {message}, {self._strategy.alert()}")


class Depot:
    default_method = "update"

    def __init__(self, events: List[str], stock: int, name: str = "AmmoDepot", max_cap: int = 500) -> None:
        self.name = name
        self.stock = stock
        self.stock_threshold = (max_cap * 20 / 100)
        self.max_cap = max_cap
        self._subscribers: Dict[str:Dict[Subscriber:Callable]] = {
            event: dict() for event in events
        }

    def __repr__(self) -> str:
        return self.name

    def ammunition_requested(self, input: int) -> None:
        if self.stock - input <= self.stock_threshold:
            self.stock -= input
            message = f"{self} stock is running low"
            self.dispatch("low stock", message)
        if self.stock - input <= 0:
            self.stock = 0
            message = f"{self} is out of stock"
            self.dispatch("out of stock", message)
        else:
            self.stock -= input
            message = f"{input} tonnes of ammunition has been requested, current {self} stock is {self.stock}"
            self.dispatch("movement", message)

    def ammunition_restocked(self, input: int) -> None:
        if self.stock + input >= self.max_cap:
            self.stock = self.max_cap
            message = f"{self} is full"
            self.dispatch("full", message)
        else:
            self.stock += input
            message = f"{input} tonnes of ammunition has been restocked, current {self} stock is {self.stock}"
            self.dispatch("movement", message)

    def dispatch(self, event: str, message: str) -> None:
        for method_to_invoke in self._subscribers[event].values():
            method_to_invoke(message)

    def register(self, event: List[str], subscriber: Subscriber, method_to_invoke: Callable = None) -> None:
        if method_to_invoke is None:
            method_to_invoke = getattr(subscriber, self.default_method)
        for item in event:
            self._subscribers[item][subscriber] = method_to_invoke

    def unregister(self, event: str, subscriber: Subscriber) -> None:
        if subscriber in self._subscribers[event]:
            del self._subscribers[event][subscriber]


if __name__ == "__main__":

    observer1 = Subscriber(StrategyLog(), "Admin")
    depot = Depot(["movement", "full", "out of stock", "low stock"], 500)
    depot.register(["movement", "full", "out of stock", "low stock"], observer1)

    depot.ammunition_requested(50)
    depot.ammunition_restocked(50)
    depot.ammunition_requested(500)
