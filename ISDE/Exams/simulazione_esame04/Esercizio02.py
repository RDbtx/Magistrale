from typing import Dict, List, Callable


class Subscriber:
    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        return self.name

    def graphical_display(self, message: str) -> None:
        print(f"[{self}] (Graphical Interface) : {message}")

    def console_logger(self, message: str) -> None:
        print(f"[{self}] (console message) : {message}")

    def file_logger(self, message: str) -> None:
        print(f"[{self}] (file message) : {message}")


class WeatherMonitoringStation:
    default_method = "graphical_display"

    def __init__(self, events: List[str], weather_data: List[int]) -> None:
        self.temperature = weather_data[0]
        self.pressure = weather_data[1]
        self.humidity = weather_data[2]
        self._subscribers: Dict[str: Dict[Subscriber, Callable]] = {
            event: dict() for event in events
        }

    def update_data(self, temperature: int, humidity: int, pressure: int) -> None:
        self.pressure = pressure
        self.temperature = temperature
        self.humidity = humidity

        message = f"TEMPERATURE: {temperature}° | HUMIDITY: {humidity}% | PRESSURE: {pressure}Pa"
        self.dispatch("update", message)

    def dispatch(self, event: str, message: str) -> None:
        for method_to_ivoke in self._subscribers[event].values():
            method_to_ivoke(message)

    def register_subscriber(self, event: str, subscriber: Subscriber, method_to_invoke: Callable = None) -> None:
        if method_to_invoke is None:
            method_to_invoke = getattr(subscriber, self.default_method)
        self._subscribers[event][subscriber] = method_to_invoke

    def unregister(self, event:str, subscriber:Subscriber) -> None:
        if subscriber in self._subscribers[event]:
            del self._subscribers[event][subscriber]

if __name__ == "__main__":

    weather_data = WeatherMonitoringStation(["update"],[20,80,7])
    observer1 = Subscriber("observer1")
    observer2 = Subscriber("observer2")
    observer3 = Subscriber("observer3")

    weather_data.register_subscriber("update", observer1)
    weather_data.register_subscriber("update", observer2,observer2.file_logger)
    weather_data.register_subscriber("update", observer3,observer3.console_logger)

    weather_data.update_data(30,50,15)