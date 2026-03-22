# Lights Out

### Description
- A single-player puzzle game.
- Played on a **5x5** grid of lights.
- At the start of the game, a random number or a predefined pattern of lights is switched on.
- Pressing any light will toggle its state and the state of its **adjacent** lights (vertically and horizontally).
    - If a light was **off**, it turns **on**.
    - If a light was **on**, it turns **off**.
- **Objective:** Switch off all the lights on the board in the shortest time or fewest moves possible.

---

## Related Work
*(Add references or similar projects here)*

---

## Game Formulation as a Search Problem

### State Representation
The board is represented as a 2D matrix where:
- `0` → Light is **OFF**
- `1` → Light is **ON**

### Possible Initial State
```python
[ 
  [0, 0, 0, 0, 0],
  [0, 1, 0, 0, 0],
  [1, 1, 1, 0, 0],
  [0, 1, 0, 1, 0],
  [0, 0, 1, 1, 1] 
]
```

### Goal State
```python
[ 
  [0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0] 
]
```

---

## Operations (Operators)

- **Name:** Toggle Light $(i, j)$
- **Parameters:** Row $i$ and Column $j$ where $0 \leq i, j < 5$.
- **Precondition:** None (any cell can be toggled as long as the search is active).
- **Effect:** The state of the cell at $(i, j)$ and its neighbors $(i+1, j), (i-1, j), (i, j+1), (i, j-1)$ are inverted ($X = 1 - X$).
- **Cost:** 1 per move.