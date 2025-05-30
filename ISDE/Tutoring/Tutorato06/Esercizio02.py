class WashingMachine:

    def __init__(self, start_state : int = 0) -> None:
        self._state = start_state

        self._transition_table = {
            0:{
                "coin":{"action":self.washing, "next_state": 1},
                "default_input":{"action":self.idle,"next_state": 0},
            },
            1:{
                "coin":{"action":self.drying, "next_state": 2},
                "default_input": {"action": self.washing, "next_state": 1},
            },
            2:{
                "open":{"action":self.idle, "next_state": 0},
                "default_input":{"action":self.drying, "next_state": 2},
            }
        }

    def idle(self):
        print("the machine is idle.")

    def washing(self):
        print("the machine is washing.")

    def drying(self):
        print("the machine is drying.")

    def process_input(self, input:str) -> None:
        actual_transition_table = self._transition_table[self._state]
        if input in actual_transition_table:
            action = actual_transition_table[input]["action"]
            next_state = actual_transition_table[input]["next_state"]
        else:
            action = actual_transition_table["default_input"]["action"]
            next_state = actual_transition_table["default_input"]["next_state"]
        action()
        self._state = next_state


    def reset_state(self) ->None:
        self.__init__()

if __name__ == "__main__":
    wm = WashingMachine()
    actions = ["open","load","coin","wait","wait",
               "machine stopped",
               "coin","wait","machine stopped",
               "open","leave"]
    for action in actions:
        wm.process_input(action)
