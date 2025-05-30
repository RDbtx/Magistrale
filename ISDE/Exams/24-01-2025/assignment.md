# Industrial Software Development (ISDe)
## 2025/01/24

### Part 1

You have 60 minutes to answer the questions that can be found on the other sheet and do Exercises 1 and 2. You can only write the answers on the other sheets.

---

#### Exercise 1

In a magical world, there are three types of characters: **Wizard**, **Knight**, and **Dragon**. The behavior of their interactions depends on which characters interact and are reported in the following table:

| Character 1 | Wizard       | Knight       | Dragon       |
|-------------|--------------|--------------|--------------|
| **Wizard**  | TIE          | Wizard wins  | Dragon wins  |
| **Knight**  | Wizard wins  | TIE          | Knight wins  |
| **Dragon**  | Dragon wins  | Knight wins  | TIE          |

Each character interacts with another one through a public `fight_against(other_character)` method, which takes the other character as input.

The solution must be designed using either **double dispatch** OR **overloading**. You must also use an **abstract class**.

**1.** Model the system using one between UML class diagram, pseudocode, or directly drafting the code in Python. The involved classes with attributes and methods (with their input/output arguments) must be clearly shown. **No implementation is required.**

---

#### Exercise 2

Model a traffic light system using the **state design pattern**. The traffic light can be in the following states: **Green**, **Yellow**, **Red**, **Blinking Yellow**.

When it receives `0` as input, it goes into the **Blinking Yellow** state. When it receives `1`:

- If the current state is **Blinking Yellow**, it switches to **Red**.
- Otherwise, it switches to the next state following the usual order: **Red → Green → Yellow → Red → ...**.

Other inputs do not cause state transitions.

The traffic light also acts as a **publisher**, and notifies **subscribers** for events they are registered to. Use **one event** for each state (**RED**, **GREEN**, **YELLOW**, **BLINKING_YELLOW**).

The observers can register for each event and indicate a different method to be called for each event:

- `RED → stop()`
- `GREEN → move()`
- `YELLOW → slow_down()`
- `BLINKING_YELLOW → move_with_caution()`

**1.** Draw the state transition diagram describing the traffic light behavior.

**2.** Model the system using one between UML class diagram, pseudocode, or directly drafting the code in Python. The involved classes with attributes and methods (with their input/output arguments) must be clearly shown. **No implementation is required.**

---

### Part 2

You have 60 minutes to implement the code of Exercises 1 and 2 on your PC. Upload your solutions using the open assignments (one for each exercise) in the Teams group.

1. Implement on your PC the code of Exercises 1 and 2.
2. For **Exercise 1**, write a `main` that clearly shows the interactions between all the characters by printing their results.
3. For **Exercise 2**, define a `main` that clearly shows the operating mechanism of the traffic light and the subscribers. To simulate the traffic light transitions, you can use the following loop:

```python
import time

# Send input 0 to the traffic light
for _ in range(10):
    # Send input 1 to the traffic light
    time.sleep(1)

# Send input 0 to the traffic light
