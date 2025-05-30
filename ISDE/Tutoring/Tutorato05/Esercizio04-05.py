from abc import abstractmethod, ABC


class Character(ABC):

    @abstractmethod
    def move(self):
        pass


class Movementstrategy(ABC):
    @abstractmethod
    def move(self):
        pass


class MoveWalking(Movementstrategy):
    def move(self) -> str:
        return "is Walking"


class MoveFlying(Movementstrategy):
    def move(self) -> str:
        return "is Flying"


class MoveSwimming(Movementstrategy):
    def move(self) -> str:
        return "is Swimming"


class Terrain(ABC):
    @abstractmethod
    def moveonterrain(self) -> Movementstrategy:
        pass


class Ground(Terrain):
    def __init__(self):
        self.name = "Ground"

    def __repr__(self):
        return self.name

    def moveonterrain(self) -> Movementstrategy:
        return MoveWalking()


class Water(Terrain):
    def __init__(self):
        self.name = "Water"

    def __repr__(self):
        return self.name

    def moveonterrain(self) -> Movementstrategy:
        return MoveSwimming()


class Air(Terrain):
    def __init__(self):
        self.name = "Air"

    def __repr__(self):
        return self.name

    def moveonterrain(self) -> Movementstrategy:
        return MoveFlying()


class Knight(Character):
    def __init__(self, terrain : Terrain) -> None:
        self.movementstrategy = terrain.moveonterrain()
        self.name = "Knight"

    def __repr__(self):
        return self.name


    def move(self) -> str:
        return self.movementstrategy.move()


class Dragon(Character):
    def __init__(self, terrain: Terrain) -> None:
        self.movementstrategy = terrain.moveonterrain()
        self.name = "Dragon"

    def __repr__(self):
        return self.name

    def move(self) -> str:
        return self.movementstrategy.move()


if __name__ == '__main__':

    terrains = [Ground(), Water(), Air(),]

    #starting on ground
    for i in range(3):
        characters = [Knight(terrains[i]), Dragon(terrains[i])]
        print(f"{characters[0]} in {terrains[i]} {characters[0].move()}")
        print(f"{characters[1]} in {terrains[i]} {characters[1].move()}")
