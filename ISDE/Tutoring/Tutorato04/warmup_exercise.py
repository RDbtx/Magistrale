from abc import ABC, abstractmethod

def exercise1():
    class Appliance(ABC):
        def __init__(self, brand: str) -> None:
            self._brand = brand
            self._power_state = False

        @property
        def name(self) -> str:
            return type(self).__name__

        @property
        def brand(self) -> str:
            return self._brand

        @brand.setter
        def brand(self, value: str) -> None:
            if not value.strip():
                raise ValueError("Brand name cannot be empty.")
            self._brand = value

        @property
        def power_state(self) -> bool:
            return self._power_state

        @power_state.setter
        def power_state(self, value: bool) -> None:
            if not isinstance(value, bool):
                raise ValueError("Power state must be a boolean.")
            self._power_state = value

        def turn_on(self) -> None:
            self._power_state = True
            print(f"{self._brand} {self.name} is now ON.")

        def turn_off(self) -> None:
            self._power_state = False
            print(f"{self._brand} {self.name} is now OFF.")

    class WashingMachine(Appliance):
        def __init__(self, brand: str, capacity: int) -> None:
            super().__init__(brand)
            self._capacity = capacity

        @property
        def capacity(self) -> int:
            return self._capacity

        @capacity.setter
        def capacity(self, value: int) -> None:
            if value <= 0:
                raise ValueError("Capacity must be greater than zero.")
            self._capacity = value

        def start_wash(self) -> None:
            if (self.power_state):
                print(f"{self.brand} {self.name} started washing.")
            else:
                raise ValueError(f"Washing can not be started {self.name} is OFF.")

    if __name__ == "__main__":
        Electrolux = WashingMachine("Electrolux", 100)
        Electrolux.turn_on()

        try:
            Electrolux.turn_off()
            Electrolux.start_wash()
        except ValueError as e:
            print(e)


def exercise2():
    # Liskov substitution principle
    class Shape(ABC):
        @abstractmethod
        def area(self) -> float:
            pass

        @property
        def name(self) -> str:
            return type(self).__name__

    class Rectangle(Shape):
        def __init__(self, width: float, height: float) -> None:
            self._width = width
            self._height = height

        @property
        def width(self) -> float:
            return self._width

        @width.setter
        def width(self, value: float) -> None:
            if value <= 0:
                raise ValueError("Width must be greater than zero.")
            self._width = value

        @property
        def height(self) -> float:
            return self._height

        @height.setter
        def height(self, value: float) -> None:
            if value <= 0:
                raise ValueError("Height must be greater than zero.")
            self._height = value

        def area(self) -> float:
            return self._width * self._height

    class Square(Rectangle):
        def __init__(self, side: float) -> None:
            super().__init__(side, side)

        @property
        def side(self) -> float:
            return self._width

        @side.setter
        def side(self, value: float) -> None:
            if value <= 0:
                raise ValueError("Side must be greater than zero.")
            self._width = self._height = value

    if __name__ == "__main__":
        r = Rectangle(10, 15)
        s = Square(10)
        print(f"{r.name} area is [{r.area()}]")
        print(f"{s.name} area is [{s.area()}]")


def exercise3():
    # compostion
    class Animal(ABC):
        @property
        def name(self) -> str:
            return type(self).__name__

        def do(self) -> str:
            pass

    class Dog(Animal):

        def do(self) -> str:
            return "Bark"

    class Lion(Animal):
        def do(self) -> str:
            return "Roar"

    class GOAT(Animal):
        def do(self) -> str:
            goat_says = (
                "I remember you was conflicted Misusing your influence "
                "Sometimes I did the same Abusing my power, full of resentment "
                "Resentment that turned into a deep depression "
                "Found myself screaming in the hotel room "
                "I didn't wanna self-destruct "
                "The evils of Lucy was all around me "
                "So I went running for answers"
            )
            return goat_says

    class Zoo:
        def __init__(self) -> None:
            self.animals = []

        def add_animal(self, animals: Animal) -> None:
            self.animals.append(animals)
            print(f"{animals.name} has been added to the zoo's collection.")

    if __name__ == "__main__":
        zoo = Zoo()

        zoo.add_animal(Dog())
        zoo.add_animal(Lion())
        zoo.add_animal(GOAT())

        print("\n\nWelcome to the Zoo:")
        print("here are our animals!")
        for animal in zoo.animals:
            print(f"\n{animal.name}")
            print(f"what does this animal do?\nOH LOOK IT'S SAYING SOMETHING: [{animal.do()}]")

