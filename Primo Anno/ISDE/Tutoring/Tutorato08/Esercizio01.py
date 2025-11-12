from typing import Dict, Callable, List


class Subscriber:

    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        return self.name

    def update(self, message: str) -> None:
        print(f"{self.name} = {message}")


class Publisher:
    default_method = "update"

    def __init__(self, events: List[str]) -> None:
        self._subscribers: Dict[str: Dict[Subscriber: Callable]] = {
            event: dict() for event in events
        }

    def get_subscribers(self, event: [List[str]]) -> None:
        for elem in event:
            if elem in self._subscribers:
                print(f"\n{elem}:", end="")
                for subscriber in self._subscribers[elem]:
                    print(f" [{subscriber}] ", end="")

    def dispatch(self, event: str, message: str) -> None:
        for method_to_invoke in self._subscribers[event].values():
            method_to_invoke(message)

    def register(self, event: List[str], subscriber: Subscriber, method_to_invoke: Callable = None) -> None:
        for item in event:
            if method_to_invoke is None:
                method_to_invoke = getattr(subscriber, self.default_method)
            self._subscribers[item][subscriber] = method_to_invoke
            message = f"{subscriber.name}: has been added to {item}!"
            self.dispatch(item, message)

    def unregister(self, event, subscriber: Subscriber) -> None:
        if subscriber in self._subscribers:
            del self._subscribers[event][subscriber]


if __name__ == "__main__":
    subscriber01 = Subscriber("subscriber01")
    subscriber02 = Subscriber("subscriber02")

    company = Publisher(["telegram", "mail", "slack", "database"])
    company.register(["telegram", "mail"], subscriber01)
    company.register(["telegram"], subscriber02)

    company.get_subscribers(["telegram", "mail"])
