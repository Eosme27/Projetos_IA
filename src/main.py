from lightsout import LightsOutState
from algorithms import solve_bfs

def main():
    game = LightsOutState()
    print("Initial Board:")
    game.print_board()
    
    print("Searching for solution...")
    solution = solve_bfs(game)
    
    if solution:
        print(f"Success! Moves: {solution}")
    else:
        print("No solution found.")

if __name__ == "__main__":
    main()