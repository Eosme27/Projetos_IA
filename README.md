# Lights Out: AI Search & Benchmark Suite

This project is a Python-based implementation of the classic **Lights Out** puzzle game, featuring a fully dynamic board size and an advanced Artificial Intelligence benchmarking suite. It allows users to play the game interactively, request optimal hints, and run various uninformed and heuristic-based search algorithms to compare their performance.

A technical report can be found [here](./docs/report.md).

## ✨ Features

* **Dynamic Board Sizes:** Play and solve puzzles on 3x3, 4x4, 5x5, and 6x6 grids.
* **Human Play Mode:** Generate random, mathematically solvable boards at varying difficulties (Easy, Medium, Hard).
* **Interactive Tools:** * **Get Hint:** Instantly calculates the optimal next move using Gaussian Elimination.
  * **Save Board:** Exports your current grid to a `.txt` file to build a custom puzzle set.
  * **Load Board:** Import specific puzzle states from text files.
* **AI Visualizer:** Watch the AI animate the optimal solution step-by-step.
* **Benchmarking Suite:** Run multiple algorithms simultaneously in the background. Generates detailed performance reports (nodes analyzed, memory usage, execution time, and path length) saved to timestamped text files.

## 🧠 Implemented Algorithms

**Uninformed Search:**
1. **Breadth-First Search (BFS)** - Optimal but highly memory-intensive.
2. **Iterative Deepening Search (IDS)** - Optimal and highly memory-efficient.

**Informed (Heuristic) Search:**
3. **A* Search** - Optimal (with admissible heuristics).
4. **Weighted A*** - Sub-optimal but designed for high-speed solving.

**Mathematical/Algebraic:**
5. **Gaussian Elimination over GF(2)** - Instant and optimal.

**Available Heuristics:**
* **Hamming:** Counts the total number of lights currently ON.
* **Light Chasing:** Counts lights ON in all rows except the bottom row.
* **Islands:** Calculates the number of disconnected clusters (connected components) of lights.

---

## 🛠️ Prerequisites & Installation

This program requires **Python 3.7 or higher**.

1. **Install Dependencies:**
   The graphical user interface is built using `pygame`. 
   Open your terminal or command prompt and run:
   ```bash
   pip install pygame
   ```

2. **Directory Setup:**
   Ensure all Python files (`main.py`, `algorithms.py`, `lightsout.py`, `utils.py`) are in the same folder. The program will automatically generate a `data/` directory to store your benchmarks and saved boards upon first run.

---

## 🚀 How to Run (Compilation & Execution)

Because this is a Python script, no traditional compilation (like C++ or Java) is required. Simply navigate to the project directory in your terminal and execute the main file:

```bash
python main.py
```
*(Note: Depending on your system configuration, you may need to use `python3 main.py`)*

---

## 🎮 User Guide

### 1. Main Menu
* **Grid Size:** Click to toggle the board dimensions (cycles from 3x3 up to 6x6).
* **Select Difficulty:** Choose Easy (3 clicks), Medium (7 clicks), or Hard (12 clicks) to generate a random solvable board.
* **Load From File:** Opens a file explorer allowing you to load a specific `.txt` board state. 

### 2. Game Mode
* **Playing:** Click any cell to toggle it and its adjacent neighbors (up, down, left, right). The goal is to turn all lights OFF.
* **Get Hint:** Calculates the optimal solution and displays the exact Row and Column you should click next at the top of the screen.
* **Save Board:** Saves the current grid layout to a text file in the `data/boards/` folder.
* **AI Options & Benchmark:** Opens the AI Configuration Modal.

### 3. AI Configuration Modal
Check the boxes for the algorithms you wish to run. If you select **A*** or **Weighted A***, you can select which heuristics to apply (multiple can be selected for benchmarking).

* **Solve Current Board:** Uses the *highest priority algorithm* and the *first selected heuristic* to calculate a solution. Once found, it animates the moves on the screen.
* **Generate Benchmark:** Runs **all** selected algorithms and heuristics silently in the background on a copy of the current board. Once finished, a detailed `.txt` report will be generated in the `data/benchmarks/` folder.

---

## 📂 File Structure

```text
project_folder/
│
├── main.py          # GUI, Event Loop, and multi-threading
├── algorithms.py    # Search algorithms and heuristic functions
├── lightsout.py     # Game state representation and successor logic
├── utils.py         # File I/O, timestamping, and directory management
│
├── docs/
│   └── report.md    # Technical formulation and benchmark analysis
│
└── data/            # (Auto-generated upon running)
    ├── benchmarks/  # Benchmark reports are saved here
    └── boards/      # Saved custom puzzles are stored here
```

---

## 📝 Custom Board Format (.txt)
Custom boards are saved as plain text grids using `0`s (OFF) and `1`s (ON) separated by spaces. The program automatically detects the dimensions based on the text file.

**Example of a 4x4 board:**
```text
0 1 0 1
1 1 1 0
0 1 1 1
1 1 0 1
```