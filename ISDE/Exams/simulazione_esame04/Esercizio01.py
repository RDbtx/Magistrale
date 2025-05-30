
class Elevator:

    def __init__(self, inital_state: str = "idle", name : str = "elevator") -> None:
        self._state = inital_state
        self._name = name
        self._transition_table = {
            "idle": {
                "up": {"action": self.move, "next_state": "moving"},
                "down": {"action": self.move, "next_state": "moving"},
                "default_input": {"action": self.f_null, "next_state": "idle"},
            },
            "moving":{
                "stop":{"action": self.stop, "next_state": "stopped"},
                "default_input": {"action": self.f_null, "next_state": "moving"},
            },
            "stopped":{
                "reset":{"action": self.reset, "next_state": "idle"},
                "default_input": {"action": self.f_null, "next_state": "stopped"},
            }
        }

    def __repr__(self) -> str:
        return self._name

    def command(self, input :str) -> None:
        actual_transition_table = self._transition_table[self._state]
        if input in actual_transition_table:
            action = actual_transition_table[input]["action"]
            next_state = actual_transition_table[input]["next_state"]
        else:
            action = actual_transition_table["default_input"]["action"]
            next_state = actual_transition_table["default_input"]["next_state"]
        action()
        self._state = next_state

    def f_null(self) -> None:
        pass

    def stop(self) -> None:
        print(f"{self} has stopped")

    def move(self) -> None:
        print(f"{self} is moving")

    def reset(self) -> None:
        print(f"{self} is returning to idle")

if __name__ == "__main__":
    elevator = Elevator()
    elevator.command("up")
    elevator.command("up")
    elevator.command("down")
    elevator.command("down")
    elevator.command("stop")
    elevator.command("stop")
    elevator.command("reset")