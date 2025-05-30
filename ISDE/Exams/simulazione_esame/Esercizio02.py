from abc import abstractmethod, ABC
from string import ascii_lowercase, ascii_uppercase, ascii_letters
from typing import Dict, Callable


class State(ABC):
    def process_input(self, context: 'StateMachine', value) -> None:
        self._action(context, value)
        self._change_state(context, value)

    @abstractmethod
    def _action(self, context: 'StateMachine', value) -> None:
        pass

    @abstractmethod
    def _change_state(self, context: 'StateMachine', value) -> None:
        pass


class Subscriber:

    def __init__(self, name: str) -> None:
        self._name = name

    def update(self, message: str) -> None:
        print(f"\n[{self._name}]: {message}")


class StateInitial(State):

    def _action(self, context: 'StateMachine', value) -> None:
        print(value,end = "")

    def _change_state(self, context: 'StateMachine', value) -> None:
        if value == 0:
            context.set_state(StateMiddle())
            message = "Initial -> Middle"
            context.dispatch("middle", message)


class StateMiddle(State):
    _state_buffer = []

    def _action(self, context: 'StateMachine', value) -> None:
        pass

    def _change_state(self, context: 'StateMachine', value) -> None:
        if value == 0 or str(value) in ascii_letters:
            pass
        elif value == 2 and self._state_buffer[0] == 1:
            context.set_state(StateFinal())
            message = "Middle -> Final"
            context.dispatch("final", message)
            self._state_buffer = []
        elif value == 1 and self._state_buffer == []:
            self._state_buffer.append(value)
        else:
            context.set_state(StateInitial())
            message = "Middle -> Initial"
            context.dispatch("initial", message)
            self._state_buffer = []


class StateFinal(State):

    def _action(self, context: 'StateMachine', value) -> None:
        if str(value) in ascii_letters:
            if value == 'z':
                print('a', end = "")
            elif value == 'Z':
                print('A', end = "")
            else:
                ch_index = ascii_letters.index(value)
                print(ascii_letters[ch_index + 1], end = "")
        else:
            print(value, end = "")

    def _change_state(self, context: 'StateMachine', value) -> None:
        if value == 0:
            context.set_state(StateInitial())
            message = "Final -> Initial"
            context.dispatch("initial", message)


class StateMachine:
    default_method = "update"

    def __init__(self, events: list[str], state: State = StateInitial()) -> None:
        self._state = state
        self._accepted_signals = [0, 1, 2]
        self._subscribers: Dict[str: Dict[Subscriber: Callable]] = {
            event: dict() for event in events
        }

    def signal(self, value: int) -> None:
        if value in self._accepted_signals:
            self._state.process_input(self, value)
        else:
            raise ValueError(f'Value {value} is not accepted! accepted values are {self._accepted_signals}')

    def c_input(self, value: str) -> None:
        if value in ascii_uppercase or value in ascii_lowercase:
            self._state.process_input(self, value)
        else:
            raise ValueError(f'Value {value} is not accepted! Value Should be a char')

    def set_state(self, state: State) -> None:
        self._state = state

    def register(self, event: str, subscriber: Subscriber, method_to_invoke: Callable = None) -> None:
        if method_to_invoke is None:
            method_to_invoke = getattr(subscriber, self.default_method)
        self._subscribers[event][subscriber] = method_to_invoke

    def unregister(self, event: str, subscriber: Subscriber) -> None:
        if subscriber in self._subscribers:
            del self._subscribers[event][subscriber]

    def dispatch(self, event: str, message: str) -> None:
        for methodtoinvoke in self._subscribers[event].values():
            methodtoinvoke(message)


if __name__ == '__main__':
    observer1 = Subscriber('observer1')
    observer2 = Subscriber('observer2')
    observer3 = Subscriber('observer3')

    publisher = StateMachine(["initial", "middle", "final"])

    publisher.register("initial", observer1)
    publisher.register("middle", observer2)
    publisher.register("final", observer3)

    signals = [0,0,1,2,1,2,0,0,0]
    chars = ascii_letters

    for signal in signals:
        publisher.signal(signal)
        for char in chars:
            publisher.c_input(char)
