
#this is the BorgSingleton implementation

class Borg1:

    _shared_state: dict = {}

    def __init__(self, x: int) -> None:
        self.__dict__ = self._shared_state
        self.x = x


class Borg2:

    _shared_state: dict = {}

    def __new__(cls, *args, **kwargs) -> 'Borg2':
        obj = super().__new__(cls)
        obj.__dict__ = cls._shared_state
        return obj

    def __init__(self, x: int) -> None:
        self.x = x


if __name__ == '__main__':
    borg1 = Borg2(10)
    print(f"Borg1 ->{hex(id(borg1))}")

    borg2 = Borg2(20)
    print(f"Borg2 ->{hex(id(borg1))}")

    print(f"{borg1.x} {borg2.x}")
    print(f"dict address: {hex(id(borg1))} {hex(id(borg2))}")