from abc import ABC, abstractmethod


class Item(ABC):
    @abstractmethod
    def equip(self, other: 'Player') -> None:
        pass

    @abstractmethod
    def use(self, other: 'Player') -> None:
        pass


class Sword(Item):
    def equip(self, other: 'Player') -> None:
        other.equip_sword(self)

    def use(self, other: 'Player') -> None:
        other.use_sword(self)


class Shield(Item):
    def equip(self, other: 'Player'):
        other.equip_shield(self)

    def use(self, other: 'Player'):
        other.use_shield(self)


class MagicStaff(Item):
    def equip(self, other: 'Player'):
        other.equip_magic(self)

    def use(self, other: 'Player'):
        other.use_magic(self)


class Player(ABC):

    @abstractmethod
    def equip_sword(self, sword: Sword) -> None:
        pass

    @abstractmethod
    def equip_shield(self, shield: Shield) -> None:
        pass

    @abstractmethod
    def equip_magic(self, magic: MagicStaff) -> None:
        pass

    @abstractmethod
    def use_sword(self, sword: Sword) -> None:
        pass

    @abstractmethod
    def use_shield(self, shield: Shield) -> None:
        pass

    @abstractmethod
    def use_magic(self, magic: MagicStaff) -> None:
        pass

    def equip(self, other: 'Item'):
        other.equip(self)

    def use(self, other: 'Item'):
        other.use(self)


class Warrior(Player):
    def __init__(self, name: str = "Warrior",
                 health: int = 100,
                 strenght: int = 5,
                 defense: int = 5,
                 magic: int = 0) -> None:
        self.name = name
        self.health = health
        self.strength = strenght
        self.defense = defense
        self.magic = magic
        self.inventory = []

    def stats(self) -> None:
        print(f"{self}:\nHEALTH = {self.health}\nSTRENGHT ={self.strength}\nDEFENSE={self.defense}\nMAGIC={self.magic}")

    def __repr__(self) -> str:
        return self.name

    def equip_sword(self, sword: Sword) -> None:
        self.inventory.append(sword)
        print(f"[{self}]:Sword added to inventory ", end="")

    def equip_shield(self, shield: Shield) -> None:
        self.inventory.append(shield)
        print(f"[{self}]:Shield added to inventory ", end="")

    def equip_magic(self, magic: MagicStaff) -> None:
        self.inventory.append(magic)
        print(f"[{self}]:Magic Staff added to inventory ", end="")

    def use_sword(self, sword: Sword) -> None:
        self.strength += 10
        print("| equipped : sword")

    def use_shield(self, shield: Shield) -> None:
        self.defense += 10
        print("| equipped : shield")

    def use_magic(self, magic: MagicStaff) -> None:
        print("| WARRIORS CANNOT USE MAGIC!")


class Rogue(Player):
    def __init__(self, name: str = "Rogue",
                 health: int = 100,
                 strenght: int = 7,
                 defense: int = 3,
                 magic: int = 0) -> None:
        self.name = name
        self.health = health
        self.strength = strenght
        self.defense = defense
        self.magic = magic
        self.inventory = []

    def stats(self) -> None:
        print(f"{self}:\nHEALTH = {self.health}\nSTRENGHT ={self.strength}\nDEFENSE={self.defense}\nMAGIC={self.magic}")

    def __repr__(self) -> str:
        return self.name

    def equip_sword(self, sword: Sword) -> None:
        self.inventory.append(sword)
        print(f"[{self}]:Sword added to inventory ", end="")

    def equip_shield(self, shield: Shield) -> None:
        self.inventory.append(shield)
        print(f"[{self}]:Shield added to inventory ", end="")

    def equip_magic(self, magic: MagicStaff) -> None:
        self.inventory.append(magic)
        print(f"[{self}]:Magic Staff added to inventory ", end="")

    def use_sword(self, sword: Sword) -> None:
        self.strength += 10
        print("| equipped : sword")

    def use_shield(self, shield: Shield) -> None:
        print("| ROGUES CANNOT USE SHIELDS!")

    def use_magic(self, magic: MagicStaff) -> None:
        print("| ROGUES CANNOT USE MAGIC!")


class Mage(Player):
    def __init__(self, name: str = "Mage",
                 health: int = 100,
                 strenght: int = 2,
                 defense: int = 2,
                 magic: int = 10) -> None:
        self.name = name
        self.health = health
        self.strength = strenght
        self.defense = defense
        self.magic = magic
        self.inventory = []

    def stats(self) -> None:
        print(f"{self}:\nHEALTH = {self.health}\nSTRENGHT ={self.strength}\nDEFENSE={self.defense}\nMAGIC={self.magic}")

    def __repr__(self) -> str:
        return self.name

    def equip_sword(self, sword: Sword) -> None:
        self.inventory.append(sword)
        print(f"[{self}]:Sword added to inventory ", end="")

    def equip_shield(self, shield: Shield) -> None:
        self.inventory.append(shield)
        print(f"[{self}]:Shield added to inventory ", end="")

    def equip_magic(self, magic: MagicStaff) -> None:
        self.inventory.append(magic)
        print(f"[{self}]:Magic Staff added to inventory ", end="")

    def use_sword(self, sword: Sword) -> None:
        print("| MAGES CANNOT USE SWORDS!")

    def use_shield(self, shield: Shield) -> None:
        print("| MAGES CANNOT USE SHIELDS!")

    def use_magic(self, magic: MagicStaff) -> None:
        self.magic += 10
        print("| equipped : magic staff")


if __name__ == "__main__":

    players = [Warrior(), Mage(), Rogue()]
    items = [Sword(), Shield(), MagicStaff()]
    for character in players:
        for item in items:
            character.equip(item)
            character.use(item)
        print("\n")
        character.stats()
        print("\n")
