# Assignment: Systems Modeling and Implementation

## Exercise 1
A system simulates the operation of an anti-tank missile. The missile has the following states: **IDLE**, **TARGET_LOCKED**, **FIRED**, and **IMPACT**. Using the `track_target()` and `fire()` methods, the missile transitions between these states based on user commands and environmental conditions. The possible states and transitions are:

- **IDLE**: The missile is inactive and waiting for a command.
- **TARGET_LOCKED**: The missile has locked onto a target.
- **FIRED**: The missile is in flight towards the target.
- **IMPACT**: The missile has hit the target or reached the end of its range.

The following transitions are defined:

1. From **IDLE**, the missile transitions to **TARGET_LOCKED** when a target is successfully identified.
2. From **TARGET_LOCKED**, the missile transitions to **FIRED** when the fire command is issued.
3. From **FIRED**, the missile transitions to **IMPACT** when it hits the target or after a timeout if the target is missed.

### Tasks:

1. Draw the state transition diagram for the anti-tank missile.
2. Write the transition table to implement the missile’s behavior.

---

## Exercise 2
A system manages an ammunition depot that stores and distributes ammunition. Model the depot using a class.

The depot allows users to request and restock ammunition. The following events occur within the system:

- **AMMUNITION_REQUESTED**: Triggered when a request for ammunition is received.
- **AMMUNITION_RESTOCKED**: Triggered when new ammunition is added to the depot.
- **LOW_STOCK**: Triggered when ammunition levels fall below a predefined threshold.
- **OUT_OF_STOCK**: Triggered when a request cannot be fulfilled due to insufficient ammunition.

Subscribers can use strategies to respond to these events. For example:

- One strategy sends an alert to the depot manager.
- Another strategy updates the stock log.

### Tasks:

1. Model the ammunition depot system and draft the source code (or pseudocode).
2. Clearly define the involved classes with attributes and methods, including their input and output arguments.

---

## Exercise 3
Use double dispatch to implement a card game where two cards are compared based on their rank.

### Rules:

- The game involves two players, each playing one card from their hand.
- Each card has a **suit** (e.g., Hearts, Diamonds) and a **rank** (e.g., Ace, King, Queen, etc.).
- The card with the higher rank wins the round. If the ranks are the same, the round is a draw.

### Tasks:

1. Create classes for the card suits and ranks.
2. Use double dispatch to compare two cards and determine the winner.
3. Write pseudocode or a source code sketch demonstrating the interaction between the card objects and the winner determination logic.
