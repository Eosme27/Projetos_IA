from copy import deepcopy

class LightsOutState:
    def __init__(self, board=None):  # fixed __init__
        self.on = 1
        self.off = 0
        if board is None:
            self.board = [
                [self.off, self.off, self.off, self.off, self.off],
                [self.off, self.on,  self.off, self.off, self.off],
                [self.on, self.on, self.on, self.off, self.off],
                [self.off, self.on, self.off, self.on, self.off],
                [self.off, self.off, self.on, self.on, self.on]
            ]
        else:
            self.board = deepcopy(board)
    
    def print_board(self):
        for row in self.board:
            print(" ".join(str(cell) for cell in row))

game = LightsOutState()
game.print_board()