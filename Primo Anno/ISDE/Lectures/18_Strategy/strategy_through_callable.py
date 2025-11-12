from typing import Callable


def dress_normal_strategy() -> None:
    print("Normal Dress")


def dress_happy_hour_strategy() -> None:
    print("Happy Hour Dress")


def compute_price_normal_strategy(cost: float) -> float:
    return cost


def compute_price_happy_hour_strategy(cost: float) -> float:
    discount = 0.5
    return cost * discount


class Customer:

    def __init__(self,
                 name: str,
                 strategy_price: Callable,
                 strategy_dress: Callable
                 ) -> None:
        self.bill: float = 0
        self.name = name
        self.compute_price = strategy_price
        self.compute_dress = strategy_dress

    def __repr__(self) -> str:
        return self.name

    def add_order(self, number: int, unit_cost: float) -> None:
        self.bill += self.compute_price(number * unit_cost)
        print(f"An order of {number} items for customer {self} has been added!")

    def print_bill(self) -> None:
        print(f"current bill of customer {self} = {self.bill}")

    def pay(self) -> None:
        print(f"a bill of {self.bill} has been payed")
        self.bill = 0


if __name__ == '__main__':



    customer = Customer("01", compute_price_normal_strategy, dress_normal_strategy)
    customer.add_order(5, 5)
    customer.compute_dress()
    customer.print_bill()

    customer.compute_price = compute_price_happy_hour_strategy
    customer.compute_dress = dress_happy_hour_strategy
    customer.add_order(5, 5)
    customer.print_bill()

    customer.pay()