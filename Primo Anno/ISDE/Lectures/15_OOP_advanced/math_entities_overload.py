from abc import ABC, abstractmethod
from plum import dispatch


class MathEntity(ABC):

    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def __repr__(self) -> str:
        pass

    @abstractmethod
    @dispatch
    def __add__(self, other: "R") -> "MathEntity":
        pass

    @abstractmethod
    @dispatch
    def __add__(self, other: "C") -> "C":
        pass


class R(MathEntity):
    def __init__(self, re: float) -> None:
        self.re = re

    def __repr__(self) -> str:
        return str(self.re)

    @dispatch
    def __add__(self, other: "R") -> "MathEntity":
        return R(self.re + other.re)

    @dispatch
    def __add__(self, other: "C") -> "C":
        return C(self.re + other.re, other.img)


class C(MathEntity):
    def __init__(self, re: float, img=0) -> None:
        self.re = re
        self.img = img

    def __repr__(self) -> str:
        s_sign = ["-", "+"][self.img > 0]
        s_img = "" if self.img == 0 else f"{s_sign}i{abs(self.img)}"
        return f"{self.re}{s_img}"

    @dispatch
    def __add__(self, other: "R") -> "MathEntity":
        return C(self.re + other.re, self.img)

    @dispatch
    def __add__(self, other: "C") -> "C":
        return C(self.re + other.re, self.img + other.img)


if __name__ == "__main__":
    values = [R(2), R(-3), C(2, 3), C(3, -3)]
    for value1 in values:
        print("\n")
        for value2 in values:
            print(f"{value1} + {value2} = {value1 + value2}")
