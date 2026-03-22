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
    
    queue = deque([(initial_state, [])])
    visited = {initial_state}

    while queue:
        current_state, path = queue.popleft()
        nodes_analyzed += 1

        if current_state.is_goal():
            execution_time = time.time() - start_time
            return {
                "path": path,
                "metrics": {
                    "time": execution_time,
                    "nodes": nodes_analyzed,
                    "memory": len(visited)  # Total states stored
                }
            }

        for next_state, action in current_state.get_successors():
            if next_state not in visited:
                visited.add(next_state)
                queue.append((next_state, path + [action]))

    return None

def heuristic_hamming(state: LightsOutState):
    """Counts the number of lights currently ON."""
    return sum(cell for row in state.board for cell in row)

def solve_astar(initial_state: LightsOutState):
    """
    A* Search with performance metrics.
    """
    start_time = time.time()
    nodes_analyzed = 0
    counter = 0 # Tie-breaker for heapq
    
    # Priority Queue: (f_score, counter, state, path)
    priority_queue = []
    h_score = heuristic_hamming(initial_state)
    heapq.heappush(priority_queue, (h_score, counter, initial_state, []))
    
    # visited stores the best g_score (cost) to reach each state
    visited = {initial_state: 0}

    while priority_queue:
        f, _, current_state, path = heapq.heappop(priority_queue)
        nodes_analyzed += 1

        if current_state.is_goal():
            execution_time = time.time() - start_time
            return {
                "path": path,
                "metrics": {
                    "time": execution_time,
                    "nodes": nodes_analyzed,
                    "memory": len(visited)
                }
            }

        for next_state, action in current_state.get_successors():
            new_g = len(path) + 1
            
            if next_state not in visited or new_g < visited[next_state]:
                visited[next_state] = new_g
                h = heuristic_hamming(next_state)
                f = new_g + h
                counter += 1
                heapq.heappush(priority_queue, (f, counter, next_state, path + [action]))

    return None