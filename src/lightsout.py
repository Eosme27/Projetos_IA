from copy import deepcopy

class LightsOutState:
    def __init__(self, board=None):
        self.rows = 5
        self.cols = 5
        if board is None:
            self.board = [
                [0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0],
                [1, 1, 1, 0, 0],
                [0, 1, 0, 1, 0],
                [0, 0, 1, 1, 1]
            ]
        else:
            self.board = deepcopy(board)
    
    def __hash__(self):
        # Converts the 2D board into a tuple of tuples so it can be hashed
        return hash(tuple(tuple(row) for row in self.board))

    def __eq__(self, other):
        # Allows comparing two states
        return self.board == other.board

    def print_board(self):
        for row in self.board:
            print(" ".join(str(cell) for cell in row))
        print("-" * 10)

    def is_goal(self):
        """Verifies if all the lights are off."""
        return all(cell == 0 for row in self.board for cell in row)

    def toggle(self, r, c):
        """Applies the move at position (r, c) and its adjacent cells."""
        # List of positions to toggle: (current, up, down, left, right)
        positions = [(r, c), (r-1, c), (r+1, c), (r, c-1), (r, c+1)]
        
        for row, col in positions:
            if 0 <= row < self.rows and 0 <= col < self.cols:
                # Inverts between 0 and 1 using XOR or subtraction
                self.board[row][col] = 1 - self.board[row][col]

    def get_successors(self):
        """Generates all possible states from clicking each cell."""
        successors = []
        for r in range(self.rows):
            for c in range(self.cols):
                new_state = LightsOutState(self.board)
                new_state.toggle(r, c)
                # Return the new state and the action that generated it (coordinates)
                successors.append((new_state, (r, c)))
        return successors