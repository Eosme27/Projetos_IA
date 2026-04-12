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

## Operations (Operators)

- **Name:** Toggle Light $(i, j)$
- **Parameters:** Row $i$ and Column $j$ where $0 \leq i, j < 5$.
- **Precondition:** None (any cell can be toggled as long as the search is active).
- **Effect:** The state of the cell at $(i, j)$ and its neighbors $(i+1, j), (i-1, j), (i, j+1), (i, j-1)$ are inverted ($X = 1 - X$).
- **Cost:** 1 per move.

---

## 2. Search Strategies Implemented

This section outlines the theoretical foundation and practical characteristics of the algorithms evaluated in this study. The selected methods represent three distinct computational paradigms: uninformed state-space search, heuristic-guided search, and algebraic solving.

### 2.1 Uninformed Search Algorithms
Uninformed search algorithms systematically explore the state space without utilizing domain-specific knowledge regarding the proximity of a given state to the goal.

* **Breadth-First Search (BFS):** BFS expands the search tree level by level. Because all moves in Lights Out carry a uniform cost, BFS mathematically guarantees an optimal solution path. However, its memory footprint expands exponentially at $O(b^d)$, where $b$ represents the branching factor (up to 25 valid moves) and $d$ is the depth. On a standard 5x5 grid containing $2^{25}$ discrete states, BFS rapidly exhausts available memory when applied to moderately or heavily scrambled configurations.
* **Iterative Deepening Search (IDS):** IDS addresses the severe memory limitations of BFS by executing bounded Depth-First Searches (DFS) with incrementally increasing depth limits. This approach preserves the strict optimality guarantee of BFS while constraining memory complexity to a linear $O(bd)$. The primary trade-off is computational overhead, as the upper levels of the search tree must be redundantly generated during successive iterations.

### 2.2 Informed Search Algorithms
Informed algorithms incorporate a heuristic function, $h(n)$, to estimate the required cost to transition from the current state to the goal state. This allows the search mechanism to prioritize promising branches and defer the expansion of unlikely paths.

* **A\* Search:** The A* algorithm evaluates nodes based on the composite function $f(n) = g(n) + h(n)$, combining the exact accumulated path cost $g(n)$ with the estimated remaining cost $h(n)$. A* will always return an optimal solution provided the selected heuristic is admissible (meaning it never overestimates the true cost to reach the goal). It serves as a strong balance between exhaustive path optimality and efficient memory utilization.
* **Weighted A\* (WA\*):** Weighted A* applies a scalar multiplier to the heuristic estimate, modifying the evaluation function to $f(n) = g(n) + W \cdot h(n)$, where $W > 1$. This structural adjustment artificially inflates the influence of the heuristic, inducing a greedier node expansion strategy. While the introduction of this weight systematically breaks the guarantee of optimality, it significantly restricts the size of the generated search tree, resulting in much faster execution times on complex boards where standard A* struggles.

### 2.3 Algebraic Approach
Due to the specific mathematical properties of the toggle mechanic in Lights Out, the puzzle can be modeled independently of traditional state-space tree search.

* **Gaussian Elimination over GF(2):** Every state transition in the game operates on a binary toggle, allowing the entire board to be framed as a system of linear equations over the Galois Field of 2. By representing the grid configuration and adjacency rules as an augmented matrix, we can apply Gaussian Elimination to solve the system. This mathematical reduction resolves the board in $O(N^3)$ time, where $N$ equals the total number of cells. Unlike search algorithms subject to combinatorial explosion, this algebraic method yields an optimal solution with deterministic, polynomial-time efficiency, regardless of the board's initial complexity.

---

## 3. Heuristic Functions

The performance of informed search algorithms depends entirely on the quality of the heuristic function, $h(n)$, which evaluates the estimated cost from the current state to the goal. In this study, three distinct heuristics were implemented to analyze the trade-off between computational simplicity and structural awareness.

### 3.1 Hamming Distance (Active Light Count)
The Hamming distance heuristic evaluates a state by simply counting the total number of active (ON) lights remaining on the grid. 
* **Mechanics & Complexity:** This is computationally trivial, requiring only a linear $O(N)$ traversal of the board matrix to sum the active cells. 
* **Admissibility Considerations:** In the context of Lights Out, a raw light count is technically inadmissible because a single action can deactivate up to five lights simultaneously. Consequently, the raw count frequently overestimates the true remaining cost, causing standard A* to behave greedily and return suboptimal paths. While dividing the total count by five restores mathematical admissibility, it severely underestimates the true distance, reducing the heuristic's ability to effectively prune the search tree.

### 3.2 Light Chasing
The Light Chasing heuristic is derived from a classical algorithmic strategy used to solve the puzzle, where a player systematically deactivates lights from the top row downward.
* **Mechanics & Complexity:** This function calculates the heuristic penalty by counting the active lights strictly in the upper rows, deliberately ignoring the bottom-most row. 
* **Strategic Pruning:** By heavily penalizing active lights in the upper regions of the board, this heuristic successfully forces the A* search algorithm to prioritize states that resolve the grid sequentially. It defers the remaining complexity to the final row, acting as a highly informed guide for top-down solving strategies.

### 3.3 Islands (Connected Components)
The Islands heuristic attempts to capture the spatial relationships between active lights by counting isolated, contiguous clusters. 
* **Mechanics & Complexity:** Because adjacent lights can often be resolved together via shared toggle radius, evaluating spatial grouping provides a much more accurate reflection of the true distance to the goal than a flat count. 
* **Overhead vs. Pruning:** While this heuristic is highly informed and aggressively prunes unpromising branches from the search tree, it requires executing a localized search algorithm (such as a sub-BFS or Depth-First Search) for every single node generated. The massive computational overhead required to identify connected components effectively negates its pruning benefits on complex boards, rendering it inefficient compared to simpler metrics.

---

## 4. Benchmark Analysis & Findings


---

## 5. Conclusion

This project successfully modeled the Lights Out puzzle as an Artificial Intelligence search problem.

The empirical data proves that while highly informed heuristics (like Islands) provide better structural understanding and guarantee optimal paths when admissible, their computational overhead can render them practically unusable on large search trees. In contrast, simple heuristics like Hamming paired with greedy algorithms (Weighted A*) yield the fastest search times, at the cost of path optimality.

Finally, while heuristic search is a powerful generalized AI tool, this project demonstrated that domain-specific mathematical modeling is sometimes superior. By treating the puzzle as a system of linear equations over a Galois Field of 2, **Gaussian Elimination** bypassed tree-search limitations entirely, solving even the most complex $5 \times 5$ boards instantaneously and optimally.