import pygame
import sys
import time
from lightsout import LightsOutState
from algorithms import solve_bfs, solve_astar
from utils import save_benchmark_to_file, load_board_from_txt

# --- GUI Constants ---
WIDTH, HEIGHT = 700, 800
GRID_SIZE = 5
CELL_SIZE = 80
MARGIN = 15
BOARD_Y_OFFSET = 120

# Colors
BG_COLOR = (25, 25, 35)
CELL_ON = (255, 230, 100)
CELL_OFF = (50, 50, 70)
TEXT_COLOR = (240, 240, 240)
BTN_COLOR = (70, 90, 150)
BTN_HOVER = (90, 110, 180)
ACCENT_COLOR = (100, 255, 100)

class LightsOutApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Lights Out AI")
        self.clock = pygame.time.Clock()
        self.font_title = pygame.font.SysFont("Verdana", 40, bold=True)
        self.font_main = pygame.font.SysFont("Verdana", 22)
        self.btn_font = pygame.font.SysFont("Verdana", 16)
        
        # App State: "MENU" or "GAME"
        self.state = "MENU"
        self.game = None
        self.difficulty = 5
        self.message = ""
        self.is_solving = False

    def draw_button(self, text, x, y, w, h, color=BTN_COLOR):
        mouse = pygame.mouse.get_pos()
        rect = pygame.Rect(x, y, w, h)
        final_color = BTN_HOVER if rect.collidepoint(mouse) else color
        
        pygame.draw.rect(self.screen, final_color, rect, border_radius=5)
        text_surf = self.btn_font.render(text, True, TEXT_COLOR)
        self.screen.blit(text_surf, (x + (w - text_surf.get_width()) // 2, y + (h - text_surf.get_height()) // 2))
        return rect

    # --- MENU SCREEN ---
    def render_menu(self):
        self.screen.fill(BG_COLOR)
        
        title = self.font_title.render("LIGHTS OUT", True, CELL_ON)
        self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 150))
        
        subtitle = self.font_main.render("Select Difficulty to Start:", True, TEXT_COLOR)
        self.screen.blit(subtitle, (WIDTH//2 - subtitle.get_width()//2, 250))

        # Difficulty Buttons
        self.btn_easy = self.draw_button("EASY (3 clicks)", WIDTH//2 - 100, 320, 200, 50)
        self.btn_med  = self.draw_button("MEDIUM (7 clicks)", WIDTH//2 - 100, 390, 200, 50)
        self.btn_hard = self.draw_button("HARD (12 clicks)", WIDTH//2 - 100, 460, 200, 50)
        
        self.btn_load_menu = self.draw_button("LOAD FROM FILE", WIDTH//2 - 100, 550, 200, 50, color=(100, 100, 100))
        
        pygame.display.flip()

    def start_game(self, diff, board=None):
        self.game = LightsOutState(board=board)
        if board is None:
            self.difficulty = diff
            self.game.generate_random_solvable(num_clicks=self.difficulty)
        self.message = "Mode: Human Play. Click to toggle!"
        self.state = "GAME"

    # --- GAME SCREEN ---
    def render_game(self):
        self.screen.fill(BG_COLOR)
        
        title = self.font_main.render("LIGHTS OUT", True, (255, 255, 255))
        self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 30))
        
        status = self.btn_font.render(self.message, True, ACCENT_COLOR if "Solved" in self.message else TEXT_COLOR)
        self.screen.blit(status, (WIDTH//2 - status.get_width()//2, 75))

        # Draw Grid
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                color = CELL_ON if self.game.board[r][c] == 1 else CELL_OFF
                rect = pygame.Rect(
                    (WIDTH - (GRID_SIZE * (CELL_SIZE + MARGIN))) // 2 + c * (CELL_SIZE + MARGIN),
                    BOARD_Y_OFFSET + r * (CELL_SIZE + MARGIN),
                    CELL_SIZE, CELL_SIZE
                )
                pygame.draw.rect(self.screen, color, rect, border_radius=10)
                if color == CELL_ON:
                    pygame.draw.rect(self.screen, (255, 255, 255), rect, 2, border_radius=10)

        # Control Buttons
        self.btn_astar = self.draw_button("Solve A*", 50, 620, 130, 45)
        self.btn_bfs   = self.draw_button("Solve BFS", 200, 620, 130, 45)
        self.btn_bench = self.draw_button("Benchmark", 350, 620, 130, 45)
        self.btn_hint  = self.draw_button("Get Hint", 500, 620, 130, 45)
        self.btn_back  = self.draw_button("Back to Menu", WIDTH//2 - 100, 700, 200, 45, color=(150, 50, 50))

        pygame.display.flip()

    def animate_solution(self, path):
        self.is_solving = True
        for move in path:
            self.game.toggle(*move)
            self.message = f"AI applying move {move}..."
            self.render_game()
            pygame.time.wait(300)
        self.is_solving = False
        self.message = "Solved!"

    def main_loop(self):
        while True:
            if self.state == "MENU":
                self.render_menu()
            else:
                self.render_game()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    
                    if self.state == "MENU":
                        if self.btn_easy.collidepoint(pos): self.start_game(3)
                        elif self.btn_med.collidepoint(pos): self.start_game(7)
                        elif self.btn_hard.collidepoint(pos): self.start_game(12)
                        elif self.btn_load_menu.collidepoint(pos):
                            fn = input("Enter filename from src/data/boards: ")
                            board = load_board_from_txt(fn)
                            if board: self.start_game(0, board=board)
                    
                    elif self.state == "GAME" and not self.is_solving:
                        # Grid Clicks
                        for r in range(GRID_SIZE):
                            for c in range(GRID_SIZE):
                                rect = pygame.Rect(
                                    (WIDTH - (GRID_SIZE * (CELL_SIZE + MARGIN))) // 2 + c * (CELL_SIZE + MARGIN),
                                    BOARD_Y_OFFSET + r * (CELL_SIZE + MARGIN),
                                    CELL_SIZE, CELL_SIZE
                                )
                                if rect.collidepoint(pos):
                                    self.game.toggle(r, c)
                                    if self.game.is_goal(): self.message = "Solved!"
                        
                        # Button Clicks
                        if self.btn_astar.collidepoint(pos):
                            res = solve_astar(self.game)
                            if res: self.animate_solution(res['path'])
                        elif self.btn_bfs.collidepoint(pos):
                            res = solve_bfs(self.game)
                            if res: self.animate_solution(res['path'])
                        elif self.btn_hint.collidepoint(pos):
                            res = solve_astar(self.game)
                            if res and res['path']: self.message = f"Hint: Click {res['path'][0]}"
                        elif self.btn_bench.collidepoint(pos):
                            self.message = "Running Benchmark..."
                            self.render_game()
                            res_b = solve_bfs(self.game)
                            res_a = solve_astar(self.game)
                            save_benchmark_to_file(self.game.board, {"BFS": res_b, "A*": res_a}, self.difficulty)
                            self.message = "Report saved to benchmarks!"
                        elif self.btn_back.collidepoint(pos):
                            self.state = "MENU"

            self.clock.tick(60)

if __name__ == "__main__":
    app = LightsOutApp()
    app.main_loop()