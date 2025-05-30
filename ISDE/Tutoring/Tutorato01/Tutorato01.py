def ex1_tutorato1():
    print("EX1:")
    numbers = [1, 2, 3, 4, 5]
    print(numbers[0], numbers[len(numbers) - 1])
    numbers.append(6)
    numbers.remove(numbers[2])
    print(numbers)


def ex2_tutorato1():
    print("EX2:")
    fruits = ['apple', 'banana', 'cherry', 'date', 'elderberry']
    print(fruits[0:3])
    vegetables = ['potato', 'aubergine', 'eggplant']
    fruits.extend(vegetables)
    print(fruits)


def ex3_tutorato1():
    print("EX3:")
    student = {'name': 'Riccardo', 'age': 23, 'grade': 25};
    print(student)
    student.update({'grade': 30})
    print(student['grade'])


def ex4_tutorato1():
    print("EX4:")
    number = int(input("insert number:"))
    if (number % 2 == 0):

        print(str(number) + " is even")
    else:
        print(str(number) + " is odd")


def ex5_tutorato1():
    print("EX5:")
    list_of_int = [1, 2, 3, 4, 5]
    sum = 0
    for i in list_of_int:
        sum = sum + i
    print(sum)


def ex6_tutorato1():
    print("EX6:")
    list_of_int = [1, 2, 3, 4, 5]
    string = " "
    for i in list_of_int:
        string = string + str(i)
    print(string)


def ex7_tutorato1():
    def subtract_one(value):
        return value - 1

    def subtract_one_to_list(list):
        for i in range(len(list)):
            list[i] = subtract_one(list[i])
        return list

    def subtract_one_to_all(dictionary):
        for k, v in dictionary.items():
            v = subtract_one_to_list(v)
        return dictionary

    dictionary = {'A': [1, 2, 3, 4, 5],
                  'B': [10, 20, 30, 40, 50],
                  'C': [22, 23, 24, 25, 10]}
    subtract_one_to_all(dictionary)
    print(dictionary)


def ex8_tutorato1():
    def somma(val1, val2):
        return val1 + val2

    def prodotto(val1, val2):
        return val1 * val2

    def divisione(val1, val2):
        return val1 / val2

    def sottrazione(val1, val2):
        return val1 / val2

    valore1 = int(input("insert numero 1: "))
    valore2 = int(input("insert numero 2: "))

    print(str(valore1) + " + " + str(valore2) + " = " + str(somma(valore1, valore2)))
    print(str(valore1) + " * " + str(valore2) + " = " + str(prodotto(valore1, valore2)))
    print(str(valore1) + " / " + str(valore2) + " = " + str(divisione(valore1, valore2)))
    print(str(valore1) + " - " + str(valore2) + " = " + str(sottrazione(valore1, valore2)))
