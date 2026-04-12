import os
from datetime import datetime

# Get the directory where utils.py is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Define paths for the new folders
DATA_DIR = os.path.join(BASE_DIR, "data")
BENCHMARK_DIR = os.path.join(DATA_DIR, "benchmarks")
BOARDS_DIR = os.path.join(DATA_DIR, "boards")

# Ensure folders exist (creates them if they don't)
os.makedirs(BENCHMARK_DIR, exist_ok=True)
os.makedirs(BOARDS_DIR, exist_ok=True)

def get_timestamped_path(directory, prefix="benchmark", extension=".txt"):
    """Generates a full path for a file with a timestamp."""
    now = datetime.now()
    filename = now.strftime(f"{prefix}_%H%M%d%m%Y{extension}")
    return os.path.join(directory, filename)

def save_benchmark_to_file(board, results, difficulty):
    """
    Saves the board and all algorithm metrics to a new timestamped file.
    """
    filepath = get_timestamped_path(BENCHMARK_DIR)
    
    with open(filepath, "w") as f:
        f.write("="*40 + "\n")
        f.write(f"LIGHTS OUT AI BENCHMARK REPORT\n")
        f.write(f"Date/Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Initial Difficulty (Random Clicks): {difficulty}\n")
        f.write("="*40 + "\n\n")

        f.write("Initial Board State:\n")
        for row in board:
            f.write(" ".join(map(str, row)) + "\n")
        
        f.write("\n" + "-"*40 + "\n")
        
        for name, res in results.items():
            if res and res.get("timeout"):
                f.write(f"ALGORITHM: {name}\n")
                f.write(f"Status: Timeout (>60s)\n")
                f.write(f"Execution Time: >60.000000 seconds\n")
                f.write(f"Path: N/A\n")
            elif res:
                path = res["path"]
                m = res["metrics"]
                f.write(f"ALGORITHM: {name}\n")
                f.write(f"Status: Solved\n")
                f.write(f"Solution Length: {len(path)} moves\n")
                f.write(f"Nodes Analyzed: {m['nodes']}\n")
                f.write(f"Memory (States in RAM): {m['memory']}\n")
                f.write(f"Execution Time: {m['time']:.6f} seconds\n")
                f.write(f"Path: {path}\n")
            else:
                f.write(f"ALGORITHM: {name}\nStatus: Failed/No Solution\n")
            f.write("-"*40 + "\n")

    print(f"\nBenchmark report created in: data/benchmarks/{os.path.basename(filepath)}")

def save_board_to_txt(board, filename=None):
    """
    Saves a specific board state to a text file so you can build your 'Puzzle Set'.
    If no filename is provided, generates a timestamped one.
    """
    if filename is None:
        filepath = get_timestamped_path(BOARDS_DIR, prefix="puzzle")
    else:
        filepath = os.path.join(BOARDS_DIR, filename)

    try:
        with open(filepath, "w") as f:
            for row in board:
                f.write(" ".join(map(str, row)) + "\n")
        print(f"Board saved to {filepath}")
    except Exception as e:
        print(f"Failed to save board: {e}")

def load_board_from_txt(filepath):
    """
    Loads a board state from a text file. Accepts absolute paths (from GUI)
    or just filenames (looks in BOARDS_DIR). Includes structural validation.
    """
    if not os.path.isabs(filepath):
        filepath = os.path.join(BOARDS_DIR, filepath)
    
    if not os.path.exists(filepath):
        print(f"File not found at: {filepath}")
        return None
        
    try:
        with open(filepath, "r") as f:
            lines = [line.strip() for line in f if line.strip()]
            board = [[int(x) for x in line.split()] for line in lines]
            
            if not board: return None
            cols = len(board[0])
            for row in board:
                if len(row) != cols:
                    print("Error: Board is not rectangular.")
                    return None
                if any(val not in (0, 1) for val in row):
                    print("Error: Board contains invalid characters (must be 0 or 1).")
                    return None
                    
            return board
    except ValueError:
        print("Error: File contains non-numeric data.")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None