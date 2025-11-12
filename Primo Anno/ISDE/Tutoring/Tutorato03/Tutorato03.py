from matplotlib import pyplot as plt


def ex1_tutorato3():
    word_frequencies = {"Python": 25, "Java": 15, "C++": 10, "JavaScript": 30, "Ruby": 8, "Swift": 12, "Go": 18,
                        "Kotlin": 14, "R": 7, "MATLAB": 10}

    keys = list(word_frequencies.keys())
    words = list(word_frequencies.values())

    for val in words:
        if type(val) != int:
            raise TypeError("VALUE OF FREQUENCIES SHOULD BE INTEGER!")

    plt.bar(keys, words, color="orange")
    plt.title("Most used languages")
    plt.xlabel("Languages")
    plt.xticks(rotation=30)
    plt.grid(axis="y")
    plt.ylabel("Frequency")
    plt.show()


def ex2_tutorato3():
    class Person:
        def __init__(self, name, surname):
            self.name = name
            self.surname = surname

        def move_to_target(self, target):
            print(f"{self.name} {self.surname} is moving to {target}!")

    gianni = Person("Gianni", "Sperti")
    Luca = Person("Luca", "Big")
    gianni.move_to_target(f"{Luca.surname} {Luca.name}")


def ex3_tutorato3():
    class Library:
        library_count = 0

        def __init__(self):
            self.books = []
            Library.library_count = Library.library_count + 1

        def is_valid(self, input):
            counter = 0
            for k, v in input.items():
                if type(v) != str and type(k) != str:
                    raise TypeError("AUTHOR AND TILE SHOULD BE STRINGS!")
                elif k != "titolo" and k != "autore":
                    raise ValueError("KEY ARGUMENTS SHOULD BE titolo OR autore!")
                counter = counter + 1
            if counter > 2:
                raise ValueError("TOO MANY ARGUMENTS")

        def add_book(self, input):
            self.is_valid(input)
            self.books.append(input)
            print(f"Libro aggiunto:\nTITOLO = {input['titolo']}\nAUTORE = {input['autore']}\n")

        @classmethod
        def get_library_count(cls):
            return cls.library_count

    libreria1 = Library()
    libreria2 = Library()
    libreria3 = Library()
    libreria1.add_book({"titolo": "Python", "autore": "Gianni Sperti"})
    libreria2.add_book({"titolo": "Java", "autore": "Big Luca"})

    print(f"NUMERO DI LIBRERIE ESISTENTI = {Library.get_library_count()}")


def ex4_tutorato3():
    class Vehicle:
        def __init__(self, currenV, MAXV=200):
            self.current_speed = currenV
            self.max_speed = MAXV

        def set_speed(self, speed):
            if speed > self.max_speed:
                raise ValueError("CURRENT SPEEDS EXCEED MAX SPEED!")
            else:
                self.current_speed = speed

    class Bus(Vehicle):
        def __init__(self, occupied_seats, MAX_CAP, current_speed, MAXV=200, ):
            self.max_capacity = MAX_CAP
            self.occupied_seats = occupied_seats
            super().__init__(current_speed, MAXV)

        def add_passengers(self, persons):
            if self.occupied_seats + persons > self.max_capacity:
                raise ValueError(f"Occupants exceed max capacity! "
                                 f"only {self.occupied_seats + persons - self.max_capacity} "
                                 f"person can enter!")
            else:
                self.occupied_seats += persons

    ARST = Bus(10, 100, 30, 50)
    ARST.set_speed(50)
    ARST.add_passengers(91)
    try:
        ARST.set_speed(250)
    except:
        print("LOWER YOUR SPEED")



