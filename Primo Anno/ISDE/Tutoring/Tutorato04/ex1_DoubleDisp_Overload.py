from abc import abstractmethod,ABC
from plum import dispatch

def doubleDispatch():
    # double dispatch

    class MathEntity(ABC):

        @abstractmethod
        def __init__(self) -> None:
            pass

        @abstractmethod
        def __repr__(self) -> str:
            pass

        @abstractmethod
        def __add__(self, other: "MathEntity") -> "MathEntity":
            pass

        @abstractmethod
        def _add_real(self, other: "R") -> "MathEntity":
            pass

        @abstractmethod
        def _add_complex(self, other: "C") -> "C":
            pass

    class R(MathEntity):

        def __init__(self, re: float) -> None:
            self.re = re

        def __repr__(self) -> str:
            return str(self.re)

        def __add__(self, other: "MathEntity") -> "MathEntity":
            return other._add_real(self)

        def _add_real(self, other: "R") -> "R":
            return R(self.re + other.re)

        def _add_complex(self, other: "C") -> "C":
            return C(self.re + other.re, other.img)

    class C(MathEntity):

        def __init__(self, re: float, img=0) -> None:
            self.re = re
            self.img = img

        def __repr__(self) -> str:
            s_sign = ["-", "+"][self.img > 0]
            s_img = "" if self.img == 0 else f"{s_sign}{abs(self.img)}i"
            return f"{self.re}{s_img}"

        def __add__(self, other: "MathEntity") -> "MathEntity":
            return other._add_complex(self)

        def _add_real(self, other: "R") -> "C":
            return C(self.re + other.re, self.img)

        def _add_complex(self, other: "C") -> "C":
            return C(self.re + other.re, self.img + other.img)

    if __name__ == "__main__":
        values = [R(2), R(-3), C(2, 3), C(3, -3)]
        for value1 in values:
            print("\n")
            for value2 in values:
                print(f"{value1} + {value2} = {value1 + value2}")

def Overload():
    class MathEntity2(ABC):
        @abstractmethod
        def __init__(self) -> None:
            pass

        @abstractmethod
        @dispatch
        def __add__(self, other: "R2") -> "MathEntity2":
            pass

        @abstractmethod
        @dispatch
        def __add__(self, other: "C2") -> "C2":
            pass

    class R2(MathEntity2):
        def __init__(self, re: float) -> None:
            self.re = re

        def __repr__(self) -> str:
            return str(self.re)

        @dispatch
        def __add__(self, other: "C2") -> "C2":
            return C2(self.re + other.re, other.img)

        @dispatch
        def __add__(self, other: "R2") -> "R2":
            return R2(self.re + other.re)

    class C2(MathEntity2):
        def __init__(self, re: float, img=0) -> None:
            self.re = re
            self.img = img

        def __repr__(self) -> str:
            sign = "-" if self.img > 0 else "+"
            img = '' if self.img == 0 else f"{sign}{abs(self.img)}i"
            return f"{self.re}{img}"

        @dispatch
        def __add__(self, other: "C2") -> "C2":
            return C2(self.re + other.re, self.img)

        @dispatch
        def __add__(self, other: "R2") -> "C2":
            return C2(self.re + other.re, self.img)

    if __name__ == "__main__":
        values = [R2(2), R2(-3), C2(2, 3), C2(3, -3)]
        for op1 in values:
            for op2 in values:
                print(op1, "+", op2, "=", op1 + op2)
