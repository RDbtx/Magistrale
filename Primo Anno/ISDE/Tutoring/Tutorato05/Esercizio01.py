from abc import ABC, abstractmethod
from plum import dispatch


def doubleDispatch():
    class Chef(ABC):
        @abstractmethod
        def __init__(self) -> None:
            pass

        @abstractmethod
        def __repr__(self) -> str:
            pass

        @abstractmethod
        def prepare_dish(self, other) -> int:
            pass

    class Dish(ABC):
        @abstractmethod
        def __init__(self) -> None:
            pass

        @abstractmethod
        def __repr__(self) -> str:
            pass

        @abstractmethod
        def italianchef(self) -> int:
            pass

        @abstractmethod
        def pastrychef(self) -> int:
            pass

        @abstractmethod
        def fusionchef(self) -> int:
            pass

    class ItalianChef(Chef):
        def __init__(self) -> None:
            self.name = "Italian Chef"

        def __repr__(self) -> str:
            return self.name

        def prepare_dish(self, other: Dish) -> int:
            return other.italianchef()

    class PastryChef(Chef):
        def __init__(self) -> None:
            self.name = "Pastry Chef"

        def __repr__(self) -> str:
            return self.name

        def prepare_dish(self, other: Dish) -> int:
            return other.pastrychef()

    class FusionChef(Chef):
        def __init__(self) -> None:
            self.name = "Fusion Chef"

        def __repr__(self) -> str:
            return self.name

        def prepare_dish(self, other: Dish) -> int:
            return other.fusionchef()

    class Pizza(Dish):
        def __init__(self, name: str) -> None:
            self.name = name

        def __repr__(self) -> str:
            return self.name

        def italianchef(self) -> int:
            return 10

        def pastrychef(self) -> int:
            return 4

        def fusionchef(self) -> int:
            return 6

    class Sushi(Dish):
        def __init__(self, name: str) -> None:
            self.name = name

        def __repr__(self) -> str:
            return self.name

        def italianchef(self) -> int:
            return 4

        def pastrychef(self) -> int:
            return 1

        def fusionchef(self) -> int:
            return 8

    class Cake(Dish):
        def __init__(self, name: str) -> None:
            self.name = name

        def __repr__(self) -> str:
            return self.name

        def italianchef(self) -> int:
            return 3

        def pastrychef(self) -> int:
            return 10

        def fusionchef(self) -> int:
            return 6

    if __name__ == "__main__":
        chefs = [ItalianChef(), PastryChef(), FusionChef()]
        menu = [Pizza("Pizza Margherita"), Cake("Torta di Mele"), Sushi("Nigiri")]

        for chef in chefs:
            print(f"\n{chef} obtained:")
            for dish in menu:
                print(f"-{chef.prepare_dish(dish)} points for {dish}")


def Overload():
    class Dish(ABC):
        @abstractmethod
        def __init__(self) -> None:
            pass

        @abstractmethod
        def __repr__(self) -> str:
            pass

    class Chef(ABC):
        @abstractmethod
        def __init__(self) -> None:
            pass

        @abstractmethod
        def __repr__(self) -> str:
            pass

        @abstractmethod
        @dispatch
        def prepare_dish(self, other: Dish) -> int:
            pass

        @abstractmethod
        @dispatch
        def prepare_dish(self, other: Dish) -> int:
            pass

        @abstractmethod
        @dispatch
        def prepare_dish(self, other: Dish) -> int:
            pass

    class Pizza(Dish):
        def __init__(self, name: str) -> None:
            self.name = name

        def __repr__(self) -> str:
            return self.name

    class Cake(Dish):
        def __init__(self, name: str) -> None:
            self.name = name

        def __repr__(self):
            return self.name

    class Sushi(Dish):
        def __init__(self, name: str) -> None:
            self.name = name

        def __repr__(self) -> str:
            return self.name

    class ItalianChef(Chef):
        def __init__(self) -> None:
            self.name = "Italian Chef"

        def __repr__(self) -> str:
            return self.name

        @dispatch
        def prepare_dish(self, other: "Pizza") -> int:
            return 10

        @dispatch
        def prepare_dish(self, other: "Cake") -> int:
            return 1

        @dispatch
        def prepare_dish(self, other: "Sushi") -> int:
            return 4

    class PastryChef(Chef):
        def __init__(self) -> None:
            self.name = "Pastry Chef"

        def __repr__(self) -> str:
            return self.name

        @dispatch
        def prepare_dish(self, other: "Pizza") -> int:
            return 4

        @dispatch
        def prepare_dish(self, other: "Cake") -> int:
            return 10

        @dispatch
        def prepare_dish(self, other: "Sushi") -> int:
            return 1

    class FusionChef(Chef):
        def __init__(self) -> None:
            self.name = "Fusion Chef"

        def __repr__(self) -> str:
            return self.name

        @dispatch
        def prepare_dish(self, other: "Pizza") -> int:
            return 6

        @dispatch
        def prepare_dish(self, other: "Cake") -> int:
            return 6

        @dispatch
        def prepare_dish(self, other: "Sushi") -> int:
            return 8

    if __name__ == "__main__":
        chefs = [ItalianChef(), PastryChef(), FusionChef()]
        menu = [Pizza("Pizza Margherita"), Cake("Torta di Mele"), Sushi("Nigiri")]

        for chef in chefs:
            print(f"\n{chef} obtained:")
            for dish in menu:
                print(f"-{chef.prepare_dish(dish)} points for {dish}")
