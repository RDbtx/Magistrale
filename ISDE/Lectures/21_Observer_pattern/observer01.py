from typing import Set


class Subscriber:

    def __init__(self, name: str) -> None:
        self.name = name

    def update(self, message: str) -> None:
        print(f"{self.name} recieved {message}")


class Publisher:

    def __init__(self, x: int) -> None:
        self._x = x
        self._subscribers: Set[Subscriber] = set()

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
                message = f"new value of x is {x}"
                self.dispatch(message)

    def dispatch(self, message: str) -> None:
        for subscriber in self._subscribers:
            subscriber.update(message)

    def register(self, subscriber: Subscriber) -> None:
        self._subscribers.add(subscriber)

    def unregister(self, subscriber: Subscriber) -> None:
        self._subscribers.remove(subscriber)


if __name__ == "__main__":
    obs1 = Subscriber("obs1")
    obs2 = Subscriber("obs2")
    obs3 = Subscriber("obs3")

    publisher = Publisher(0)

    publisher.register(obs1)
    publisher.register(obs2)

    publisher.x = 0

    publisher.x = 10

    publisher.unregister(obs1)

    publisher.x=30