# Industrial Software Development (ISDe) 

---

## Part 1

You have **60 minutes** to answer the questions that can be found on the other sheet and complete **Exercises 1, 2, and 3**. Write your answers on the other sheet.

---

### Exercise 1: State Design Pattern

A **smart home thermostat system** has three states: `OFF`, `COOLING`, and `HEATING`. The system responds to commands `TURN_ON`, `TURN_OFF`, and `SET_TEMPERATURE` through the `command()` method. The initial state is `OFF`.

- In the `OFF` state, the system transitions to `COOLING` or `HEATING` upon receiving the `TURN_ON` command with a desired temperature.
- In the `COOLING` or `HEATING` state:
  - The system transitions to `OFF` when the `TURN_OFF` command is received.
  - The system adjusts between `COOLING` and `HEATING` automatically if the desired temperature changes.
- Invalid commands (e.g., `SET_TEMPERATURE` in `OFF` state) do not change the state.

#### Tasks:
1. Implement the requested behavior using the **state design pattern**.
2. Define two observers (`o1`, `o2`) that log transitions and temperature changes.
3. Write a `main` that demonstrates:
   - State transitions through various command sequences.
   - Dynamic subscription and unsubscription of the observers.

---

### Exercise 2: Observer Design Pattern

A **real-time cryptocurrency tracker** monitors the price of multiple cryptocurrencies, such as `Bitcoin`, `Ethereum`, and `Dogecoin`. The system allows users to subscribe to price updates for specific cryptocurrencies.

#### Tasks:
1. Model the system and implement it using the **observer design pattern**.
2. Define at least three types of subscribers:
   - A `ConsoleLogger` that prints price updates to the console.
   - A `FileLogger` that writes updates to a file.
   - A `MobileAlert` that sends alerts when a price crosses a specified threshold.
3. Simulate the behavior of the system:
   - Trigger price updates (e.g., "Bitcoin increased to $50,000").
   - Show notifications being sent only to subscribers interested in specific cryptocurrencies.

---

### Exercise 3: Double Dispatch

#### Context:
Create a **zoo simulation** where animals interact with visitors using **double dispatch**. There are three types of Visitors: `Child`, `Adult`, and `Veterinarian`, and three types of Animals: `Lion`, `Elephant`, and `Monkey`.

1. The interaction between visitors and animals is determined as follows:

|                 | **Lion** | **Elephant** | **Monkey** |
|-----------------|----------|--------------|------------|
| **Child**       | Gets scared | Feeds with peanuts | Plays |
| **Adult**       | Takes photo | Observes quietly | Laughs |
| **Veterinarian** | Examines | Examines | Examines |

2. Each animal has a unique characteristic:
   - `Lion`: Can roar, which scares visitors.
   - `Elephant`: Can perform tricks when interacting with `Children`.
   - `Monkey`: Can throw objects, amusing or annoying visitors.

#### Tasks:
1. Implement the system using **double dispatch**:
   - Create abstract base classes for `Visitor` and `Animal`.
   - Implement specific subclasses for each type of Visitor and Animal.
   - Use double dispatch to handle interactions between Visitors and Animals.
2. Demonstrate the behavior in a `main` program:
   - Show how each type of Visitor interacts with each type of Animal.
   - Include special behaviors (e.g., the `Lion` roaring).
3. Extend the system to:
   - Add a new type of Visitor, `Zookeeper`, who can feed all animals.
   - Add a new Animal, `Panda`, that interacts uniquely with Visitors.

---

## Part 2

You have **60 minutes** to implement on your PC the code for **Exercises 1, 2, and 3**. Upload your solutions using the open assignments (one for each exercise) in the Teams group.

---

### Tasks:
1. **Exercise 1**: Write a `main` that clearly demonstrates the thermostat system state transitions and observer behavior.
2. **Exercise 2**: Write a `main` that simulates price updates for cryptocurrencies and shows notifications being sent to subscribers.
3. **Exercise 3**: Write a `main` that demonstrates:
   - Correct use of **double dispatch** for Visitor-Animal interactions.
   - The behavior of the `Zookeeper` and the new `Panda` animal.
