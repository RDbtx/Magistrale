class Logger:
    def __new__(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
            cls.messages = []

            # flush the file
            with open("data.txt", "w") as f:
                f.write("")

        return cls._instance

    def log(self, message):
        self.messages.append(message)

    def write_log(self):
        with open("data.txt", 'w') as f:
            f.write("".join(self.messages))

if __name__ == "__main__":

    def f0():
        l = Logger()
        l.write_log()
        print('action 0')


    def f1():
        l = Logger()
        l.log("I am the function f1\n")
        print('action 1')


    def f2():
        l = Logger()
        l.log("I am the function f2\n")
        print('action 2')


    def f3():
        l = Logger()
        l.log("I am the function f3\n")
        print('action 3')


    actions = [f0, f1, f2, f3]

    while True:
        command = int(input())
        print('enter a number (0-3); 0 to exit')
        actions[command]()

        # modify the main so that it ends with f0
        if command == 0:
            break

    print("content of data.txt: ")
    with open("data.txt", "r") as f:
        print(f.read())