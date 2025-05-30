from abc import ABC, abstractmethod


class Card(ABC):

    @abstractmethod
    def fight(self, other: 'Card') -> None:
        pass

    @abstractmethod
    def fight_king(self, other: 'Card') -> str:
        pass

    @abstractmethod
    def fight_ace(self, other: 'Card') -> str:
        pass

    @abstractmethod
    def fight_queen(self, other: 'Card') -> str:
        pass


class King(Card):
    def __init__(self, name: str = "King"):
        self.name = name

    def __repr__(self) -> str:
        return self.name

    def fight(self, other: 'Card') -> None:
        print(other.fight_king(self))

    def fight_king(self, other: 'King') -> str:
        return f"{other} VS {self} == DRAW"

    def fight_queen(self, other: 'Card') -> str:
        return f"{other} VS {self} == {self} WINS"

    def fight_ace(self, other: 'Card') -> str:
        return f"{other} VS {self} == {other} WINS"

class Queen(Card):
    def __init__(self, name: str = "Queen"):
        self.name = name

    def __repr__(self) -> str:
        return self.name

    def fight(self, other: 'Card') -> None:
        print(other.fight_queen(self))

    def fight_king(self, other: 'King') -> str:
        return f"{other} VS {self} == {other} WINS"

    def fight_queen(self, other: 'Card') -> str:
        return f"{other} VS {self} == DRAW"

    def fight_ace(self, other: 'Card') -> str:
        return f"{other} VS {self} == {other} WINS"

class Ace(Card):
    def __init__(self, name: str = "Ace"):
        self.name = name

    def __repr__(self) -> str:
        return self.name

    def fight(self, other: 'Card') -> None:
        print(other.fight_queen(self))

    def fight_king(self, other: 'King') -> str:
        return f"{other} VS {self} == {self} WINS"

    def fight_queen(self, other: 'Card') -> str:
        return f"{other} VS {self} == {self} WINS"

    def fight_ace(self, other: 'Card') -> str:
        return f"{other} VS {self} == DRAW"

if __name__ == "__main__":

    cards = [King(), Queen(), Ace()]
    for card in cards:
        for card2 in cards:
            card.fight(card2)

        print("\n")

