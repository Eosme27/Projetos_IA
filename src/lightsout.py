import random
from copy import deepcopy

class LightsOutState:
    def __init__(self, board=None):
        self.rows = 5
        self.cols = 5
        if board is None:
            # Create a clean board (all off) by default
            self.board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        else:
            self.board = deepcopy(board)
    
    def generate_random_solvable(self, num_clicks=5):
        """
        Starts with a clean board and performs random clicks.
        This ensures the puzzle is mathematically solvable.
        """
        # Reset board to all 0s first
        self.board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        
        # We track clicks to avoid clicking the same spot twice (which cancels out)
        clicks_made = 0
        used_positions = set()

        while clicks_made < num_clicks:
            r = random.randint(0, self.rows - 1)
            c = random.randint(0, self.cols - 1)
            
            if (r, c) not in used_positions:
                self.toggle(r, c)
                used_positions.add((r, c))
                clicks_made += 1

    def __hash__(self):
        return hash(tuple(tuple(row) for row in self.board))

    def __eq__(self, other):
        return isinstance(other, LightsOutState) and self.board == other.board

    def print_board(self):
        for row in self.board:
            print(" ".join(str(cell) for cell in row))
        print("-" * 10)

    def is_goal(self):
        return all(cell == 0 for row in self.board for cell in row)

    def toggle(self, r, c):
        positions = [(r, c), (r-1, c), (r+1, c), (r, c-1), (r, c+1)]
        for row, col in positions:
            if 0 <= row < self.rows and 0 <= col < self.cols:
                self.board[row][col] = 1 - self.board[row][col]

    def get_successors(self):
        successors = []
        for r in range(self.rows):
            for c in range(self.cols):
                new_state = LightsOutState(self.board)
                new_state.toggle(r, c)
                successors.append((new_state, (r, c)))
        return successors