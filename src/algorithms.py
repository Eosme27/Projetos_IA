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