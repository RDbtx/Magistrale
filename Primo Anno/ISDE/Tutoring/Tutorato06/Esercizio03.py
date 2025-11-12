from abc import ABC, abstractmethod


class TrafficLight:
    def __init__(self):
        self.state = Red()
        self.state.work()

    def change_state(self, new_state):
        self.state = new_state
        self.state.work()

    def next(self):
        self.state.next(self)

    def emergency(self):
        self.state.emergency(self)

    def pedestrian_cross(self):
        self.state.pedestrian_crossing(self)

    def low_traffic(self):
        self.change_state(BlinkingYellow())

    def reset(self):
        self.change_state(Red())



class States(ABC):
    @abstractmethod
    def next(self, traffic_light: 'TrafficLight') -> None:
        pass

    @abstractmethod
    def emergency(self, traffic_light: 'TrafficLight') -> None:
        pass

    @abstractmethod
    def pedestrian_crossing(self, traffic_light: 'TrafficLight') -> None:
        pass

    @abstractmethod
    def work(self) -> None:
        pass


class Red(States):

    def next(self, traffic_light: 'TrafficLight') -> None:
        traffic_light.change_state(Green())

    def emergency(self, traffic_light: 'TrafficLight') -> None:
        traffic_light.change_state(Red())

    def pedestrian_crossing(self, traffic_light: 'TrafficLight') -> None:
        pass

    def work(self) -> None:
        print("Red Light!")


class Green(States):

    def next(self, traffic_light: 'TrafficLight') -> None:
        traffic_light.change_state(Yellow())

    def emergency(self, traffic_light: 'TrafficLight') -> None:
        traffic_light.change_state(Red())

    def pedestrian_crossing(self, traffic_light: 'TrafficLight') -> None:
        traffic_light.change_state(Yellow())

    def work(self) -> None:
        print("Green Light!")


class Yellow(States):

    def next(self, traffic_light: 'TrafficLight') -> None:
        traffic_light.change_state(Red())

    def emergency(self, traffic_light: 'TrafficLight') -> None:
        traffic_light.change_state(Red())

    def pedestrian_crossing(self, traffic_light: 'TrafficLight') -> None:
        traffic_light.change_state(Red())

    def work(self) -> None:
        print("Yellow Light!")

class BlinkingYellow(States):

    def next(self, traffic_light: 'TrafficLight') -> None:
        traffic_light.change_state(BlinkingYellow())

    def emergency(self, traffic_light: 'TrafficLight') -> None:
        traffic_light.change_state(Red())

    def pedestrian_crossing(self, traffic_light: 'TrafficLight') -> None:
        traffic_light.change_state(Red())

    def work(self) -> None:
        print("Blinking Yellow!")


if __name__ == '__main__':
    traffic_light = TrafficLight()
    traffic_light.next()
    traffic_light.next()
    traffic_light.pedestrian_cross()
    traffic_light.next()
    traffic_light.emergency()
    traffic_light.low_traffic()
    traffic_light.reset()