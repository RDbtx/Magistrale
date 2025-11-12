# Exercise 1:
# Consider the following objects and their operations MyList , MyNumber:
# MyList + MyList -> MyList
# if the lists have the same lenght, the output is a list containing the sum
# of the elements of the two list, otherwise an empty list is returned.
# MyNumber + MyNumber -> MyNumber | MyList + MyNumber -> MyList | MyNumber + MyList -> MyList
# Implement MyList and MyNumber using Composition. Implement __add__() using Double Dispatch.

from abc import ABC, abstractmethod


class MyElement(ABC):

    @abstractmethod
    def add_number(self, other: 'MyNumber') -> 'MyElement':
        pass

    @abstractmethod
    def add_list(self, other: 'MyList') -> 'MyList':
        pass

    @abstractmethod
    def __add__(self, other: 'MyElement') -> 'MyElement':
        pass


class MyList(MyElement):

    # implemented composition by composing MyList with elements from MyNumber class
    def __init__(self, lista: list['MyNumber']) -> None:
        self.list = lista

    def __repr__(self) -> str:
        return str(self.list)

    def add_number(self, other: 'MyNumber') -> 'MyList':
        new_list = []
        for elem in self.list:
            new_list.append(elem + other)
        return MyList(new_list)

    def add_list(self, other: 'MyList') -> 'MyList':
        new_list = []
        if len(self.list) != len(other.list):
            return MyList(new_list)
        else:
            for index in range(len(self.list)):
                new_list.append(self.list[index] + other.list[index])

    def __add__(self, other: MyElement) -> 'MyList':
        return other.add_list(self)


class MyNumber(MyElement):
    def __init__(self, number: int) -> None:
        self.number = number

    def __repr__(self) -> str:
        return str(self.number)

    def add_number(self, other: 'MyNumber') -> 'MyNumber':
        return MyNumber(self.number + other.number)

    def add_list(self, other: 'MyList') -> 'MyList':
        new_list = []
        for elem in other.list:
            new_list.append(elem + self)
        return MyList(new_list)

    def __add__(self, other: 'MyNumber') -> 'MyNumber':
        return other.add_number(self)


if __name__ == "__main__":
    values = [MyNumber(5), MyNumber(5),
              MyList([MyNumber(1),
                      MyNumber(2),
                      MyNumber(3),
                      MyNumber(4)]),
              MyList([MyNumber(4),
                      MyNumber(3),
                      MyNumber(2),
                      MyNumber(1)]),
              MyList([MyNumber(4),
                      MyNumber(3),
                      MyNumber(5)])]

    for item in values:
        print("\n")
        for sub_item in values:
            print(f"{item} + {sub_item} = {item + sub_item}")
