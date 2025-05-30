from abc import ABC, abstractmethod

class AbstractSomeClass(ABC):

    @abstractmethod
    def method1(self):
        pass
    @abstractmethod
    def method2(self):
        pass

class SomeClass(AbstractSomeClass):

    def method1(self) -> None:
        print("original method 01 of some class")

    def method2(self) -> None:
        print("original method 02 of some class")

class BaseDecorator(AbstractSomeClass):

    def __init__(self, obj):
        self._obj = obj

    def method1(self):
        self._obj.method1()

    def method2(self):
        self._obj.method2()

class Decorator(BaseDecorator):

    def method1(self):
        print("\ndecorator operation")
        self._obj.method1()

if __name__ == "__main__":
    obj = SomeClass()
    obj.method1()

    wrapped_obj = Decorator(obj)
    wrapped_obj.method1()
    wrapped_obj.method2()