from lightsout import LightsOutState
from algorithms import solve_bfs, solve_astar
from utils import save_benchmark_to_file, load_board_from_txt

def print_results(algorithm_name, result):
    if not result:
        print(f"\n❌ {algorithm_name}: No solution found.")
        return

    path = result["path"]
    m = result["metrics"]
    
    print(f"\n--- {algorithm_name} Results ---")
    print(f"Solution Found: {len(path)} moves")
    print(f"Nodes Analyzed: {m['nodes']}")
    print(f"Memory (States stored): {m['memory']}")
    print(f"Time Taken: {m['time']:.6f} seconds")
    print(f"Path (clicks): {path}")

def human_mode(game):
    """Allows a human to play and ask for hints."""
    # We work on a copy so we don't mess up the board if the user wants to solve it with AI later
    temp_game = LightsOutState(board=game.board)
    
    while not temp_game.is_goal():
        print("\n" + "-"*20)
        temp_game.print_board()
        print("Type 'r,c' (ex: 1,2), 'hint' for help, or 'exit'.")
        action = input("Action: ").strip().lower()

        if action == 'exit':
            break
        elif action == 'hint':
            print("🤖 AI is calculating hint...")
            res = solve_astar(temp_game)
            if res and res["path"]:
                next_move = res["path"][0]
                print(f"💡 HINT: Try clicking at {next_move}")
            else:
                print("⚠️ No solution possible from this state!")
        else:
            try:
                r, c = map(int, action.split(','))
                temp_game.toggle(r, c)
            except:
                print("❌ Invalid format. Use row,col (e.g., 0,0)")
    
    if temp_game.is_goal():
        temp_game.print_board()
        print("\n✨ Congratulations! You solved the puzzle!")
        # Update the main game state
        game.board = temp_game.board

def main():
    game = LightsOutState()
    difficulty = 5 
    game.generate_random_solvable(num_clicks=difficulty)

    while True:
        print("\n" + "!"*40)
        print("    LIGHTS OUT - AI BENCHMARK TOOL")
        print("!"*40)
        print("Current Board State:")
        game.print_board()
        
        print("\n--- SELECT OPTION ---")
        print("1. Solve with BFS (Uninformed)")
        print("2. Solve with A* (Informed - Hamming)")
        print("3. Run Benchmark (Save to data/benchmarks/)")
        print("4. Human Play (Manual + AI Hints)")
        print("5. Load Board from data/boards/")
        print("6. Reset Board (Change Difficulty)")
        print("7. Exit")
        
        choice = input("\nSelect an option: ")

        if choice == '1':
            res = solve_bfs(game)
            print_results("BFS", res)
        
        elif choice == '2':
            res = solve_astar(game)
            print_results("A*", res)
            
        elif choice == '3':
            print("\n🚀 Running full benchmark comparison...")
            res_bfs = solve_bfs(game)
            res_astar = solve_astar(game)
            
            print_results("BFS", res_bfs)
            print_results("A*", res_astar)
            
            save_benchmark_to_file(game.board, {"BFS": res_bfs, "A*": res_astar}, difficulty)

        elif choice == '4':
            human_mode(game)

        elif choice == '5':
            print("\n📂 Looking in: src/data/boards/")
            filename = input("Enter filename (e.g., puzzle.txt): ")
            new_board = load_board_from_txt(filename)
            if new_board:
                game = LightsOutState(board=new_board)
                print("✅ Board loaded successfully!")

        elif choice == '6':
            try:
                difficulty = int(input("Enter difficulty (random clicks): "))
                game.generate_random_solvable(num_clicks=difficulty)
                print("🎲 New board generated.")
            except ValueError:
                print("❌ Please enter a valid number.")

        elif choice == '7':
            print("Exiting. Happy puzzling!")
            break

if __name__ == "__main__":
    main()