from collections import deque
import heapq
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

def heuristic(state: LightsOutState):
    """Counts the number of lights currently ON."""
    return sum(cell for row in state.board for cell in row)

def solve_astar(initial_state: LightsOutState):
    """
    A* Search Algorithm.
    Uses a priority queue to explore states based on f(n) = g(n) + h(n)
    where g(n) is the cost to reach the state and h(n) is the heuristic.
    """
    # Priority Queue stores: (f_score, current_state, path_taken)
    # The f_score determines the order of extraction
    priority_queue = []
    
    # Initial scores
    g_score = 0  # Moves made so far
    h_score = heuristic(initial_state)
    f_score = g_score + h_score
    
    counter = 0
    
    heapq.heappush(priority_queue, (f_score, counter, initial_state, []))
    
    # visited stores the best g_score found for each state
    visited = {initial_state: g_score}

    while priority_queue:
        # Pop the state with the LOWEST f_score
        _, _, current_state, path = heapq.heappop(priority_queue)

        if current_state.is_goal():
            return path

        for next_state, action in current_state.get_successors():
            new_g = len(path) + 1
            
            # If we haven't seen this state OR we found a shorter way to get there
            if next_state not in visited or new_g < visited[next_state]:
                visited[next_state] = new_g
                h = heuristic(next_state)
                f = new_g + h
                counter += 1
                heapq.heappush(priority_queue, (f, counter, next_state, path + [action]))

    return None