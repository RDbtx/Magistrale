from abc import ABC, abstractmethod


class Money(ABC):
    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def __add__(self, other):
        pass

    @abstractmethod
    def withdrawal(self, other):
        pass

    @abstractmethod
    def deposit(self, other):
        pass


class Currency(Money):
    def __init__(self, amount: float) -> None:
        self.amount = amount

    def __repr__(self):
        return f'{self.amount}$'

    def withdrawal(self, other: 'Currency') -> 'Currency':
        return Currency(self.amount + other.amount)

    def deposit(self, other: 'BankAccount') -> 'BankAccount':
        return BankAccount(self + other.money)

    def __add__(self, other: Money) -> 'Money':
        return other.withdrawal(self)


class BankAccount(Money):
    def __init__(self, money: Currency) -> None:
        self.money = money

    def __repr__(self) -> str:
        return f'bank account ={self.money}'

    def deposit(self, other: 'BankAccount') -> 'BankAccount':
        return BankAccount(self.money + other.money)

    def withdrawal(self, other: 'Currency') -> 'Currency':
        return Currency(self.money.amount + other.amount)

    def __add__(self, other):
        return other.deposit(self)


if __name__ == '__main__':
    currency = Currency(500)
    bank = BankAccount(currency)

    # This double dispatch works in the following way:
    # - if currency is added to a bank account then the program simulate as the money are being deposited into the account
    # - if the bank account money is added to real money then the program simulate a withdrawal of money from an account
    # Bank + Currency = Bank      (Deposit)
    # Currency + Bank = Currency  (Withdrawal)
    print(bank + currency)
    print(currency + bank)
    print(currency + currency)
    print(bank + bank)
