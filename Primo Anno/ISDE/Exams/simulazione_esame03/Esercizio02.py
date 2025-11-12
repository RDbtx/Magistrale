from typing import Dict, List, Callable
from abc import ABC, abstractmethod



class Strategy(ABC):
    @abstractmethod
    def notification_method(self, message: str) -> str:
        pass


class StrategyEmail(Strategy):
    def notification_method(self, message: str) -> str:
        return f"received a new email -> [{message}]"


class StrategyLog(Strategy):
    def notification_method(self, message: str) -> str:
        return f"new log notfication -> [{message}]"


class Subscriber:
    def __init__(self, name: str, strategy: Strategy):
        self.name = name
        self._strategy = strategy

    def __repr__(self) -> str:
        return self.name

    def update(self, message: str) -> None:
        print(f"[{self}] : {self._strategy.notification_method(message)}")


class Library:
    default_method = "update"

    def __init__(self, events: List[str], n_book: int, name: str = "library") -> None:
        self.name = name
        self.book_capacity = 500
        self.books = n_book
        self._subscribers : Dict[str: Dict[Subscriber:Callable]] = {
            event: dict() for event in events
        }
    def __repr__(self) -> str:
        return self.name

    def add_book(self, books: int):
        if books + self.books <= self.book_capacity:
            message = "a book has been added"
            self.dispatch("add book", message)
            self.books += books
        else:
            self.books = self.book_capacity

    def borrow_book(self, books: int):
        if books - self.books >= 0:
            message = "a book has been borrowed"
            self.dispatch("borrow book", message)
            self.books -= books
        else:
            self.books = 0

    def return_books(self, books: int):
        if books > self.book_capacity - self.books:
            print("the books you are trying to return are not from this library!")
        else:
            self.books += books

    def dispatch(self, event: str, message: str) -> None:
        for method_to_ivoke in self._subscribers[event].values():
            method_to_ivoke(message)

    def register(self, event: str, subscriber: Subscriber, method_to_ivoke: Callable = None) -> None:
        if method_to_ivoke is None:
            method_to_ivoke = getattr(subscriber, self.default_method)
        self._subscribers[event][subscriber] = method_to_ivoke

    def unregister(self, event: str, subscriber: Subscriber) -> None:
        if subscriber in self._subscribers[event]:
            del self._subscribers[event][subscriber]

if __name__=="__main__":

    publisher = Library(["add book","borrow book"],500)

    observer1 = Subscriber("Viola Ballas",StrategyEmail())
    observer2 = Subscriber("Riccardo",StrategyLog())

    publisher.register("add book",observer1)
    publisher.register("borrow book",observer2)

    publisher.borrow_book(10)
    publisher.borrow_book(50)
    publisher.borrow_book(50)
    publisher.add_book(15)