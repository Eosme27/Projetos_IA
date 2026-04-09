import time
import heapq
from collections import deque
from lightsout import LightsOutState

def solve_bfs(initial_state: LightsOutState):
    """
    Breadth-First Search with performance metrics.
    """
    start_time = time.time()
    nodes_analyzed = 0
    
    # We store the path as a tuple of actions. Tuples are much faster 
    # to copy/append than lists in Python's memory management.
    queue = deque([(initial_state, ())])
    visited = {initial_state}

    while queue:
        current_state, path = queue.popleft()
        nodes_analyzed += 1

        if current_state.is_goal():
            execution_time = time.time() - start_time
            return {
                "path": list(path), # Convert back to list for the GUI animator
                "metrics": {
                    "time": execution_time,
                    "nodes": nodes_analyzed,
                    "memory": len(visited)
                }
            }

        for next_state, action in current_state.get_successors():
            if next_state not in visited:
                visited.add(next_state)
                # tuple + (item,) is more memory-efficient here
                queue.append((next_state, path + (action,)))

    return None

def heuristic_hamming(state: LightsOutState):
    """Counts the number of lights currently ON.
    """
    count = 0
    for row in state.board:
        count += sum(row)
    return count

def solve_astar(initial_state: LightsOutState):
    """
    A* Search with performance metrics.
    """
    start_time = time.time()
    nodes_analyzed = 0
    counter = 0 
    
    # Priority Queue: (f_score, counter, state, path_tuple)
    priority_queue = []
    h_score = heuristic_hamming(initial_state)
    # Using tuples for paths saves significant time in state-heavy searches
    heapq.heappush(priority_queue, (h_score, counter, initial_state, ()))
    
    # Dictionary of state: g_score
    visited = {initial_state: 0}

    while priority_queue:
        f, _, current_state, path = heapq.heappop(priority_queue)
        nodes_analyzed += 1

        if current_state.is_goal():
            execution_time = time.time() - start_time
            return {
                "path": list(path),
                "metrics": {
                    "time": execution_time,
                    "nodes": nodes_analyzed,
                    "memory": len(visited)
                }
            }

        g = len(path)
        for next_state, action in current_state.get_successors():
            new_g = g + 1
            
            # Standard A* check: is this the cheapest way to reach this state?
            if next_state not in visited or new_g < visited[next_state]:
                visited[next_state] = new_g
                h = heuristic_hamming(next_state)
                counter += 1
                heapq.heappush(priority_queue, (new_g + h, counter, next_state, path + (action,)))

    return None

def solve_gaussian(initial_state: LightsOutState):
    """
    Gaussian Elimination over GF(2) for Lights Out.
    Models the puzzle as a system of linear equations.
    """
    import time
    start_time = time.time()
    
    rows, cols = initial_state.rows, initial_state.cols
    n = rows * cols
    
    # Build the augmented matrix [A|b] where A is n x n, b is n x 1
    # Each row i corresponds to cell i, each column j corresponds to move j
    augmented = [[0] * (n + 1) for _ in range(n)]
    
    # Fill the matrix
    for i in range(n):
        row = i // cols
        col = i % cols
        # The equation for cell (row, col)
        # b[i] = initial board state
        augmented[i][n] = initial_state.board[row][col]
        
        # For each possible move j, check if it affects cell i
        for j in range(n):
            move_row = j // cols
            move_col = j % cols
            # Check if this move affects the current cell
            if (move_row == row and move_col == col) or \
               (abs(move_row - row) + abs(move_col - col) == 1):
                augmented[i][j] = 1
    
    # Gaussian elimination over GF(2)
    operations = 0
    
    # Forward elimination
    for pivot in range(n):
        # Find pivot row
        pivot_row = -1
        for r in range(pivot, n):
            if augmented[r][pivot] == 1:
                pivot_row = r
                break
        
        if pivot_row == -1:
            # No solution or inconsistent system
            # For Lights Out, this shouldn't happen for solvable puzzles
            continue
            
        # Swap rows if needed
        if pivot_row != pivot:
            augmented[pivot], augmented[pivot_row] = augmented[pivot_row], augmented[pivot]
            operations += 1
        
        # Eliminate below
        for r in range(pivot + 1, n):
            if augmented[r][pivot] == 1:
                for c in range(n + 1):
                    augmented[r][c] ^= augmented[pivot][c]
                operations += 1
    
    # Back substitution
    solution = [0] * n
    for i in range(n - 1, -1, -1):
        if augmented[i][i] == 0:
            # Free variable, set to 0 (one possible solution)
            solution[i] = 0
        else:
            solution[i] = augmented[i][n]
            for j in range(i + 1, n):
                solution[i] ^= (augmented[i][j] * solution[j])
    
    # Convert solution to path (list of (row, col) tuples)
    path = []
    for i in range(n):
        if solution[i] == 1:
            row = i // cols
            col = i % cols
            path.append((row, col))
    
    execution_time = time.time() - start_time
    
    return {
        "path": path,
        "metrics": {
            "time": execution_time,
            "nodes": operations,  # Number of row operations
            "memory": n  # Matrix size
        }
    }
