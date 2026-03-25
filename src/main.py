import pygame
import sys
import time
import os
import threading
import tkinter as tk
from tkinter import filedialog
from lightsout import LightsOutState
from algorithms import solve_bfs, solve_astar
from utils import save_benchmark_to_file, load_board_from_txt, BOARDS_DIR

# --- GUI Constants ---
WIDTH, HEIGHT = 700, 800
GRID_SIZE = 5
CELL_SIZE = 80
MARGIN = 15
BOARD_Y_OFFSET = 120

# Colors
BG_COLOR = (25, 25, 35)
MODAL_BG = (40, 40, 55)
CELL_ON = (255, 230, 100)
CELL_OFF = (50, 50, 70)
CELL_LOCKED = (40, 40, 50) 
TEXT_COLOR = (240, 240, 240)
BTN_COLOR = (70, 90, 150)
BTN_HOVER = (90, 110, 180)
BTN_DISABLED = (50, 50, 60)
ACCENT_COLOR = (100, 255, 100)

class LightsOutApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Lights Out AI Benchmark")
        self.clock = pygame.time.Clock()
        self.font_title = pygame.font.SysFont("Verdana", 40, bold=True)
        self.font_main = pygame.font.SysFont("Verdana", 22)
        self.btn_font = pygame.font.SysFont("Verdana", 16)
        
        self.state = "MENU" 
        self.game = None
        self.difficulty = 5
        self.message = ""
        self.is_solving = False
        self.ai_result = None

        # Modal Selection State
        self.selected_algos = {"BFS": False, "A*": True}

    def draw_button(self, text, x, y, w, h, color=BTN_COLOR, active=True):
        mouse = pygame.mouse.get_pos()
        rect = pygame.Rect(x, y, w, h)
        final_color = color
        if not active:
            final_color = BTN_DISABLED
        elif rect.collidepoint(mouse):
            final_color = BTN_HOVER
            
        pygame.draw.rect(self.screen, final_color, rect, border_radius=5)
        text_color = TEXT_COLOR if active else (100, 100, 100)
        text_surf = self.btn_font.render(text, True, text_color)
        self.screen.blit(text_surf, (x + (w - text_surf.get_width()) // 2, y + (h - text_surf.get_height()) // 2))
        return rect

    def draw_checkbox(self, text, y, is_checked):
        box_rect = pygame.Rect(WIDTH//2 - 150, y, 20, 20)
        pygame.draw.rect(self.screen, TEXT_COLOR, box_rect, 2)
        if is_checked:
            pygame.draw.rect(self.screen, ACCENT_COLOR, box_rect.inflate(-6, -6))
        
        txt = self.btn_font.render(text, True, TEXT_COLOR)
        self.screen.blit(txt, (box_rect.x + 30, y))
        return pygame.Rect(box_rect.x, y, 200, 25)

    def render_modal(self):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0,0))

        modal_rect = pygame.Rect(WIDTH//2 - 200, HEIGHT//2 - 200, 400, 400)
        pygame.draw.rect(self.screen, MODAL_BG, modal_rect, border_radius=15)
        pygame.draw.rect(self.screen, ACCENT_COLOR, modal_rect, 2, border_radius=15)

        title = self.font_main.render("AI Configuration", True, ACCENT_COLOR)
        self.screen.blit(title, (WIDTH//2 - title.get_width()//2, modal_rect.y + 20))

        self.rect_bfs = self.draw_checkbox("BFS Algorithm", modal_rect.y + 80, self.selected_algos["BFS"])
        self.rect_astar = self.draw_checkbox("A* Algorithm", modal_rect.y + 130, self.selected_algos["A*"])

        self.btn_run_ai = self.draw_button("Run First Selected", modal_rect.x + 50, modal_rect.y + 220, 300, 40)
        self.btn_gen_bench = self.draw_button("Generate Benchmark", modal_rect.x + 50, modal_rect.y + 280, 300, 40, color=(50, 120, 50))
        self.btn_close = self.draw_button("Close", modal_rect.x + 150, modal_rect.y + 340, 100, 30, color=(150, 50, 50))

    def render_game(self):
        self.screen.fill(BG_COLOR)
        title = self.font_main.render("LIGHTS OUT", True, (255, 255, 255))
        self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 30))
        
        status_color = ACCENT_COLOR if "Solved" in self.message else TEXT_COLOR
        status = self.btn_font.render(self.message, True, status_color)
        self.screen.blit(status, (WIDTH//2 - status.get_width()//2, 75))

        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if self.is_solving:
                    color = CELL_ON if self.game.board[r][c] == 1 else CELL_LOCKED
                else:
                    color = CELL_ON if self.game.board[r][c] == 1 else CELL_OFF
                
                rect = pygame.Rect((WIDTH - (GRID_SIZE * (CELL_SIZE + MARGIN))) // 2 + c * (CELL_SIZE + MARGIN), 
                                   BOARD_Y_OFFSET + r * (CELL_SIZE + MARGIN), CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, color, rect, border_radius=10)
                if self.game.board[r][c] == 1:
                    pygame.draw.rect(self.screen, (255, 255, 255), rect, 2, border_radius=10)

        ui_active = (self.state == "GAME" and not self.is_solving)
        self.btn_open_ai = self.draw_button("AI Options", WIDTH//2 - 150, 620, 300, 50, active=ui_active)
        self.btn_back = self.draw_button("Back to Menu", WIDTH//2 - 100, 700, 200, 45, color=(150, 50, 50), active=ui_active)
        
        if self.state == "MODAL":
            self.render_modal()
        pygame.display.flip()

    def render_menu(self):
        self.screen.fill(BG_COLOR)
        title = self.font_title.render("LIGHTS OUT", True, CELL_ON)
        self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 150))
        subtitle = self.font_main.render("Select Difficulty:", True, TEXT_COLOR)
        self.screen.blit(subtitle, (WIDTH//2 - subtitle.get_width()//2, 250))

        self.btn_easy = self.draw_button("EASY (3 clicks)", WIDTH//2 - 100, 320, 200, 50)
        self.btn_med  = self.draw_button("MEDIUM (7 clicks)", WIDTH//2 - 100, 390, 200, 50)
        self.btn_hard = self.draw_button("HARD (12 clicks)", WIDTH//2 - 100, 460, 200, 50)
        self.btn_load_menu = self.draw_button("LOAD FROM FILE", WIDTH//2 - 100, 550, 200, 50, color=(100, 100, 100))
        pygame.display.flip()

    def run_custom_ai(self, mode):
        board_copy = [row[:] for row in self.game.board]
        diff_val = self.difficulty

        def task():
            if mode == "SOLVE":
                algo = "A*" if self.selected_algos["A*"] else "BFS"
                func = solve_astar if algo == "A*" else solve_bfs
                res = func(LightsOutState(board=board_copy))
                self.ai_result = ("SOLVE_DONE", res)
            else:
                results = {}
                if self.selected_algos["BFS"]:
                    results["BFS"] = solve_bfs(LightsOutState(board=board_copy))
                if self.selected_algos["A*"]:
                    results["A*"] = solve_astar(LightsOutState(board=board_copy))
                save_benchmark_to_file(board_copy, results, diff_val)
                self.ai_result = ("BENCH_DONE", None)

        threading.Thread(target=task, daemon=True).start()

    def main_loop(self):
        while True:
            if self.ai_result:
                res_type, data = self.ai_result
                self.ai_result = None
                if res_type == "SOLVE_DONE":
                    if data: self.animate_solution(data['path'])
                    else: 
                        self.message = "AI found no solution."
                        self.is_solving = False
                elif res_type == "BENCH_DONE":
                    self.message = "Benchmark Complete!"
                    self.is_solving = False

            if self.state == "MENU": self.render_menu()
            else: self.render_game()

            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if self.is_solving:
                        continue 

                    if self.state == "MENU":
                        if self.btn_easy.collidepoint(pos): self.start_game(3)
                        elif self.btn_med.collidepoint(pos): self.start_game(7)
                        elif self.btn_hard.collidepoint(pos): self.start_game(12)
                        elif self.btn_load_menu.collidepoint(pos):
                            path = self.open_file_dialog()
                            if path: 
                                loaded = load_board_from_txt(os.path.basename(path))
                                if loaded: self.start_game(0, loaded)
                    
                    elif self.state == "GAME":
                        if self.btn_open_ai.collidepoint(pos): self.state = "MODAL"
                        elif self.btn_back.collidepoint(pos): self.state = "MENU"
                        else:
                            for r in range(GRID_SIZE):
                                for c in range(GRID_SIZE):
                                    rect = pygame.Rect((WIDTH - (GRID_SIZE * (CELL_SIZE + MARGIN))) // 2 + c * (CELL_SIZE + MARGIN), BOARD_Y_OFFSET + r * (CELL_SIZE + MARGIN), CELL_SIZE, CELL_SIZE)
                                    if rect.collidepoint(pos): 
                                        self.game.toggle(r, c)
                                        if self.game.is_goal(): self.message = "Solved!"

                    elif self.state == "MODAL":
                        if self.rect_bfs.collidepoint(pos): self.selected_algos["BFS"] = not self.selected_algos["BFS"]
                        if self.rect_astar.collidepoint(pos): self.selected_algos["A*"] = not self.selected_algos["A*"]
                        if self.btn_close.collidepoint(pos): self.state = "GAME"
                        if self.btn_run_ai.collidepoint(pos):
                            if any(self.selected_algos.values()):
                                self.state = "GAME"; self.is_solving = True
                                self.message = "AI Calculating..."; self.run_custom_ai("SOLVE")
                        if self.btn_gen_bench.collidepoint(pos):
                            if any(self.selected_algos.values()):
                                self.state = "GAME"; self.is_solving = True
                                self.message = "Generating Benchmark..."; self.run_custom_ai("BENCH")

            self.clock.tick(60)

    def start_game(self, diff, board=None):
        self.game = LightsOutState(board=board)
        self.difficulty = diff if board is None else "Custom"
        if board is None: self.game.generate_random_solvable(num_clicks=diff)
        self.message = "Human Play Mode"; self.state = "GAME"

    def animate_solution(self, path):
        self.is_solving = True
        for move in path:
            self.game.toggle(*move)
            self.message = f"AI applying move {move}..."
            self.render_game()
            pygame.time.wait(300)
        self.is_solving = False
        self.message = "Solved!"

    def open_file_dialog(self):
        root = tk.Tk(); root.withdraw(); root.attributes("-topmost", True)
        fp = filedialog.askopenfilename(initialdir=BOARDS_DIR, title="Select Board File", filetypes=(("Text files", "*.txt"), ("all files", "*.*")))
        root.destroy()
        return fp

if __name__ == "__main__":
    app = LightsOutApp(); app.main_loop()