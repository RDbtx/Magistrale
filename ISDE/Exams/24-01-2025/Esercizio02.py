# EXERCISE 2
# STUDENT NAME RICCARDO DEIDDA
# STUDENT ID 70/90/00639


from abc import ABC, abstractmethod
from typing import Dict, Callable, List
import time


class State(ABC):
    def process_input(self, context: 'TrafficLights', value) -> None:
        self._action(context, value)
        self._change_state(context, value)

    @abstractmethod
    def _action(self, context: 'TrafficLights', value) -> None:
        pass

    @abstractmethod
    def _change_state(self, context: 'TrafficLights', value) -> None:
        pass


class RedState(State):
    def _action(self, context: 'TrafficLights', value) -> None:
        message = f"RED LIGHT"
        context.dispatch("RED", message)

    def _change_state(self, context: 'TrafficLights', value) -> None:
        if str(value) == "1":
            context.change_state(GreenState())
        if str(value) == "0":
            context.change_state(BlinkingYellowState())


class GreenState(State):
    def _action(self, context: 'TrafficLights', value):
        message = f"GREEN LIGHT"
        context.dispatch("GREEN", message)

    def _change_state(self, context: 'TrafficLights', value) -> None:
        if str(value) == "1":
            context.change_state(YellowState())
        if str(value) == "0":
            context.change_state(BlinkingYellowState())


class YellowState(State):
    def _action(self, context: 'TrafficLights', value) -> None:
        message = f"YELLOW LIGHT"
        context.dispatch("YELLOW", message)

    def _change_state(self, context: 'TrafficLights', value) -> None:
        if str(value) == "1":
            context.change_state(RedState())
        if str(value) == "0":
            context.change_state(BlinkingYellowState())


class BlinkingYellowState(State):
    def _action(self, context: 'TrafficLights', value) -> None:
        message = f"BLINKING YELLOW LIGHT"
        context.dispatch("BLINKING_YELLOW", message)

    def _change_state(self, context: 'TrafficLights', value) -> None:
        if str(value) == "1":
            context.change_state(RedState())


class Subscriber:
    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        return self.name

    def stop(self, message: str) -> None:
        print(f"[{self}] : {message}, dont move")

    def move(self, message) -> None:
        print(f"[{self}] : {message}, you can move")

    def slow_down(self, message: str) -> None:
        print(f"[{self}] : {message}, slow down")

    def move_with_caution(self, message: str) -> None:
        print(f"[{self}] : {message}, move with caution")


class TrafficLights:

    def __init__(self, events: List[str], initial_state: State = RedState()) -> None:
        self._state = initial_state
        self._subscribers: Dict[str:Dict[Subscriber: Callable]] = {
            event: dict() for event in events
        }

    def dispatch(self, event: str, message: str) -> None:
        for method_to_invoke in self._subscribers[event].values():
            method_to_invoke(message)

    def register(self, event: str, subscriber: Subscriber, method_to_invoke: Callable) -> None:
        self._subscribers[event][subscriber] = method_to_invoke

    def unregister(self, event: str, subscriber: Subscriber) -> None:
        if subscriber in self._subscribers[event]:
            del self._subscribers[event][subscriber]

    def process_input(self, value) -> None:
        self._state.process_input(self, value)

    def change_state(self, state: State) -> None:
        self._state = state


if __name__ == '__main__':
    # publisher creation
    publisher = TrafficLights(["RED", "GREEN", "YELLOW", "BLINKING_YELLOW"])
    # observers creation
    observer1 = Subscriber("observer1")
    observer2 = Subscriber("observer2")
    observer3 = Subscriber("observer3")
    observer4 = Subscriber("observer4")

    # register functionality
    publisher.register("RED", observer1, observer1.stop)
    publisher.register("GREEN", observer2, observer2.move)
    publisher.register("YELLOW", observer3, observer3.slow_down)
    publisher.register("BLINKING_YELLOW", observer4, observer4.move_with_caution)

    # test
    print("first test with all the observers:")
    publisher.process_input(0)
    for value in range(10):
        publisher.process_input(1)
        time.sleep(1)
    publisher.process_input(0)

    # unregister functionality
    publisher.unregister("BLINKING_YELLOW", observer4)
    publisher.unregister("RED", observer1)
    publisher.unregister("YELLOW", observer3)

    # test without: red, yellow and blinking yellow observations
    print("\nsecond test with unregistered observers:")
    publisher.process_input(0)
    for value in range(10):
        publisher.process_input(1)
        time.sleep(1)
    publisher.process_input(0)
