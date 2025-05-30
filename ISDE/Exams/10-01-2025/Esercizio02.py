from abc import ABC, abstractmethod
from typing import Dict, Callable, List


class Strategy(ABC):
    @abstractmethod
    def print(self, event: str) -> str:
        pass


class StrategyUppercase(Strategy):
    def print(self, event: str) -> str:
        return event.upper()


class StrategyLowercase(Strategy):
    def print(self, event: str) -> str:
        return event.lower()


class Subscriber:
    def __init__(self, strategy: Strategy, name: str) -> None:
        self.name = name
        self.strategy = strategy

    def __repr__(self) -> str:
        return self.name

    # As requested, the event is printed uppercase or lowercase depending on the strategy chosen by the subscriber
    def update(self, event: str) -> None:
        print(f"[{self}]: {self.strategy.print(event)}")

# piggybank is the publisher
class PiggyBank:
    default_method = "update"

    def __init__(self, events: List[str], budget: int = 0, name: str = "PiggyBank") -> None:
        self.name = name
        self.budget = budget
        self.max_budget = 200
        self._subscribers: Dict[str: Dict[Subscriber: Callable]] = {
            event: dict() for event in events
        }

    def insert(self, money: int) -> None:
        # observer want to know if some coins are inserted even if the insertion causes the piggybank to
        # be at max capacity. Because of this the dispatch function is called everytime the insert function
        # is invoked in order to flag both events.
        event = "coin inserted"
        self.dispatch(event, event)
        if self.budget + money >= self.max_budget:
            self.budget = self.max_budget
            event = "piggybank full"
            self.dispatch(event, event)
        else:
            self.budget += money

    def withdraw(self, money: int) -> None:
        if self.budget - money < 0:
            self.budget = 0
        else:
            self.budget -= money

    def dispatch(self, event: str, message: str) -> None:
        for method_to_invoke in self._subscribers[event].values():
            method_to_invoke(message)

    def register(self, event: str, subscriber: Subscriber, method_to_invoke: Callable = None) -> None:
        if method_to_invoke is None:
            method_to_invoke = getattr(subscriber, self.default_method)
        self._subscribers[event][subscriber] = method_to_invoke

    def unregister(self, event: str, subscriber: Subscriber) -> None:
        if subscriber in self._subscribers[event]:
            del self._subscribers[event][subscriber]


if __name__ == "__main__":
    observer1 = Subscriber(StrategyUppercase(), "observer1")
    observer2 = Subscriber(StrategyLowercase(), "observer2")

    piggybank = PiggyBank(["piggybank full", "coin inserted"])

    piggybank.register("piggybank full", observer1)
    piggybank.register("piggybank full", observer2)

    piggybank.register("coin inserted", observer1)
    piggybank.register("coin inserted", observer2)

    piggybank.insert(100)

    piggybank.unregister("piggybank full", observer1)
    observer2.strategy = StrategyUppercase()

    piggybank.insert(100)
