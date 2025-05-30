class SomeClass:

    def method1(self):
        print("original method01 of some class")

    def method2(self):
        print("original method02 of some class")

class Decorator:

    def __init__(self, obj):
        self._obj = obj

    def method1(self):
        print("\ndecorator operation:")
        self._obj.method1()

    def method2(self):
        print("\ndecorator operation:")
        self._obj.method2()

    def __getattr__(self, item):
        return getattr(self._obj, item)

if __name__ == "__main__":
    obj = SomeClass()
    obj.method1()

    wrapped_obj = Decorator(obj)
    wrapped_obj.method1()
    wrapped_obj.method2()