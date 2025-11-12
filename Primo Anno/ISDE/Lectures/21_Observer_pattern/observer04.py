from math import sqrt
from typing import Callable, Dict, List


class Subscriber:

    def __init__(self, name: str) -> None:
        self.name = name

    def update(self, message: str) -> None:
        print(f"{self.name} (update) received the message {message}")

    def receive(self, message: str) -> None:
        print(f"{self.name} (receive) received the message {message}")


class Segment:

    default_method = "update"

    def __init__(self, events: List[str], p1: List[int], p2: List[int]) -> None:
        self._p1 = p1
        self._p2 = p2
        self.segment_lenght = self.calculate_segment()
        self._subscribers: Dict[str: Dict[Subscriber: Callable]] = {
            event: dict() for event in events}

    @property
    def p1(self) -> List[int]:
        return self._p1

    @p1.setter
    def p1(self, coordinates : List[int]) -> None:
        if not hasattr(self, '_p1'):
            self._p1[0] = coordinates[0]
            self._p1[1] = coordinates[1]
        else:
            if self._p1[0] != coordinates[0] or self.p1[1] != coordinates[1]:
                self._p1[0] = coordinates[0]
                self._p1[1] = coordinates[1]
        if not hasattr(self, '_p2'):
            print("inserire p2")
        else:
            older_distance = self.segment_lenght
            if older_distance > self.calculate_segment():
                self.segment_lenght = self.calculate_segment()
                message = f" = [segment lenght decreased, new lenght is {self.segment_lenght}]"
                self.dispatch("decreased", message)
            if older_distance < self.calculate_segment():
                self.segment_lenght = self.calculate_segment()
                message = f" = [segment lenght increased, new lenght is {self.segment_lenght}]"
                self.dispatch("increased", message)

    @property
    def p2(self) -> List[int]:
        return self._p2

    @p2.setter
    def p2(self, coordinates : List[int]) -> None:
        if not hasattr(self, '_p2'):
            self._p2[0] = coordinates[0]
            self._p2[1] = coordinates[1]
        else:
            if self._p2[0] != coordinates[0] or self.p2[1] != coordinates[1]:
                self._p2[0] = coordinates[0]
                self._p2[1] = coordinates[1]
        if not hasattr(self, '_p1'):
            print("inserire p1")
        else:
            older_distance = self.segment_lenght
            if older_distance > self.calculate_segment():
                self.segment_lenght = self.calculate_segment()
                message = f" = [segment lenght decreased, new lenght is {self.segment_lenght}]"
                self.dispatch("decreased", message)
            if older_distance < self.calculate_segment():
                self.segment_lenght = self.calculate_segment()
                message = f" = [segment lenght increased, new lenght is {self.segment_lenght}]"
                self.dispatch("increased", message)

    def dispatch(self, event: str, message: str) -> None:
        for method_to_invoke in self._subscribers[event].values():
            method_to_invoke(message)

    def unregister(self, event: str, subscriber: Subscriber) -> None:
        if subscriber in self._subscribers[event]:
            del self._subscribers[event][subscriber]
            print(f"Unregistered subscriber {subscriber} from event '{event}'.")

    def register(self, event: str, subscriber: Subscriber, method_to_invoke: Callable = None) -> None:
        if method_to_invoke is None:
            method_to_invoke = getattr(subscriber, self.default_method)
        self._subscribers[event][subscriber] = method_to_invoke

    def calculate_segment(self) -> float:
        if not hasattr(self, '_p1') or not hasattr(self, '_p2'):
            self.segment_lenght = None
        else:
            distance = sqrt(pow(self._p1[0] - self._p2[0], 2) + pow(self._p1[1] - self._p2[1], 2))
            return distance


if __name__ == "__main__":
    obs1 = Subscriber("observer 1")
    obs2 = Subscriber("observer 2")
    publisher = Segment(["increased", "decreased"], [1, 2], [3, 4])

    publisher.register("increased",obs1)
    publisher.register("decreased",obs2)
    publisher.unregister("increased",obs1)
    publisher.unregister("decreased",obs2)


    publisher.p1 = [1,5]


    publisher.p2 = [15,6]

