**Industrial Software Development (ISDe)**
**2025/01/20**

**Part 1**

You have 60 minutes to answer the questions that can be found below. You can only write the answers on the other sheet.

**Exercise 1**

A system contains a "robot" that navigates a grid. The robot begins at the START state. Using the `move()` method, the robot attempts to navigate to a TARGET state, but can encounter various obstacles or take specific actions which alter its state. The possible states are:

- **START**: The robot begins here.
- **OBSTACLE**: The robot encounters an obstacle and pauses.
- **CHARGING**: The robot moves to a charging station to refill its battery.
- **TARGET**: The robot successfully reaches the target.

The following actions and transitions are defined:

1. If the robot encounters an obstacle, it transitions from any state to the OBSTACLE state.
2. If the robot runs out of battery, it transitions to the CHARGING state.
3. Once fully charged, it transitions back to the START state.
4. If no obstacles or battery issues are encountered, the robot transitions directly from START to TARGET.

1. Draw the state transition diagram.
2. Write the transition table needed to implement the ROBOT behavior.

**Exercise 2**

A vending machine dispenses snacks and can store up to 100 snacks. Model the vending machine using a class.

- Snacks are added using the `ADD_SNACKS()` method and dispensed using the `DISPENSE_SNACK()` method.
- Subscribers may be interested in the `STOCK_LOW` and `STOCK_FULL` events.
- Subscribers may have different strategies for notification. For example, one strategy prints the event name in reverse, while another prints it in uppercase.

1. Model the system and draft the source code needed (you can use pseudocode). The involved classes with attributes and methods (with their input and output arguments) must be clearly shown.

**Part 2**

You have 60 minutes to implement on your PC the code for Exercises 1 and 2. Upload your solutions using the open assignments (one for each exercise) in the Teams group.

1. Implement on your PC the code of Exercises 1 and 2.
2. For Exercise 1, write a `main` that clearly shows that the state machine works correctly. You should implement AT LEAST the following situations:
   - START -> OBSTACLE -> CHARGING -> START -> TARGET
   - START -> TARGET
   - START -> CHARGING -> OBSTACLE -> START -> TARGET
   The robot must print its status after each transition.
3. For Exercise 2, define a `main` that clearly shows the operating mechanism of the subscribers with the appropriate `ADD_SNACKS()` and `DISPENSE_SNACK()` operations on the vending machine. Assign different strategies to the subscribers. Show what happens when the subscriber is interested or no longer interested in an event.

