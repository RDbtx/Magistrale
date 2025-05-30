Industrial Software Development (ISDe)

**Part 1**

You have 60 minutes to answer the questions that can be found on the other sheet and complete Exercises 1, 2, and 3. Write your answers on the other sheet.

**Exercise 1 (State Design Pattern)**

An elevator system receives commands `UP`, `DOWN`, and `STOP` through the `command()` method. The elevator starts in the IDLE state.

- In the IDLE state, the elevator waits for a `UP` or `DOWN` command to transition to the MOVING state.
- While in the MOVING state, the elevator transitions to the STOPPED state upon receiving the `STOP` command.
- In the STOPPED state, the elevator transitions back to IDLE when a `RESET` command is received.

Invalid commands in any state do not change the state of the elevator.

1. Implement the requested behavior using the state design pattern.
2. Define 2 observers (`o1`, `o2`) that respond to state transitions.

Write a main that clearly shows the transitions of the elevator using various command sequences. Demonstrate the behavior of the observers by subscribing and unsubscribing them dynamically.

**Exercise 2 (Observer Design Pattern)**

A weather monitoring system tracks temperature, humidity, and pressure. Model this system using a class.

Data updates are provided using the `UPDATE_DATA()` method. Subscribers may register to receive updates on specific data points (e.g., only temperature, only pressure).

1. Model the system and draft the source code using the observer design pattern. Define at least three types of subscribers:
   - A console logger that prints the updates.
   - A file logger that writes updates to a file.
   - A graphical display that shows the updates visually (simplified).

2. Demonstrate the behavior by simulating updates to the weather data and showing subscriber notifications.

**Exercise 3 (Double Dispatch)**

Implement a financial system using the double dispatch pattern:

- Define two object types: `BankAccount` and `Currency`.
- Implement the `deposit()` and `withdraw()` operations between these types as follows:
  - `BankAccount.deposit(Currency)` → Adds the currency value to the bank account balance.
  - `BankAccount.withdraw(Currency)` → Deducts the currency value from the bank account balance if sufficient funds are available.
  - `Currency + Currency` → Returns a new `Currency` object with the sum of their values.

1. Implement the `BankAccount` and `Currency` classes using composition.
2. Implement the `deposit()` and `withdraw()` methods using the double dispatch approach.

Write a main that demonstrates all the above cases with meaningful examples, including edge cases (e.g., overdraft attempts).

---

**Part 2**

You have 60 minutes to implement on your PC the code for Exercises 1, 2, and 3. Upload your solutions using the open assignments (one for each exercise) in the Teams group.

1. Implement on your PC the code for Exercises 1, 2, and 3.
2. For Exercise 1, write a `main` that clearly shows the elevator state transitions and the behavior of the observers.
3. For Exercise 2, define a `main` that demonstrates the behavior of the weather monitoring system and the notifications sent to subscribers.
4. For Exercise 3, write a `main` that demonstrates the correct use of the `deposit()` and `withdraw()` methods between `BankAccount` and `Currency`, as well as the `+` operator for `Currency` objects.

