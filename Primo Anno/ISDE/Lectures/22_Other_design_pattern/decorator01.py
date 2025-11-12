class SomeClass:

    def method_1(self) -> None:
        print("original method of some class")

class DecoratorClass:

    def __init__(self, obj) -> None:
        self.obj = obj

    def method_1(self) -> None:
        print("decorator method")

if __name__ == "__main__":
    obj = SomeClass()
    obj.method_1()

    wrapped_obj = DecoratorClass(obj)
    wrapped_obj.method_1()