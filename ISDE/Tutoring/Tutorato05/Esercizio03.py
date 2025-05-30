from abc import abstractmethod, ABC

def Strategy():
    class PaymentStrategy(ABC):
        @abstractmethod
        def pay(self, payment):
            pass


    class CreditCardPayment(PaymentStrategy):
        def pay(self, amount: float) -> None:
            print(f"Paying {amount} using credit card.")


    class CashOnDeliveryPayment(PaymentStrategy):
        def pay(self, amount: float) -> None:
            print(f"Paying {amount + 5} using cash on delivery.")


    class ShoppingCart:
        def __init__(self, payment_strategy : PaymentStrategy) -> None:
            self.payment_strategy = payment_strategy
            self.items = []
            self.amount = 0

        def add_item(self, item: str, price : float) ->None:
            self.items.append(item)
            self.amount += price

        def checkout(self) ->None:
            self.payment_strategy.pay(self.amount)

    if __name__ == "__main__":

        credit_card = CreditCardPayment()
        cash = CashOnDeliveryPayment()

        cart1 = ShoppingCart(credit_card)
        cart2 = ShoppingCart(cash)

        cart2.add_item("Banana", 1)
        cart2.add_item("Banana", 1)

        cart2.checkout()