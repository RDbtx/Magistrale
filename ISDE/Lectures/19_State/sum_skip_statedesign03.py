#full state design implementation


from abc import ABC, abstractmethod

class State(ABC):
    def process_input(self, context : 'SumSkip', value : int) -> None:
        self._action(context, value)
        self._change_state(context, value)

    @abstractmethod
    def _action(self, context, value):
        pass

    @abstractmethod
    def _change_state(self, context, value):
        pass


class StateSum(State):

    def _action(self, context : 'SumSkip', value : int) -> None:
        if value != context.value_to_skip:
            context.sum(value)

    def _change_state(self, context : 'SumSkip', value : int) -> None:
        if value == context.value_to_skip:
            context.set_state(StateSkip())

class StateSkip(State):

    def _action(self, context : 'SumSkip', value : int) -> None:
        pass

    def _change_state(self, context : 'SumSkip', value : int) -> None:
        if value != context.value_to_skip:
            context.set_state(StateSum())

class SumSkip:

    def __init__(self, value_to_skip : int) -> None:
        self._state = StateSum()
        self.sum_value = 0
        self.value_to_skip = value_to_skip

    def set_state(self, state : State) -> None:
        self._state = state

    def process_input(self, value : int) -> None:
        self._state.process_input(self, value)

    def sum(self, value : int) -> None:
        self.sum_value += value

if __name__ == "__main__":
    nums1 = [1, 13, 10, 1, 13, 13, 13, 10, 1, 13]
    nums2 = [1, 13, 10, 1, 13, 13, 13, 10, 1]
    nums3 = [13, 10, 1, 13, 13, 13, 10, 1]

    list_of_nums = [nums1, nums2, nums3]
    list_of_results = [3, 3, 2]

    for nums, r in zip(list_of_nums, list_of_results):
        s = SumSkip(13)
        for el in nums:
            s.process_input(el)
        print(s.sum_value == r)