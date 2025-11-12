from abc import abstractmethod, ABC


# implementation of design pattern

class Strategy(ABC):

    @abstractmethod
    def compute_price(self, price: float) -> float:
        pass

    @abstractmethod
    def get_acual_dress(self) -> None:
        pass


class NormalStrategy(Strategy):

    def compute_price(self, price: float) -> float:
        return price

    def get_acual_dress(self) -> None:
        print("Normal Dress")


class HappyHourStrategy(Strategy):

    def compute_price(self, price: float) -> float:
        discount = 0.5
        return price * discount

    def get_acual_dress(self) -> None:
        print("Happy Hour Dress")


class Customer:

    def __init__(self, name: str, strategy: Strategy) -> None:
        self.name = name
        self.bill: float = 0
        self.strategy = strategy

    def __repr__(self) -> str:
        return self.name

    def add_order(self, number: int, cost) -> None:
        self.bill += self.strategy.compute_price(cost * number)
        print(f"an order for {number} items has been added.")

    def print_bill(self) -> None:
        print(f"actual bill for {self} = {self.bill}")

    def get_acual_dress(self) -> None:
        self.strategy.get_acual_dress()

    def pay(self):
        self.bill = 0


if __name__ == "__main__":
    normalStrategy = NormalStrategy()
    happyHourStrategy = HappyHourStrategy()

    print("Welcome to our bar")
    customer1 = Customer("01", normalStrategy)
    customer1.add_order(5, 5)
    customer1.print_bill()

    print("\nHappy Hour started!")
    customer1.strategy = happyHourStrategy
    customer1.add_order(5, 5)
    customer1.print_bill()
