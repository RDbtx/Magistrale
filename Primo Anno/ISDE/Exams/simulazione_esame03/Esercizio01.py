# implementazione tramite state design pattern:

from abc import ABC, abstractmethod
import random


class State(ABC):

    def process_input(self, context: 'Robot', value: "str") -> None:
        self._action(context, value)
        self._changestate(context, value)

    @abstractmethod
    def _action(self, context: 'Robot', value: "str") -> None:
        pass

    @abstractmethod
    def _changestate(self, context: 'Robot', value: "str") -> None:
        pass


class StateInit(State):
    name = 'init'

    def __repr__(self):
        return self.name

    def _action(self, context: 'Robot', value: "str") -> None:
        context.about()

    def _changestate(self, context: 'Robot', value: "str") -> None:
        if value == "KEY1":
            context.set_state(StateMid())


class StateMid(State):
    _state_buffer = []
    name = 'mid'

    def __repr__(self):
        return self.name

    def _action(self, context: 'Robot', value: "str") -> None:
        context.about()

    def _changestate(self, context: 'Robot', value: "str") -> None:
        if value == "KEY1":
            pass
        elif value == "KEY2" and self._state_buffer == []:
            self._state_buffer.append(value)
        elif value == "KEY3" and "KEY2" in self._state_buffer:
            context.set_state(StateFinal())
        else:
            context.set_state(StateInit())
            self._state_buffer = []


class StateFinal(State):
    name = "final"

    def __repr__(self):
        return self.name

    def _action(self, context: 'Robot', value: "str") -> None:
        context.about()

    def _changestate(self, context: 'Robot', value: "str") -> None:
        if value in ["KEY1", "KEY2", "KEY3"]:
            context.set_state(StateInit())


class Robot:
    def __init__(self, name: str = "Robot", starting_state: State = StateInit()):
        self.name = name
        self._current_state = starting_state

    def __repr__(self):
        return self.name

    def about(self) -> None:
        print(f"{self} : Current State = [{self._current_state}]")

    def move(self, direction: str) -> None:
        if direction not in ["LEFT", "RIGHT", "UP", "DOWN"]:
            raise ValueError("Inexistent Direction!")
        # keys are randomic drops that the robot obtains from moving
        object = ["KEY1", "KEY2", "KEY3", "other"]
        pickup = self, random.choice(object)
        self._current_state.process_input(self, pickup[1])
        print(f"{self} moved and picked up : {pickup[1]}")

    def set_state(self, state: State):
        self._current_state = state


if __name__ == "__main__":
    robot = Robot()
    robot.move("UP")
    robot.move("DOWN")
    robot.move("LEFT")
    robot.move("RIGHT")
    robot.move("UP")
    robot.move("DOWN")
    robot.move("LEFT")
    robot.move("RIGHT")
    robot.move("UP")
    robot.move("DOWN")
    robot.move("LEFT")
    robot.move("RIGHT")
