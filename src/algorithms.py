from collections import deque
from lightsout import LightsOutState

def solve_bfs(initial_state: LightsOutState):
    """
    Standard Breadth-First Search.
    Guarantees the shortest path to the solution.
    """
    # Queue stores: (current_state, path_taken)
    queue = deque([(initial_state, [])])
    
    visited = {initial_state}

    while queue:
        current_state, path = queue.popleft()

        # Check if the goal (all lights off) is reached
        if current_state.is_goal():
            return path

        # Explore all 25 possible clicks
        for next_state, action in current_state.get_successors():
            if next_state not in visited:
                visited.add(next_state)
                # Append a new tuple to the queue: (the new board, the path including this click)
                queue.append((next_state, path + [action]))

    return None # No solution found