class Warrior:

    def __init__(self, name: str, start_state: str = "zero") -> None:
        self._state = start_state
        self.name = name
        self._transition_table = {
            "zero": {
                "AMULET1": {"action": self.print_state, "next_state": "int_1"},
                "default_input": {"action": self.print_state, "next_state": "zero"}
            },
            "int_1": {
                "AMULET2": {"action": self.print_state, "next_state": "int_2"},
                "AMULET1": {"action": self.print_state, "next_state": "int_1"},
                "AMULET3": {"action": self.print_state, "next_state": "zero"},
                "default_input": {"action": self.print_state, "next_state": "int_1"}
            },
            "int_2": {
                "AMULET3": {"action": self.print_state, "next_state": "power"},
                "AMULET2": {"action": self.print_state, "next_state": "zero"},
                "AMULET1": {"action": self.print_state, "next_state": "zero"},
                "default_input": {"action": self.print_state, "next_state": "int_2"}
            },
            "power": {
                "AMULET3": {"action": self.print_state, "next_state": "zero"},
                "AMULET2": {"action": self.print_state, "next_state": "zero"},
                "AMULET1": {"action": self.print_state, "next_state": "zero"},
                "default_input": {"action": self.print_state, "next_state": "power"}
            }
        }

    def __repr__(self) -> str:
        return self.name

    def reset_state(self) -> None:
        self._state = "zero"

    def print_state(self) -> None:
        print(f"->{self._state} ", end="")

    def catch(self, object: str) -> None:
        actual_transition_table = self._transition_table[self._state]
        if object in actual_transition_table:
            action = actual_transition_table[object]["action"]
            next_state = actual_transition_table[object]["next_state"]
        else:
            action = actual_transition_table["default_input"]["action"]
            next_state = actual_transition_table["default_input"]["next_state"]

        self._state = next_state # firstly i move to the next state then i print the state (as requested)
        action()


if __name__ == "__main__":
    warrior = Warrior("Asgharoth")

    transition1 = ["AMULET1", "AMULET2", "X", "AMULET3", "Y"]
    transition2 = ["AMULET1", "AMULET2", "AMULET3", "AMULET3"]
    transition3 = ["AMULET1", "AMULET2", "AMULET1"]

    tests = [transition1, transition2, transition3]

    for test in tests:
        warrior.reset_state()
        print(f"tranisiton = {warrior._state} ", end ="")
        for element in test:
            warrior.catch(element)
        print("\n")
