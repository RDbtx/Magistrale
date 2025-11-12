from abc import ABC, abstractmethod

#QUESTO ESERCIZIO NON HA SENSO

def implementation01():
    class Bird(ABC):

        def __init__(self, name):
            self.name = name

        @abstractmethod
        def fly(self):
            pass

    class Sparrow(Bird):

        def fly(self):
            print("can fly")

    class Penguin(Bird):

        def fly(self):
            raise ValueError("CANT FLY")


    pinguino = Penguin('Pinguino')
    rondine = Sparrow('Rondine')
    print(pinguino.name), pinguino.fly()
    print(rondine.name), rondine.fly()


#RISPETTA LA LISKOV SOBSTITUTION
def implementation02():

    class Bird(ABC):
        def __init__(self, name):
            self.name = name
        pass

    class FlyingBird(ABC):

        def __init__(self, name):
            self.name = name

        def fly(self):
            print("can fly")
            pass

    class Sparrow(FlyingBird):
        pass

    class Penguin(Bird):
        pass

    rondine = Sparrow('Rondine')
    print(rondine.name), rondine.fly()

