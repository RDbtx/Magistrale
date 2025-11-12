class VacuumRobot:

    def __init__(self, name: str = "robot", initial_state: str = "idle") -> None:
        self.name = name
        self._state = initial_state
        self._transition_table = {
            "idle": {
                "start": {"action": self.working, "next_state": "cleaning"},
                "default_input": {"action": self.f_null, "next_state": "idle"}
            },
            "cleaning": {
                "pause": {"action": self.stop_working, "next_state": "paused"},
                "default_input": {"action": self.f_null, "next_state": "cleaning"}
            },
            "paused": {
                "dock": {"action": self.docking, "next_state": "idle"},
                "start": {"action": self.working, "next_state": "cleaning"},
                "default_input": {"action": self.f_null, "next_state": "paused"}
            }
        }

    def __repr__(self) -> str:
        return self.name

    def f_null(self) -> None:
        pass

    def working(self) -> None:
        print(f"{self} started working")

    def stop_working(self) -> None:
        print(f"{self} stopped working")

    def docking(self) -> None:
        print(f"{self} docked to recharge station")

    def process_inputs(self, input: str) -> None:
        _actual_transition_table = self._transition_table[self._state]
        if input in _actual_transition_table:
            _action = _actual_transition_table[input]["action"]
            _next_state = _actual_transition_table[input]["next_state"]
        else:
            _action = _actual_transition_table["default_input"]["action"]
            _next_state = _actual_transition_table["default_input"]["next_state"]
        _action()
        self._state = _next_state


if __name__ == "__main__":
    robot = VacuumRobot()
    robot.process_inputs("start")
    robot.process_inputs("pause")
    robot.process_inputs("start")
    robot.process_inputs("pause")
    robot.process_inputs("dock")
