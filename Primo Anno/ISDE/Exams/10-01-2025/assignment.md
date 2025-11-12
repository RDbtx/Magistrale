# Industrial Software Development (ISDe)

Industrial Software Development (ISDe)
2025/01/10

Part 1

You i i
(e) pave 60 minutes to answer the questions that can be found on the other sheet and do
Exercises 1 and 2. You Can only write the answers on the other sheet.

Exercise 1

A game contains the character "warrior". The character begins the action Starting from the
ZERO state. Using the Catch() method the warrior collects various objects, which, in our case,
are represented by strings.

If the warrior collects “AMULET1”, “AMULET2” and “AMULET3" in this order then he arrives in
the POWER state. If he instead collects an amulet in an incorrect sequence, he returns to the
ZERO state. The objects collected between one amulet and another do not interrupt the
sequence that leads to the POWER state. If, from the POWER State, he picks up any amulet,
he returns to the ZERO state.

1. Draw the state transition diagram.

2. Write the transition table needed to implement the WARRIOR behavior.

Exercise 2

A piggy bank can contain up to a maximum of 200 coins. Model the Piggy bank using a class.
Coins are inserted using the INSERT() method and withdrawn using the WITHDRAW() method.
Subscribers may be interested in the COIN_INSERTED and PIGGYBANK_FULL events.

Subscribers also have a strategy that is called when an update from the publisher is received.
For instance, a strategy may print the event name in lowercase, and another one in uppercase.

1. Model the system and draft the source code that is needed (you can also use
pseudocode). The involved classes with attributes and methods (with their input and output

arguments) must be clearly shown.


Part 2

You have 60 minutes to implement on your PC the code of Exercises 1 and 2. Upload your
solutions using the open assignments (one for each exercise) in the Teams group.

1. Implement on your PC the code of Exercises 1 and 2.
ly shows that the state machine works correctly. You

2. For Exercise 1, write a ‘main’ that clear!
should implement AT LEAST the followi
‘AMULET1', ‘AMULET2’, 'X', ‘AMULETS', ‘Y'
‘AMULET1', ‘AMULET2', ‘AMULETS', ' ‘AMULET3"
‘AMULET1', ‘AMULET2', ‘AMULET1' -> final state: ZERO

The warrior must print his status after each transition.
For Exercise 2, define a ‘main’ that clearly shows the Operating mechanism of the

3.
Subscribers with the appropriate INSERT() and WITHDRAW( operations on the Piggy
bank. Assign different Strategies to the subscribers. Show what happens when the /

ing situations:
-> final state: POWER
-> final state: ZERO

subscriber is interested or no longer interested in the event.
