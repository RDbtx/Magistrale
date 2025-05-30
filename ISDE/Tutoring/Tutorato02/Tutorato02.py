from copyreg import pickle
import numpy as np
import pickle
from matplotlib import pyplot as plt


def ex1_tutorato2():
    def add_expenses(expenses, values):
        for i in values:
            expenses.append(i)

    def total_expenses(list):
        sum = 0
        for i in list:
            sum += i
        return sum

    def average_expenses(list):
        sum = total_expenses(list)
        media = sum / len(list)
        return media

    expenses = [150, 20, 200, 10, 250]
    add_expenses(expenses, [50, 20, 30])
    print("SPESE =", expenses)
    print("SPESA TOTALE =", total_expenses(expenses))
    print("SPESA MEDIA =", average_expenses(expenses))


def ex2_tutorato2():
    expenses = np.random.rand(12)
    months = ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", "Luglio", "Agosto",
              "Settembre", "Ottobre", "Novembre", "Dicembre"]
    plt.bar(months, expenses, color="skyblue")
    x = plt.xlabel("Mesi")
    y = plt.ylabel("Spese")
    plt.title("Spese Mensili")
    plt.grid(axis="y")
    plt.xticks(rotation=35)
    plt.show()


def ex3_tutorato2():
    with open("/src/filetutorato2/two_moons_vectors.pkl", "rb") as f:
        vector1, vector2 = pickle.load(f)

    plt.scatter(vector1, vector2)
    plt.xlabel("vettore 1")
    plt.ylabel("vettore 2")
    plt.title("Moon Dataset")
    plt.show()

    media1 = np.average(vector1)
    media2 = np.average(vector2)
    dev1 = np.std(vector1)
    dev2 = np.std(vector2)
    data1 = f"Vettore 1 : Media = {media1}, Deviazione Standard = {dev1}"
    data2 = f"Vettore 2 : Media = {media2}, Deviazione Standard = {dev2}"

    with open("/src/filetutorato2/newpckl.pckl", "wb") as f:
        pickle.dump((data1, data2), f)


def ex4_tutorato2():
    array = np.array(np.linspace(0, 2 * np.pi, 100))
    y_sine = np.sin(array)
    y_cos = np.cos(array)

    plt.plot(array, y_sine, color="blue", label="Sine")
    plt.plot(array, y_cos, color="red", label="Cosine")
    plt.fill_between(array, y_sine, y_cos, alpha=0.5, color="lightyellow")
    plt.title("SENO E COSENO")
    plt.ylabel("0 - 2pi")
    plt.xlabel("0 - 100")
    plt.legend()
    plt.grid(True)
    plt.show()
