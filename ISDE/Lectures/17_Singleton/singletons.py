from typing import Any


# Here are some Singleton implementations. The best one is the MetaclassSingleton

# without including *arg and **kwargs the init will accept only one attribute as input
def Singleton01():
    class Singleton:
        def __init__(self, x: str) -> None:
            self.x = x

        def __new__(cls, *args, **kwargs) -> 'Singleton':
            if not hasattr(cls, "_instance"):
                print("1st call")
                cls._instance = super().__new__(cls)
            else:
                print("already exists")
            return cls._instance

    if __name__ == "__main__":
        s1 = Singleton.get_instance()
        print("s1 ->", hex(id(s1)))

        s2 = Singleton.get_instance()
        print("s2 ->", hex(id(s2)))

        s3 = Singleton()


# in order to create a class that accpets multiple imputs we will write:


def SingletonArgsKwargs():
    class SingletonMulti:
        def __init__(self, x) -> 'SingletonMulti':
            if not hasattr(self, "_initialized"):
                self.x = x
                self._initialized = True

        def __new__(cls, *args, **kwargs) -> None:
            if not hasattr(cls, '_instance'):
                print("1st call")
                cls._instance = super().__new__(cls)
            else:
                print("already exists")
            return cls._instance

    if __name__ == "__main__":
        s1 = SingletonMulti.get_instance()
        print("s1 ->", hex(id(s1)))

        s2 = SingletonMulti.get_instance()
        print("s2 ->", hex(id(s2)))

        s3 = SingletonMulti

    # a more elegant approach to singletons is the metaclass approach:


def MetaclassSingleton():
    class MetaSingleton(type):

        _dict_of_instances: dict = dict()

        def __call__(cls, *args, **kwargs) -> Any:
            if cls not in cls._dict_of_instances:
                cls._dict_of_instances[cls] = super().__call__(*args, **kwargs)
            return cls._dict_of_instances[cls]

    class Singleton(metaclass=MetaSingleton):

        def __init__(self, x: str) -> None:
            self.x = x

    class SingletonSubclass(Singleton, metaclass=MetaSingleton):
        pass

    if __name__ == "__main__":
        s1 = Singleton("first value")
        print("s1 ->", hex(id(s1)))

        s2 = Singleton("second value")
        print("s2 ->", hex(id(s2)))
        print(s1.x, s2.x)

        s3 = SingletonSubclass("third value")
        print("s3 ->", hex(id(s3)))
        print(s3.x)
