from abc import abstractmethod, ABC
from tkinter.font import names
from typing import Dict, List, Callable


class Strategy(ABC):

    @abstractmethod
    def update(self, message: str) -> str:
        pass


class StrategyUppercase(Strategy):
    def update(self, message: str) -> str:
        return message.upper()


class StrategyLowercase(Strategy):
    def update(self, message: str) -> str:
        return message.lower()


class Subscriber:
    def __init__(self, name: str, strategy: Strategy):
        self.name = name
        self.strategy = strategy

    def __repr__(self) -> str:
        return self.name

    def update(self, message: str) -> None:
        print(f"{self} : {self.strategy.update(message)}")


class VendingMachine:
    default_method  = "update"

    def __init__(self, events: List[str], name: str = "vending machine", current_stock : int = 100):
        self.name = name
        self.current_stock = current_stock
        self._max_stock = 100
        self._subscribers : Dict[str: Dict[Subscriber: Callable]] = {
            event: dict() for event in events
        }

    def add_snacks(self, input : int):
        if input + self.current_stock >= self._max_stock:
            message = "stock is full"
            self.dispatch("stock full", message)
            self.current_stock = self._max_stock
        else:
            self.current_stock += input

    def dispense_snacks(self, input : int):
        if self.current_stock - input <=  0:
            message = "stock is low"
            self.dispatch("stock low", message)
            self.current_stock = 0
        else:
            self.current_stock -= input

    def dispatch(self, event : str, message : str) -> None:
        for methodtoinvoke in self._subscribers[event].values():
            methodtoinvoke( message)

    def register(self, event : str, subscriber: Subscriber, methodtoinvoke : Callable = None):
            if methodtoinvoke is None:
                methodtoinvoke = getattr(subscriber, self.default_method)
            self._subscribers[event][subscriber] = methodtoinvoke

    def unregister(self, event : str, subscriber: Subscriber) -> None:
        if subscriber in self._subscribers[event]:
            del self._subscribers[event][subscriber]

if "__main__" == __name__:



    observer1 = Subscriber("observer1", StrategyLowercase())
    observer2 = Subscriber("observer2", StrategyUppercase())

    vendingMachine = VendingMachine(["stock low", "stock full"])
    vendingMachine.register("stock low",observer1)
    vendingMachine.register("stock low",observer2)
    vendingMachine.register("stock full", observer1)
    vendingMachine.register("stock full", observer2)

    vendingMachine.add_snacks(100)
    vendingMachine.dispense_snacks(100)

    vendingMachine.unregister( "stock full", observer2)
    vendingMachine.add_snacks(100)