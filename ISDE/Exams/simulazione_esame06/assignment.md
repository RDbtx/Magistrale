# Industrial Software Development (ISDe)

---

## Part 1

You have **60 minutes** to answer the questions that can be found on the other sheet and complete **Exercises 1, 2, and 3**. Write your answers on the other sheet.

---

### Exercise 1 (State Design Pattern)

A **robot vacuum cleaner system** receives commands `START`, `PAUSE`, and `DOCK` through the `command()` method. The vacuum starts in the `IDLE` state.

- In the `IDLE` state, the vacuum waits for the `START` command to transition to the `CLEANING` state.
- While in the `CLEANING` state, the vacuum transitions to the `PAUSED` state upon receiving the `PAUSE` command.
- In the `PAUSED` state, the vacuum transitions back to `CLEANING` when the `START` command is received or to `IDLE` when the `DOCK` command is received.
- The vacuum always transitions to `IDLE` when the `DOCK` command is received from any state.

Invalid commands in any state do not change the state of the vacuum cleaner.

#### Tasks:
1. Implement the requested behavior using the **state design pattern**.
2. Define two observers (`o1`, `o2`) that log state transitions.

Write a `main` that demonstrates:
- The robot vacuum cleaner's state transitions through various command sequences.
- The behavior of the observers, including dynamic subscription and unsubscription.

---

### Exercise 2 (Observer Design Pattern)

A **stock market monitoring system** tracks the prices of various stocks. Subscribers may register to receive updates for specific stocks.

- Data updates are provided using the `UPDATE_PRICES()` method, which takes a dictionary of stock-price pairs.
- Subscribers may register to monitor specific stocks (e.g., only `AAPL` or `GOOG`).

#### Tasks:
1. Model the system and draft the source code using the **observer design pattern**. Define at least three types of subscribers:
   - A `ConsoleLogger` that prints updates to the console.
   - A `FileLogger` that writes updates to a file.
   - An `AlertSystem` that sends alerts when the price of a stock goes above or below a certain threshold.

2. Demonstrate the behavior by:
   - Simulating updates to stock prices.
   - Showing notifications being sent only to subscribers monitoring those stocks.

---

### Exercise 3 (Double Dispatch)

Implement a **game system** using the **double dispatch pattern**:

- Define two object types: `Player` and `Item`.
- Players can `equip()` and `use()` items, which behave differently based on the type of `Item` and the `Player`:
  - `Player.equip(Item)` → Adds the item to the player's inventory if compatible.
  - `Player.use(Item)` → Uses the item, affecting the player's attributes (e.g., health, damage, defense).
- Create at least three types of `Player` (`Warrior`, `Mage`, `Rogue`) and three types of `Item` (`Sword`, `Potion`, `Bow`).

#### Tasks:
1. Implement the `Player` and `Item` classes using **composition**.
2. Implement the `equip()` and `use()` methods using the **double dispatch approach**.

Write a `main` that demonstrates:
- Equipping and using different types of items for each type of player.
- Edge cases (e.g., trying to equip an incompatible item).

---

## Part 2

You have **60 minutes** to implement on your PC the code for **Exercises 1, 2, and 3**. Upload your solutions using the open assignments (one for each exercise) in the Teams group.

---

### Tasks:
1. **Exercise 1**: Write a `main` that demonstrates the robot vacuum's state transitions and observer behavior.
2. **Exercise 2**: Write a `main` that simulates stock price updates and shows notifications being sent to subscribers.
3. **Exercise 3**: Write a `main` that demonstrates:
   - Correct use of `equip()` and `use()` methods between `Player` and `Item`.
   - The behavior of specific item types like `Sword`, `Potion`, and `Bow`.
   - Handling of edge cases (e.g., equipping incompatible items).
