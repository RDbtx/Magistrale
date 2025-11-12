# EXERCISE 1
# STUDENT NAME RICCARDO DEIDDA
# STUDENT ID 70/90/00639



from abc import ABC, abstractmethod

class Character(ABC):

    @abstractmethod
    def __init__(self, name:str ) -> None:
        pass

    @abstractmethod
    def __repr__(self) -> str:
        pass

    @abstractmethod
    def fight_against(self, other : 'Character') -> None:
        pass

    @abstractmethod
    def fight_Wizard(self, other: 'Wizard') -> str:
        pass

    @abstractmethod
    def fight_Knight(self, other: 'Knight') -> str:
        pass

    @abstractmethod
    def fight_Dragon(self, other: 'Dragon') -> str:
        pass

class Wizard(Character):
    def __init__(self, name:str = "Wizard" ) -> None:
        self.name = name

    def __repr__(self) -> str:
        return self.name


    def fight_against(self, other: 'Character') -> None:
        print(f"{self} vs {other} = {other.fight_Wizard(self)}")

    def fight_Wizard(self, other: 'Wizard') -> str:
        return f"DRAW"

    def fight_Knight(self, other: 'Knight') -> str:
        return f"{self} WINS"

    def fight_Dragon(self, other: 'Dragon') -> str:
        return  f"{other} WINS"


class Knight(Character):
    def __init__(self, name: str = "Knight") -> None:
        self.name = name

    def __repr__(self) -> str:
        return self.name

    def fight_against(self, other: 'Character') -> None:
        print(f"{self} vs {other} = {other.fight_Knight(self)}")

    def fight_Wizard(self, other: 'Wizard') -> str:
        return f"{other} WINS"

    def fight_Knight(self, other: 'Knight') -> str:
        return f"DRAW"

    def fight_Dragon(self, other: 'Dragon') -> str:
        return f"{self} WINS"


class Dragon(Character):
    def __init__(self, name: str = "Dragon") -> None:
        self.name = name

    def __repr__(self) -> str:
        return self.name

    def fight_against(self, other: 'Character') -> None:
        print(f"{self} vs {other} = {other.fight_Dragon(self)}")

    def fight_Wizard(self, other: 'Wizard') -> str:
        return f"{self} WINS"

    def fight_Knight(self, other: 'Knight') -> str:
        return f"{other} WINS"

    def fight_Dragon(self, other: 'Dragon') -> str:
        return f"DRAW"

if __name__ =="__main__":

    characters  = [Wizard(),Knight(),Dragon()]
    for character in characters:
        for character2 in characters:
            character.fight_against(character2)
        print("\n")