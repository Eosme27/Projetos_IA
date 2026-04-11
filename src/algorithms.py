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

def solve_ids(initial_state: LightsOutState, max_depth=25):
    """
    Iterative Deepening Search (IDS).
    Combines DFS's space-efficiency and BFS's optimality.
    """
    start_time = time.time()
    nodes_analyzed = 0

    def dls(current_state, path, depth, visited):
        nonlocal nodes_analyzed
        nodes_analyzed += 1
        
        if current_state.is_goal():
            return path
        if depth <= 0:
            return None
        
        # Standard DFS move exploration
        for next_state, action in current_state.get_successors():
            # Basic cycle detection within the current branch
            if next_state not in visited:
                visited.add(next_state)
                result = dls(next_state, path + (action,), depth - 1, visited)
                if result is not None:
                    return result
                visited.remove(next_state) # Backtrack
        return None

    # Main IDS Loop
    # For a 5x5 board, a solution is always reachable within 25 moves
    for limit in range(max_depth + 1):
        # We use a set for path-based cycle detection to keep it efficient
        found = dls(initial_state, (), limit, {initial_state})
        if found is not None:
            execution_time = time.time() - start_time
            return {
                "path": list(found),
                "metrics": {
                    "time": execution_time,
                    "nodes": nodes_analyzed,
                    # Memory in IDS is proportional to the depth of the tree (O(d))
                    "memory": limit 
                }
            }

    return None

def heuristic_hamming(state: LightsOutState):
    """Counts the number of lights currently ON.
    """
    count = 0
    for row in state.board:
        count += sum(row)
    return count

def heuristic_light_chasing(state: LightsOutState):
    count = 0
    # Iterate through all rows except the last one
    for r in range(state.rows - 1):
        count += sum(state.board[r])
    return count

def heuristic_islands(state: LightsOutState):
    """
    Counts the number of connected components (islands) of lights.
    Disconnected lights usually require more moves to 'corral' together.
    """
    rows, cols = state.rows, state.cols
    visited = set()
    islands = 0

    for r in range(rows):
        for c in range(cols):
            # If we find a light that hasn't been visited yet, it's a new island
            if state.board[r][c] == 1 and (r, c) not in visited:
                islands += 1
                # Use a small local BFS to mark all lights in this specific island
                q = deque([(r, c)])
                visited.add((r, c))
                while q:
                    curr_r, curr_c = q.popleft()
                    # Check 4-connectivity
                    for dr, dc in [(0,1), (0,-1), (1,0), (-1,0)]:
                        nr, nc = curr_r + dr, curr_c + dc
                        if 0 <= nr < rows and 0 <= nc < cols:
                            if state.board[nr][nc] == 1 and (nr, nc) not in visited:
                                visited.add((nr, nc))
                                q.append((nr, nc))
    return islands

def solve_astar(initial_state: LightsOutState, heuristic=heuristic_hamming):
    """
    A* Search that accepts any heuristic function.
    """
    start_time = time.time()
    nodes_analyzed = 0
    counter = 0 
    
    priority_queue = []
    h_score = heuristic(initial_state)
    heapq.heappush(priority_queue, (h_score, counter, initial_state, ()))
    visited = {initial_state: 0}

    while priority_queue:
        f, _, current_state, path = heapq.heappop(priority_queue)
        nodes_analyzed += 1

        if current_state.is_goal():
            return {
                "path": list(path),
                "metrics": {
                    "time": time.time() - start_time,
                    "nodes": nodes_analyzed,
                    "memory": len(visited)
                }
            }

        g = len(path)
        for next_state, action in current_state.get_successors():
            new_g = g + 1
            if next_state not in visited or new_g < visited[next_state]:
                visited[next_state] = new_g
                h = heuristic(next_state) # Swappable heuristic
                counter += 1
                heapq.heappush(priority_queue, (new_g + h, counter, next_state, path + (action,)))
    return None

def solve_weighted_astar(initial_state: LightsOutState, heuristic=heuristic_hamming, weight=1.5):
    """
    Weighted A* Search that accepts any heuristic function.
    """
    start_time = time.time()
    nodes_analyzed = 0
    counter = 0 
    
    priority_queue = []
    h_init = heuristic(initial_state)
    heapq.heappush(priority_queue, (weight * h_init, counter, initial_state, ()))
    visited = {initial_state: 0}

    while priority_queue:
        f, _, current_state, path = heapq.heappop(priority_queue)
        nodes_analyzed += 1

        if current_state.is_goal():
            return {
                "path": list(path),
                "metrics": {
                    "time": time.time() - start_time,
                    "nodes": nodes_analyzed,
                    "memory": len(visited),
                    "weight": weight
                }
            }

        g = len(path)
        for next_state, action in current_state.get_successors():
            new_g = g + 1
            if next_state not in visited or new_g < visited[next_state]:
                visited[next_state] = new_g
                h = heuristic(next_state) 
                f_weighted = new_g + (weight * h)
                counter += 1
                heapq.heappush(priority_queue, (f_weighted, counter, next_state, path + (action,)))
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
