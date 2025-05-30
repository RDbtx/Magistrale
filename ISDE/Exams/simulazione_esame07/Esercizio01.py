from abc import ABC, abstractmethod
from time import sleep


class State(ABC):
    def _process_input(self, context: 'ATGM', input: str) -> None:
        self._action(context, input)
        self._change_state(context, input)

    @abstractmethod
    def _action(self, context: 'ATGM', input: str) -> None:
        pass

    @abstractmethod
    def _change_state(self, context: 'ATGM', input: str) -> None:
        pass


class IdleState(State):
    def _action(self, context: 'ATGM', input: str) -> None:
        print(f"{context} ready to rumble sir!")
        print(f"Target locked = [{input}]")


    def _change_state(self, context: 'ATGM', input: str) -> None:
        context.set_state(TargetLockState())


class TargetLockState(State):
    def _action(self, context: 'ATGM', input: str) -> None:
        if input == "fire":
            print("Missile has been fired")
        else:
            pass

    def _change_state(self, context: 'ATGM', input: str) -> None:
        if input == "fire":
            context.set_state(FiredState())
        else:
            pass


class FiredState(State):
    timer = 0.0

    def _action(self, context: 'ATGM', input: str) -> None:
        tti = context.target_distance / context.velocity
        self.timer = tti
        print(f"TTI = {tti}s")

    def _change_state(self, context: 'ATGM', input: str) -> None:
        sleep(self.timer)
        context.set_state(ImpactState())


class ImpactState(State):
    def _action(self, context: 'ATGM', input: str) -> None:
        if input == "reload":
            print("reloading atgm")
        else:
            print("IMPACT! TARGET DESTROYED")

    def _change_state(self, context: 'ATGM', input: str) -> None:
        if input == "reload":
            sleep(5)
            print("atgm has been reloaded")
            context.set_state(IdleState())


class ATGM:
    def __init__(self, name: str = "SpikeLR",
                 velocity: int = 2100,
                 maxrange: int = 1000,
                 inital_state: State = IdleState()) -> None:
        self._name = name
        self._maxrange = maxrange
        self._state = inital_state
        self.target_distance = 0
        self.velocity = velocity

    def __repr__(self) -> str:
        return self._name

    def target_lock(self, target_name: str, distance) -> None:
        if isinstance(self._state, IdleState) and self._maxrange >= distance:
            self.target_distance = distance
            self._state._process_input(self, target_name)

        else:
            print("invalid input state")

    def fire(self) -> None:
        if isinstance(self._state, TargetLockState):
            self._state._process_input(self, "fire")
            self._state._process_input(self, "fly me to the moon")
            self._state._process_input(self, "blood for the blood god")
        else:
            print("invalid input state, no target has been Locked!")

    def reload(self) -> None:
        if isinstance(self._state, ImpactState):
            self._state._process_input(self, "reload")

    def set_state(self, state: State) -> None:
        self._state = state


if __name__ == "__main__":

    atgm = ATGM(name="SpikeLR")


    print("A enemy t-90 has been spotted")
    atgm.target_lock("T-90", 800)
    atgm.fire()  # Should succeed and calculate TTI
    atgm.reload()
