from abc import ABC, abstractmethod


class State(ABC):
    def process_input(self, context: 'CharPrinter', value: str) -> str:
        self._change_state(context, value)
        return self._action(value)

    @abstractmethod
    def _action(self, value: str) -> str:
        pass

    @abstractmethod
    def _change_state(self, context: 'CharPrinter', value: str) -> None:
        pass


class LowerCaseState(State):
    def _action(self, value: str) -> str:
        return value.lower()

    def _change_state(self, context: 'CharPrinter', value: str) -> None:
        if len(context.switch_checker) >= 3 and "".join(context.switch_checker[-3:]) == context.switch_to_upper:
            context.set_state(UpperCaseState())


class UpperCaseState(State):
    def _action(self, value: str) -> str:
        return value.upper()

    def _change_state(self, context: 'CharPrinter', value: str) -> None:
        if value == context.switch_to_lower:
            context.set_state(LowerCaseState())


class CharPrinter:
    def __init__(self, switch_to_upper: str, switch_to_lower: str) -> None:
        self._state = LowerCaseState()
        self.switch_checker = []
        self.switch_to_upper = switch_to_upper
        self.switch_to_lower = switch_to_lower

    def set_state(self, state: State) -> None:
        self._state = state

    def process_input(self, char: str) -> None:
        self._state.process_input(self, char)

    def writeChar(self, char: str) -> None:
        self.switch_checker.append(char)
        output = self._state.process_input(self, char)
        print(output, end="")


if __name__ == "__main__":
    p = CharPrinter('abc', 'x')
    sequence = ["a", "a", "b", "c", "d", "e", "f", "x", "a", "d", "b", "c", "d"]
    string = (
              "If abc \nPirus and Crips all got along \n"
              "They'd probably gun me down by the end of this song\n"
              "X"
              "Seem like the whole city go against me\n"
              "Every time I'm in the street I hear\n"
              "abc"
              "Yawk! Yawk! Yawk! Yawk!")
    for c in sequence:
        p.writeChar(c)

    print("\n")
    for c in string:
        p.writeChar(c)
