from typing import Dict, Callable, List
from abc import ABC, abstractmethod


class Subscriber:

    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        return self.name

    def update(self, message: str) -> None:
        print(f"[{self}]: {message}")


class State(ABC):

    def _process_input(self, context: 'AC', value: str) -> None:
        self._action(context, value)
        self._changestate(context, value)

    @abstractmethod
    def _action(self, context: 'AC', value: str) -> None:
        pass

    @abstractmethod
    def _changestate(self, context: 'AC', value: str) -> None:
        pass


class StateOFF(State):
    def __init__(self, name: str = "OFF") -> None:
        self.name = name

    def __repr__(self) -> str:
        return self.name

    def _action(self, context: 'AC', value: str) -> None:
        if value == "ON" and context.temperature >= 24:
            print("AC is cooling")
        if value == "ON" and context.temperature < 24:
            print("AC is heating")

    def _changestate(self, context: 'AC', value: str) -> None:
        if value == "ON" and context.temperature >= 24:
            context.set_state(StateCooling())
            message = f"state switching to -> COOLING"
            context.dispatch("update", message)
        if value == "ON" and context.temperature < 24:
            context.set_state(StateHeating())
            message = f"state switching to -> HEATING"
            context.dispatch("update", message)


class StateCooling(State):
    def __init__(self, name: str = "COOLING") -> None:
        self.name = name

    def __repr__(self) -> str:
        return self.name

    def _action(self, context: 'AC', value: str) -> None:
        if value == "OFF":
            print("turning off AC")

        if value != "OFF" and context.temperature < 24:
            print("AC switching to heating")

    def _changestate(self, context: 'AC', value: str) -> None:
        if value == "OFF":
            context.set_state(StateOFF())
            message = f"state switching to -> OFF"
            context.dispatch("update", message)
        if value != "OFF" and context.temperature < 24:
            context.set_state(StateHeating())
            message = f"state switching to -> HEATING"
            context.dispatch("update", message)


class StateHeating(State):
    def __init__(self, name: str = "HEATING") -> None:
        self.name = name

    def __repr__(self) -> str:
        return self.name

    def _action(self, context: 'AC', value: str) -> None:
        if value == "OFF":
            print("turning off AC")
        if value != "OFF" and context.temperature >= 24:
            print("AC switching to cooling")

    def _changestate(self, context: 'AC', value: str) -> None:
        if value == "OFF":
            context.set_state(StateOFF())
            message = f"state switching to -> OFF"
            context.dispatch("update", message)
        if value != "OFF" and context.temperature >= 24:
            context.set_state(StateCooling())
            message = f"state switching to -> COOLING"
            context.dispatch("update", message)


class AC:
    default_method = "update"

    def __init__(self, events: List[str], temperature: int, name: str = "AC",
                 initial_state: State = StateOFF()) -> None:
        self._state = initial_state
        self._temperature = temperature
        self._name = name
        self._subscribers : Dict[str:Dict[Subscriber: Callable]] = {
            event: dict() for event in events
        }

    def __repr__(self) -> str:
        return self._name

    def set_state(self, state: State) -> None:
        self._state = state

    @property
    def temperature(self) -> int:
        return self._temperature

    @temperature.setter
    def temperature(self, value: int) -> None:
        self._temperature = value
        self._state._process_input(self, "")
        message = f"TEMPERATURE  = {self._temperature}°"
        self.dispatch("update", message)

    def dispatch(self, event: str, message: str) -> None:
        for method_to_invoke in self._subscribers[event].values():
            method_to_invoke(message)

    def register(self, event: str, subscriber: Subscriber, method_to_ivoke: Callable = None) -> None:
        if method_to_ivoke is None:
            method_to_ivoke = getattr(subscriber, self.default_method)
        self._subscribers[event][subscriber] = method_to_ivoke

    def unregister(self, event: str, subscriber: Subscriber) -> None:
        if subscriber in self._subscribers[event]:
            del self._subscribers[event][subscriber]

    def command(self,input : str) -> None:
        self._state._process_input(self,input)


if __name__ == "__main__":
    air_conditioner = AC(["update"],20)

    observer1 = Subscriber("observer1")
    observer2 = Subscriber("observer2")
    air_conditioner.register("update",observer1)
    air_conditioner.register("update",observer2)

    air_conditioner.temperature = 20
    air_conditioner.command("ON")
    air_conditioner.temperature = 25
    air_conditioner.temperature = 23
    air_conditioner.command("OFF")
