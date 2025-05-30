from abc import ABC, abstractmethod


class Character(ABC):

    def __init__(self, name):
        self.name = name

    @abstractmethod
    def jump(self):
        pass


class Mouse(Character):

    def jump(self):
        super().jump()
        print("Tiny Jump!")


class Kangaroo(Character):

    def jump(self):
        super().jump()
        print("Big Jump!")


topo = Mouse("Topo")
canguro = Kangaroo("Canguro")
print(f"\n{topo.name} esegue = "), topo.jump()
print(f"\n{canguro.name} esegue = "), canguro.jump()
