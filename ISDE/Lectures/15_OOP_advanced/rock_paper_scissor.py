from abc import ABC, abstractmethod

class Weapon(ABC):
    @abstractmethod
    def fight_against(self, other_weapon: "Weapon") -> str:
        pass

    def __str__(self) -> str:
        return self.__class__.__name__


class Scissor(Weapon):
    def fight_against(self, other_weapon: "Weapon") -> str:
        if type(other_weapon) is Scissor:
            return "TIE"
        if type(other_weapon) is Rock:
            return "Rock"
        if type(other_weapon) is Paper:
            return "Scissor"


class Rock(Weapon):
    def fight_against(self, other_weapon: "Weapon") -> str:
        if type(other_weapon) is Scissor:
            return "Rock"
        if type(other_weapon) is Rock:
            return "TIE"
        if type(other_weapon) is Paper:
            return "Paper"


class Paper(Weapon):
    def fight_against(self, other_weapon: "Weapon") -> str:
        if type(other_weapon) is Scissor:
            return "Scissor"
        if type(other_weapon) is Rock:
            return "Paper"
        if type(other_weapon) is Paper:
            return "Tie"


if __name__ == "__main__":
    list_of_weapons = [Scissor(), Rock(), Paper()]
    for w1 in list_of_weapons:
        print("\n")
        for w2 in list_of_weapons:
            print(f"{w1} vs {w2} = {w1.fight_against(w2)}")