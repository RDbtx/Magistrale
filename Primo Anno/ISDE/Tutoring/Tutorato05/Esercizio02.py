def Singleton():
    #Standardized singleton buildup
    ##################
    class MetaSingleton (type):
        _instances = {}

        def __call__(cls, *args, **kwargs):
            if cls not in cls._instances:
                cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
                return cls._instances[cls]
    ###################

    class Logger(metaclass= MetaSingleton):
        def __init__(self, name: str) -> None:
            self.name = name
            print(f"logger created! = {self.name}")

        def log(self, message: str) -> None:
            print(f"[{self.name}] message recived: {message}")


    if __name__ == "__main__":
        logger = Logger("Windows")
        logger.log("ciao")


