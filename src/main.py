import time
from lightsout import LightsOutState
from algorithms import solve_bfs, solve_astar

def main():
    game = LightsOutState()
    
    game.generate_random_solvable(num_clicks=7)

    print("\n" + "="*20)
    print("  LIGHTS OUT  ")
    print("="*20)
    print("Initial Board:")
    game.print_board()

    # 2. Menu selection
    print("Choose the algorithm:")
    print("1. Breadth-First Search (BFS) - Guaranteed Shortest")
    print("2. A* Search - Fast & Informed")
    print("3. Exit")
    
    choice = input("\nEnter your choice (1-3): ")

    if choice == '1':
        print("\nSolving with BFS...")
        start_time = time.time()
        solution = solve_bfs(game)
        elapsed = time.time() - start_time
    elif choice == '2':
        print("\nSolving with A*...")
        start_time = time.time()
        solution = solve_astar(game)
        elapsed = time.time() - start_time
    elif choice == '3':
        print("Goodbye!")
        return
    else:
        print("Invalid choice. Exiting.")
        return

    # 3. Show Results
    if solution:
        print(f"Success!")
        print(f"Moves ({len(solution)}): {solution}")
        print(f"Time taken: {elapsed:.4f} seconds")
    else:
        print("No solution found.")

if __name__ == "__main__":
    main()