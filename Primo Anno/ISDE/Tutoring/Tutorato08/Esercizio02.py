from typing import Dict, Callable
from abc import abstractmethod, ABC


class Strategy(ABC):

    @abstractmethod
    def action(self, change) -> None:
        pass


class Buy(Strategy):
    def action(self, change: float) -> int:
        if change < 0:
            print(f"\nBuying on decrease of {change * 100:.2f}%, {abs(change * 100):.2f}$ of action acquired")
            return int(change * 100)
        return 0


class Sell(Strategy):
    def action(self, change: float) -> int:
        if change > 0:
            print(f"\nSelling on increase: {change * 100}%")
            return int(change * 100)
        return 0


class Subscriber:

    def __init__(self, name: str, budget: int = 100, investment: int = 100) -> None:
        self.name = name
        self.budget = budget
        self.investment = investment
        self.strategy = None

    def __repr__(self) -> str:
        return self.name

    def update(self, change):
        variation = self.strategy.action(change)
        self.budget += variation
        self.investment -= self.strategy.action(change)
        print(f"{self.name} = [budget: {self.budget:.2f}, investment: {self.investment:.2f}]")


class StockMarket:
    default_method = "update"

    def __init__(self, market_value: int) -> None:
        self._subscribers: Dict[Subscriber, Callable] = {}
        self._market_value = market_value

    @property
    def market_value(self) -> int:
        return self._market_value

    @market_value.setter
    def market_value(self, market_value: int) -> None:
        old_market_value = self._market_value
        self._market_value = market_value
        mvv = ((market_value - old_market_value) / old_market_value)
        for subscriber in self._subscribers.keys():
            subscriber.investment = subscriber.investment * (1 + mvv)
            if mvv < 0:
                subscriber.strategy = Buy()
            if mvv > 0:
                subscriber.strategy = Sell()
        self.dispatch(mvv)

    def get_subscribers(self) -> None:
        print("\nList of subscribers:")
        for subscriber in self._subscribers.keys():
            print(f"Name:{subscriber} budget:{subscriber.budget} investment:{subscriber.investment}")

    def register(self, subscriber: Subscriber, method_to_invoke: Callable = None) -> None:
        if method_to_invoke is None:
            method_to_invoke = getattr(subscriber, self.default_method)
        self._subscribers[subscriber] = method_to_invoke

    def unregister(self, subscriber: Subscriber) -> None:
        if subscriber in self._subscribers:
            del self._subscribers[subscriber]

    def dispatch(self, variation) -> None:
        for method_to_invoke in self._subscribers.values():
            method_to_invoke(variation)


if __name__ == "__main__":
    subscriber = Subscriber("Subscriber1", 100, 100)
    subscriber2 = Subscriber("Subscriber2", 100, 100)

    wall_street = StockMarket(100)
    wall_street.register(subscriber)
    wall_street.register(subscriber2)
    wall_street.get_subscribers()

    wall_street.market_value = 3000

    wall_street.market_value = 50
