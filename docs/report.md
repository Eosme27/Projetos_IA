# Artificial Intelligence: Lights Out Search Problem

### Description
- A single-player puzzle game.
- Played on a **5x5** grid of lights.
- At the start of the game, a random number or a predefined pattern of lights is switched on.
- Pressing any light will toggle its state and the state of its **adjacent** lights (vertically and horizontally).
    - If a light was **off**, it turns **on**.
    - If a light was **on**, it turns **off**.
- **Objective:** Switch off all the lights on the board in the shortest time or fewest moves possible.

## 1. Game Formulation as a Search Problem
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

---

## 2. Search Strategies Implemented
* **Uninformed Search:** Breadth-First Search (BFS), Iterative Deepening Search (IDS).
* **Informed Search:** A* Search, Weighted A*.
* **Algebraic Approach:** Gaussian Elimination over GF(2).

---

## 3. Heuristic Functions
* **Hamming Distance:** Counts total lights ON. Admissible but sometimes underestimates significantly because one click can turn off up to 5 lights.
* **Light Chasing:** Counts lights ON in all rows except the bottom. Highly informed for top-down solving strategies.
* **Islands (Connected Components):** Counts isolated clusters of lights. Highly informed but computationally expensive.

---

## 4. Benchmark Analysis & Findings


---

## 5. Conclusion
