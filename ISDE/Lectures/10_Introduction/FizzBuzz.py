def is_multiple_of(val, divisor):
    return val % divisor == 0


def fizzbuzz(val, fizzer=3, buzzer=5):
    cond_fizz = is_multiple_of(val, fizzer)
    cond_buzz = is_multiple_of(val, buzzer)

    if (cond_buzz and cond_fizz):
        print(str(val) + " FizzBuzz")
    elif (cond_fizz):
        print(str(val) + " Fizz")
    elif (cond_buzz):
        print(str(val) + " Buzz")
    else:
        print(str(val) + " NorFizzNorBuzz")


while True:
    try:
        i = int(input("Inserisci un valore: "))
        fizzer = int(input("Inserisci un fizz: "))
        buzzer = int(input("Inserisci un buzz: "))
        fizzbuzz(i, fizzer, buzzer)
    except ValueError:
        print("ERROR: input not valid")
    except ZeroDivisionError:
        print("ERROR: input can't be divided by zero")
    except Exception:
        print("UNKNOWN ERROR!")
