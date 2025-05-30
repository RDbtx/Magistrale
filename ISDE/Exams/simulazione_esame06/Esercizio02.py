from typing import Dict, List, Callable


class Subscriber:
    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        return self.name

    def console_log(self, message: str) -> None:
        print(f"[{self}][console_log]: {message}")

    def file_log(self, message: str) -> None:
        print(f"[{self}][file_log]: {message}")

    def alert_system(self, message: str) -> None:
        print(f"[{self}][alert_system]: {message}")


class StockMarket:
    default_method = "alert_system"

    def __init__(self, events: List[str],
                 google_value: float,
                 apple_value: float,
                 name: str = "stock market"
                 ) -> None:
        self.name = name
        self._google_value = google_value
        self._apple_value = apple_value
        self._subscribers: Dict[str:Dict[Subscriber:Callable]] = {
            event: dict() for event in events
        }

    @property
    def google_value(self) -> float:
        return self._google_value

    @google_value.setter
    def google_value(self, google_value: float) -> None:
        self._google_value = google_value
        message = f"GOOG = {google_value:.2f}"
        self.dispatch("goog", message)

    @property
    def apple_value(self) -> float:
        return self._apple_value

    @apple_value.setter
    def apple_value(self, apple_value: float) -> None:
        self._apple_value = apple_value
        message = f"AAPL = {apple_value:.2f}"
        self.dispatch("aapl", message)

    def register(self, event: str, subscriber: Subscriber,
                 method_to_invoke: Callable = None) -> None:
        if method_to_invoke is None:
            method_to_invoke = getattr(subscriber, self.default_method)
        self._subscribers[event][subscriber] = method_to_invoke

    def unregister(self, event: str, subscriber: Subscriber) -> None:
        if subscriber in self._subscribers[event]:
            del self._subscribers[event][subscriber]

    def dispatch(self, event: str, message: str) -> None:
        for method_to_invoke in self._subscribers[event].values():
            method_to_invoke(message)


if __name__ == "__main__":

    observer1 = Subscriber("observer1")
    observer2 = Subscriber("observer2")
    observer3 = Subscriber("observer3")

    stockmarket = StockMarket(["aapl","goog"],60,75)
    stockmarket.register("aapl",observer1)
    stockmarket.register("goog",observer1)
    stockmarket.register("aapl",observer2,observer2.console_log)
    stockmarket.register("goog",observer2,observer2.console_log)
    stockmarket.register("aapl",observer3,observer3.file_log)

    stockmarket.google_value = 50
    stockmarket.apple_value = 100

    stockmarket.unregister("aapl",observer3)
    stockmarket.apple_value = 50