import os
from datetime import datetime

# Get the directory where utils.py is located (the 'src' folder)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Define paths for the new folders
DATA_DIR = os.path.join(BASE_DIR, "data")
BENCHMARK_DIR = os.path.join(DATA_DIR, "benchmarks")
BOARDS_DIR = os.path.join(DATA_DIR, "boards")

# Ensure folders exist (creates them if they don't)
os.makedirs(BENCHMARK_DIR, exist_ok=True)
os.makedirs(BOARDS_DIR, exist_ok=True)

def get_timestamped_path():
    """Generates a full path for a benchmark file: src/data/benchmarks/benchmark_HHMMDDMMYYYY.txt"""
    now = datetime.now()
    filename = now.strftime("benchmark_%H%M%d%m%Y.txt")
    return os.path.join(BENCHMARK_DIR, filename)

def save_benchmark_to_file(board, results, difficulty):
    """
    Saves the board and all algorithm metrics to a new timestamped file in the benchmarks folder.
    """
    filepath = get_timestamped_path()
    
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
            if res:
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

def load_board_from_txt(filename):
    """
    Loads a board state from a text file located in src/data/boards/
    User only needs to provide the filename (e.g., 'puzzle1.txt')
    """
    filepath = os.path.join(BOARDS_DIR, filename)
    
    if not os.path.exists(filepath):
        print(f"File not found at: {filepath}")
        return None
        
    try:
        with open(filepath, "r") as f:
            # Filters empty lines and converts to matrix
            lines = [line.strip() for line in f if line.strip()]
            return [[int(x) for x in line.split()] for line in lines]
    except Exception as e:
        print(f"Error reading file: {e}")
        return None