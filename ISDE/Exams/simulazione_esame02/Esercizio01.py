class Robot:
    def __init__(self, name: str = "Robot", initial_state: str = "start"):
        self.name = name
        self._state = initial_state
        self.battery = 100
        self._transition_table = {
            "start": {
                "default_input": {"action": self.f_about, "next_state": "target"},
                "obstacle": {"action": self.f_about, "next_state": "obstacle"},
                "power_low": {"action": self.battery_alert, "next_state": "charging"}
            },
            "target": {
                "default_input": {"action": self.f_about, "next_state": "start"},
                "obstacle": {"action": self.f_about, "next_state": "obstacle"},
                "power_low": {"action": self.battery_alert, "next_state": "charging"}
            },
            "obstacle": {
                "default_input": {"action": self.f_about, "next_state": "start"},
                "obstacle": {"action": self.f_about, "next_state": "obstacle"},
                "power_low": {"action": self.battery_alert, "next_state": "charging"}
                         },
            "charging": {
                "full_power": {"action": self.f_about, "next_state": "start"},
                "default_input": {"action": self.battery_charging, "next_state": "charging"},
            }}

    def __repr__(self) -> str:
        return self.name

    def f_about(self) -> None:
        print(f"[{self} : STATE = {self._state} : BATTERY LEVEL = {self.battery}]")

    def battery_alert(self) -> None:
        self.f_about()
        print("BATTERY LEVEL IS LOW!!")

    def battery_charging(self) -> None:
        self.battery += 20
        self.f_about()

    def move(self, input : "str") -> None:
        # these if statements are needed to coordinate battery levels and robot's actions since battery level
        # is my interpretation of the problem and it's not actually required.
        if self._state == "charging" and self.battery == 100:
            input = "full_power"
        if self._state != "charging":
            self.battery -= 20
        if self.battery < 20 and self._state != "charging":
            input = "power_low"
        actual_transition_table = self._transition_table[self._state]
        if input in actual_transition_table:
            action = actual_transition_table[input]["action"]
            next_state = actual_transition_table[input]["next_state"]
        else:
            action = actual_transition_table["default_input"]["action"]
            next_state = actual_transition_table["default_input"]["next_state"]
        self._state = next_state
        action()

if __name__ == "__main__":

    robot = Robot()
    robot.move("start")
    robot.move("target")
    robot.move("obstacle")
    robot.move("charging")
    robot.move("charging")
    robot.move("charging")
    robot.move("ciao")
    robot.move("bella")
    robot.move("o it")
    robot.move("charging")
    robot.move("bella")