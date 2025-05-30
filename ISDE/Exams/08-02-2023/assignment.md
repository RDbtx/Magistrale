# Exercise 1  
## Use the Singleton Design Pattern  

### Problem Description  

Consider the following code:

```python
def f0(): 
    print('action 0')
def f1(): 
    print('action 1')
def f2(): 
    print('action 2')
def f3(): 
    print('action 3')

actions=[f0, f1, f2, f3]
while True:
    print('enter a number (0-3); 0 to exit') 
    actions[int(input())]()
```
Modify the code so that the program terminates with the call of function f0.

```f1, f2, f3``` must write the message ```'I am the function f...'``` in the log-file ```data.txt.```

Write a class that handles communication with the log-file. The class instantiates a single object (Singleton).
The object is instantiated when a function other than f0 is called by the user. The code to open, write, and close a file is as follows:
```python
with open("data.txt", "w") as f:
    f.write('abc\n') 
    f.write('def\n')
To validate the output of the file, you can use the following lines:

with open("data.txt", "r") as f:
    print(f.read())
```