from abc import ABC, abstractmethod


class Weapon(ABC):

    @abstractmethod
    def fight_against(self, other_weapon: "Weapon") -> str:
        pass

    @abstractmethod
    def fight_against_rock(self) -> str:
        pass

    @abstractmethod
    def fight_against_paper(self) -> str:
        pass

    @abstractmethod
    def fight_against_scissor(self) -> str:
        pass

    def __str__(self) -> str:
        return self.__class__.__name__



class Scissor(Weapon):
    def fight_against(self, other_weapon: "Weapon") -> str:
        return other_weapon.fight_against_scissor()

    def fight_against_rock(self) -> str:
        return "Rock"

    def fight_against_paper(self) -> str:
        return "Scissor"

    def fight_against_scissor(self) -> str:
        return "TIE"


class Rock(Weapon):
    def fight_against(self, other_weapon: "Weapon") -> str:
        return other_weapon.fight_against_rock()

    def fight_against_rock(self) -> str:
        return "TIE"

    def fight_against_paper(self) -> str:
        return "Paper"

    def fight_against_scissor(self) -> str:
        return "Rock"


class Paper(Weapon):
   def fight_against(self, other_weapon: "Weapon") -> str:
       return other_weapon.fight_against_paper()

   def fight_against_rock(self) -> str:
       return "Paper"
   def fight_against_paper(self) -> str:
       return "TIE"
   def fight_against_scissor(self) -> str:
       return "Scissor"


if __name__ == "__main__":
    list_of_weapons = [Scissor(), Rock(), Paper()]
    for w1 in list_of_weapons:
        print("\n")
        for w2 in list_of_weapons:
            print(f"{w1} vs {w2} = {w1.fight_against(w2)}")
