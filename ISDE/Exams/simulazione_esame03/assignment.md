Industrial Software Development (ISDe)
[Date]

**Part 1**

You have 60 minutes to answer the questions that can be found on the other sheet and complete Exercises 1 and 2. Write your answers on the other sheet.

**Exercise 1**

A robot operates on a grid starting in the START position. The robot moves between states using the `move()` method, which accepts commands like "UP," "DOWN," "LEFT," and "RIGHT." The robot collects keys represented as strings during its movement.

If the robot collects "KEY1," "KEY2," and "KEY3" in this order, it reaches the UNLOCKED state. If it collects a key in an incorrect order or performs an invalid move, it returns to the START state. Collected keys between valid transitions do not disrupt the sequence. If, while in the UNLOCKED state, the robot collects any additional key, it returns to the START state.

1. Draw the state transition diagram.
2. Write the transition table needed to implement the ROBOT behavior.

**Exercise 2**

A library system manages a collection of books, which can store up to 500 books. Model the library system using a class.

Books are added using the `ADD_BOOK()` method and borrowed using the `BORROW_BOOK()` method. The library should also track when a book is returned using the `RETURN_BOOK()` method.

Subscribers may be interested in the `BOOK_ADDED` and `BOOK_BORROWED` events.

Subscribers also have a strategy that is triggered when an update from the publisher is received. For example, one strategy might email a notification, while another might log the event to a database.

1. Model the system and draft the source code needed (you can also use pseudocode). The involved classes with attributes and methods (including their input and output arguments) must be clearly shown.

---

**Part 2**

You have 60 minutes to implement on your PC the code for Exercises 1 and 2. Upload your solutions using the open assignments (one for each exercise) in the Teams group.

1. Implement on your PC the code for Exercises 1 and 2.
2. For Exercise 1, write a `main` that clearly shows that the state machine works correctly. You should implement at least the following situations:
   - "KEY1," "KEY2," "WRONG_KEY," "KEY3" → final state: START
   - "KEY1," "KEY2," "KEY3," "WRONG_MOVE," "KEY1" → final state: START
   - "KEY1," "KEY2," "KEY3" → final state: UNLOCKED

   The robot must print its status after each transition.

3. For Exercise 2, define a `main` that clearly shows the operating mechanism of the subscribers with the appropriate `ADD_BOOK()`, `BORROW_BOOK()`, and `RETURN_BOOK()` operations on the library system. Assign different strategies to the subscribers. Show what happens when a subscriber is interested or no longer interested in the event.

