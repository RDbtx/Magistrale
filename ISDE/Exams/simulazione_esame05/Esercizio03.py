from abc import ABC, abstractmethod


class Visitors(ABC):

    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        return self.name

    @abstractmethod
    def interact(self, other: 'Animal'):
        pass

    @abstractmethod
    def interact_with_lion(self, other: 'Animal'):
        pass

    @abstractmethod
    def interact_with_elephant(self, other: 'Animal'):
        pass

    @abstractmethod
    def interact_with_monkey(self, other: 'Animal'):
        pass


class Animal(ABC):
    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        return self.name

    @abstractmethod
    def interact(self, other: Visitors):
        pass

    @abstractmethod
    def interact_with_child(self, other: Visitors):
        pass

    @abstractmethod
    def interact_with_adult(self, other: Visitors):
        pass

    @abstractmethod
    def interact_with_veterinarian(self, other: Visitors):
        pass


class Child(Visitors):

    def interact(self, other: Animal):
        other.interact_with_child(self)

    def interact_with_lion(self, other: 'Animal'):
        print(f"{self} get scared of {other}")

    def interact_with_elephant(self, other: 'Animal'):
        print(f"{self} feeds {other} with peanuts")

    def interact_with_monkey(self, other: 'Animal'):
        print(f"{self} plays with {other}")


class Adult(Visitors):
    def interact(self, other: Animal):
        other.interact_with_adult(self)

    def interact_with_lion(self, other: 'Animal'):
        print(f"{self} takes photo of {other}")

    def interact_with_elephant(self, other: 'Animal'):
        print(f"{self} observe quietly the {other}")

    def interact_with_monkey(self, other: 'Animal'):
        print(f"{self} laughs  at {other}")


class Veterinarian(Visitors):
    def interact(self, other: Animal):
        other.interact_with_veterinarian(self)

    def interact_with_lion(self, other: 'Animal'):
        print(f"{self} examines {other}")

    def interact_with_elephant(self, other: 'Animal'):
        print(f"{self} examines {other}")

    def interact_with_monkey(self, other: 'Animal'):
        print(f"{self} examines {other}")


class Elephant(Animal):
    def interact(self, other: Visitors):
        other.interact_with_elephant(self)

    def interact_with_child(self, other: 'Animal'):
        print(f"{self} does tricks to impress {other}")

    def interact_with_adult(self, other: Visitors):
        print(f"{self} does tricks to impress {other}")

    def interact_with_veterinarian(self, other: Visitors):
        print(f"{self} does tricks to impress {other}")


class Monkey(Animal):
    def interact(self, other: Visitors):
        other.interact_with_monkey(self)

    def interact_with_child(self, other: Visitors):
        print(f"{self} kills the {other} that has fallen into the cage")

    def interact_with_adult(self, other: Visitors):
        print(f"{self} throws his shit to impress {other}")

    def interact_with_veterinarian(self, other: Visitors):
        print(f"{self} does tricks to impress {other}")


class Lion(Animal):
    def interact(self, other: Visitors):
        other.interact_with_lion(self)

    def interact_with_child(self, other: Visitors):
        print(f"{self} roars to scare {other}")

    def interact_with_adult(self, other: Visitors):
        print(f"{self} roars to scare {other}")

    def interact_with_veterinarian(self, other: Visitors):
        print(f"{self} roars to scare {other}")


if __name__ == "__main__":

    visitors = [Child("child"),Veterinarian("veterinarian"),Adult("adult")]
    animals = [Monkey("monkey"),Lion("lion"),Elephant("elephant")]

    for i in range(len(visitors)):
        animals[i].interact(visitors[i])
        visitors[i].interact(animals[i])
        print("\n")
