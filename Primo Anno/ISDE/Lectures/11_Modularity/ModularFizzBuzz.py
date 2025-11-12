#in this version of fizz buzz you can select if the check of fizz buzz
#is done by "is_multiple_of()" or trough "is_greater_than()"



def is_multiple_of(val, divisor):
    return val % divisor == 0

def is_greater_than(val, limiter):
    return val > limiter

def fizzbuzz(val, fizzer=3, buzzer=5, selector = 0):

    if selector == 0:
        cond_fizz = is_multiple_of(val, fizzer)
        cond_buzz = is_multiple_of(val, buzzer)
    elif selector == 1:
            cond_fizz = is_greater_than(val, fizzer)
            cond_buzz = is_greater_than(val, buzzer)
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
        selector = int(input("0- check multiplo\n1- check più grande di\n"))
        i = int(input("Inserisci un valore: "))
        fizzer = int(input("Inserisci un fizz: "))
        buzzer = int(input("Inserisci un buzz: "))
        fizzbuzz(i, fizzer, buzzer,selector)
    except ValueError:
        print("ERROR: input not valid")
    except ZeroDivisionError:
        print("ERROR: input can't be divided by zero")
    except Exception:
        print("UNKNOWN ERROR!")
