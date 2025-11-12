import sys

def factorial(value):
    try:
        result = 1
        while(value >= 1):
            result = result * value
            value = value - 1
        return result
    except TypeError:
        return print("VARIABLE SHOULD BE INT OR FLOAT!")

if __name__ == "__main__":
    print("runs as a standalone script")
    if len(sys.argv) > 1:
        print(sys.argv[1],"! =",factorial(int(sys.argv[1])))
else:
    print("i am the factorial module")