from abc import ABC, abstractmethod



# L'interfaccia è una guida su come dev essere strutturata la classe

class Character(ABC):

    @abstractmethod
    def __init__(self, name):
        pass
    @abstractmethod
    def jum(self):
        pass
