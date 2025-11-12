from typing import Dict, Callable


class Subscriber:

    def __init__(self, name) -> None:
        self.name = name

    def update(self, message: str) -> None:
        print(f"{self.name} (upade method) received the message {message}")

    def receive(self, x: int) -> None:
        print(f"{self.name} (received method) received the message")


class Publisher:
    default_method_name = "update"

    def __init__(self, x) -> None:
        self._x = x
        self._subscribers: Dict[Subscriber: Callable] = dict()

    @property
    def x(self) -> int:
        return self._x

    @x.setter
    def x(self, x: int) -> None:
        if not hasattr(self, "_x"):
            self._x = x
        else:
            if self._x != x:
                self._x = x
                message = f"the new value of x is {x}"
                self.dispatch(message)

    def dispatch(self, message: str) -> None:
        for method_to_invoke in self._subscribers.values():
            method_to_invoke(message)

    def register(self, subscriber: Subscriber, methodtoinvoke: Callable = None) -> None:
        if methodtoinvoke is None:
            methodtoinvoke = getattr(subscriber, self.default_method_name)
        self._subscribers[subscriber] = methodtoinvoke

    def unregister(self, subscriber: Subscriber) -> None:
        if subscriber in self._subscribers:
            del self._subscribers[subscriber]


if __name__ == "__main__":
    obs1 = Subscriber("obs1")
    obs2 = Subscriber("obs2")
    publisher = Publisher(0)

    publisher.register(obs1)
    publisher.register(obs2, obs2.receive)

    publisher.x = 0

    publisher.x = 10

    publisher.unregister(obs1)

    publisher.x = 20
