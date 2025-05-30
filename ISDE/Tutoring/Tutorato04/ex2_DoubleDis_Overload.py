from abc import abstractmethod,ABC
from plum import dispatch

def doubledispatch():
    class Hero(ABC):
        @abstractmethod
        def __init__(self) -> None:
            pass

        @abstractmethod
        def __repr__(self) ->str:
            pass

        @abstractmethod
        def fight(self, other) -> int:
            pass

    class Monster(ABC):

        @abstractmethod
        def __init__(self) -> None:
            pass

        @abstractmethod
        def __repr__(self) ->str:
            pass

        @abstractmethod
        def fight_dwarf(self) -> int:
            pass

        @abstractmethod
        def fight_human(self) -> int:
            pass

        @abstractmethod
        def fight_elf(self) -> int:
            pass

    class Dwarf(Hero):
        def __init__(self, name:str) -> None:
            self.name = name

        def __repr__(self) ->str:
            return self.name

        def fight(self, other: Monster) -> int:
            return other.fight_dwarf()

    class Elf(Hero):
        def __init__(self, name:str) -> None:
            self.name = name

        def __repr__(self) ->str:
            return self.name

        def fight(self, other: Monster) -> int:
            return other.fight_elf()

    class Human(Hero):
        def __init__(self, name:str) -> None:
            self.name = name

        def __repr__(self) ->str:
            return self.name

        def fight(self, other: Monster) -> int:
            return other.fight_human()

    class Giant(Monster):
        def __init__(self, name:str) -> None:
            self.name = name

        def __repr__(self) ->str:
            return self.name

        def fight_dwarf(self) ->int:
            return 6

        def fight_human(self) ->int:
            return 3

        def fight_elf(self) ->int:
            return 1

    class Bat(Monster):
        def __init__(self, name:str) -> None:
            self.name = name

        def __repr__(self) ->str:
            return self.name

        def fight_dwarf(self) -> int:
            return 0

        def fight_human(self) -> int:
            return 3

        def fight_elf(self) -> int:
            return 0


    class Troll(Monster):
        def __init__(self, name: str) -> None:
            self.name = name

        def __repr__(self) -> str:
            return self.name

        def fight_dwarf(self) -> int:
            return 6

        def fight_human(self) -> int:
            return 3

        def fight_elf(self) -> int:
            return 3


    if __name__ == '__main__':
        heroes = [Dwarf("nano"),Elf("elfo"),Human("umano")]
        monsters = [Troll("troll"),Giant("gigante"),Bat("pipistrello")]

        for hero in heroes:
            for monster in monsters:
                print(f"{hero} deals [{hero.fight(monster)}] damage to {monster}")


def overload():
    class Hero(ABC):
        @abstractmethod
        def __init__(self) -> None:
            pass

        @abstractmethod
        def __repr__(self) ->str:
            pass

        @abstractmethod
        def fight(self, other) -> int:
            pass

    class Monster(ABC):
        @abstractmethod
        def __init__(self) -> None:
            pass

        @abstractmethod
        def __repr__(self) -> str:
            pass
        pass

    class Dwarf(Hero):
        def __init__(self, name:str) -> None:
            self.name = name

        def __repr__(self) ->str:
            return self.name

        @dispatch
        def fight(self, other:"Giant") -> int:
            return 6

        @dispatch
        def fight(self, other: "Troll") -> int:
            return 6

        @dispatch
        def fight(self, other: "Bat") -> int:
            return 0


    class Elf(Hero):
        def __init__(self, name: str) -> None:
            self.name = name

        def __repr__(self) -> str:
            return self.name

        @dispatch
        def fight(self, other: "Giant") -> int:
            return 1

        @dispatch
        def fight(self, other: "Troll") -> int:
            return 3

        @dispatch
        def fight(self, other: "Bat") -> int:
            return 0


    class Human(Hero):
        def __init__(self, name: str) -> None:
            self.name = name

        def __repr__(self) -> str:
            return self.name

        @dispatch
        def fight(self, other: "Giant") -> int:
            return 3

        @dispatch
        def fight(self, other: "Troll") -> int:
            return 3

        @dispatch
        def fight(self, other: "Bat") -> int:
            return 3

    class Troll(Monster):
        def __init__(self, name: str) -> None:
            self.name = name

        def __repr__(self) -> str:
            return self.name

    class Giant(Monster):
        def __init__(self, name: str) -> None:
            self.name = name

        def __repr__(self) -> str:
            return self.name

    class Bat(Monster):
        def __init__(self, name: str) -> None:
            self.name = name

        def __repr__(self) -> str:
            return self.name


    if __name__ == "__main__":
        heroes = [Dwarf("nano"), Elf("elfo"), Human("umano")]
        monsters = [Troll("troll"), Giant("gigante"), Bat("pipistrello")]

        for hero in heroes:
            for monster in monsters:
                print(f"{hero} deals [{hero.fight(monster)}] damage to {monster}")