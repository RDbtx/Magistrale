from typing import Callable, Dict, List


class Subscriber:

    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        return self.name

    def console_logger(self, message: str) -> None:
        print(f"[{self}] console log: {message}")

    def file_logger(self, message: str) -> None:
        print(f"[{self}] file log: {message}")

    def mobile_allert(self, message: str) -> None:
        print(f"[{self}] mobile allert: {message}")


class StockExchange:
    default_method = "mobile_allert"

    def __init__(self, events: List[str], bitcoin: float, ethereum: float, doge: float,
                 name: str = "StockExchange") -> None:
        self.name = name
        self._bitcoin = bitcoin
        self._ethereum = ethereum
        self._doge = doge
        self._subscribers: Dict[str:Dict[Subscriber: Callable]] = {
            event: dict() for event in events
        }

    @property
    def bitcoin(self) -> float:
        return self._bitcoin

    @bitcoin.setter
    def bitcoin(self, value: float) -> None:
        message = f"BTC {self._bitcoin} -> {value}"
        self._bitcoin = value
        self.dispatch("update", message)

    @property
    def ethereum(self) -> float:
        return self._ethereum

    @ethereum.setter
    def ethereum(self, value: float) -> None:
        message = f"ETH {self._ethereum} -> {value}"
        self._ethereum = value
        self.dispatch("update", message)

    @property
    def doge(self) -> float:
        return self._doge

    @doge.setter
    def doge(self, value: float) -> None:
        message = f"DOGE {self._doge} -> {value}"
        self._doge = value
        self.dispatch("update", message)

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


if "__main__" == __name__:
    stockexchange = StockExchange(["update"], 50, 30, 80)
    observer1 = Subscriber("observer1")
    observer2 = Subscriber("observer2")
    observer3 = Subscriber("observer3")

    stockexchange.register("update", observer1)
    stockexchange.register("update", observer2, observer2.file_logger)
    stockexchange.register("update", observer3, observer3.console_logger)

    stockexchange.bitcoin = 100
    stockexchange.unregister("update", observer1)
    stockexchange.unregister("update", observer2)
    stockexchange.ethereum = 10
    stockexchange.doge = 23
