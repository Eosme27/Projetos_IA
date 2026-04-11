import pygame
import sys
import time
import os
import threading
import tkinter as tk
from tkinter import filedialog
from lightsout import LightsOutState
from algorithms import (
    solve_bfs, solve_ids, solve_astar, solve_weighted_astar, solve_gaussian,
    heuristic_hamming, heuristic_light_chasing, heuristic_islands
)
from utils import save_benchmark_to_file, load_board_from_txt, save_board_to_txt, BOARDS_DIR

# --- GUI Constants ---
WIDTH, HEIGHT = 700, 750   # <-- Reduced height for laptop screens
CELL_SIZE = 65             # <-- Scaled down to fit 6x6 boards safely
MARGIN = 10                # <-- Tighter spacing
BOARD_Y_OFFSET = 110

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
DIVIDER_COLOR = (80, 80, 100)

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
        self.grid_size = 5
        self.message = ""
        self.is_solving = False
        self.ai_result = None

        self.selected_algos = {
            "BFS": False, 
            "IDS": False, 
            "A*": True, 
            "Weighted A*": False, 
            "Gaussian": False
        }
        self.selected_heuristics = {
            "Hamming": True, 
            "Light Chasing": False, 
            "Islands": False
        }
        self.h_rects = {} 

    def draw_button(self, text, x, y, w, h, color=BTN_COLOR, active=True):
        mouse = pygame.mouse.get_pos()
        rect = pygame.Rect(x, y, w, h)
        final_color = color
        if not active:
            final_color = BTN_DISABLED
        elif rect.collidepoint(mouse):
            final_color = BTN_HOVER
            
        pygame.draw.rect(self.screen, final_color, rect, border_radius=6)
        text_color = TEXT_COLOR if active else (100, 100, 100)
        text_surf = self.btn_font.render(text, True, text_color)
        self.screen.blit(text_surf, (x + (w - text_surf.get_width()) // 2, y + (h - text_surf.get_height()) // 2))
        return rect

    def draw_checkbox(self, text, x, y, is_checked):
        box_rect = pygame.Rect(x, y, 20, 20)
        pygame.draw.rect(self.screen, TEXT_COLOR, box_rect, 2, border_radius=4)
        if is_checked:
            pygame.draw.rect(self.screen, ACCENT_COLOR, box_rect.inflate(-6, -6), border_radius=2)
        
        txt = self.btn_font.render(text, True, TEXT_COLOR)
        self.screen.blit(txt, (box_rect.right + 15, y - 2))
        return pygame.Rect(x, y, 250, 25)

    def render_modal(self):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 190))
        self.screen.blit(overlay, (0,0))

        modal_w, modal_h = 440, 580  # Compressed modal height
        modal_rect = pygame.Rect(WIDTH//2 - modal_w//2, HEIGHT//2 - modal_h//2, modal_w, modal_h)
        pygame.draw.rect(self.screen, MODAL_BG, modal_rect, border_radius=15)
        pygame.draw.rect(self.screen, ACCENT_COLOR, modal_rect, 2, border_radius=15)

        title = self.font_main.render("AI Configuration", True, ACCENT_COLOR)
        self.screen.blit(title, (WIDTH//2 - title.get_width()//2, modal_rect.y + 20))
        pygame.draw.line(self.screen, DIVIDER_COLOR, (modal_rect.x + 20, modal_rect.y + 55), (modal_rect.right - 20, modal_rect.y + 55), 2)

        start_x = modal_rect.x + 60
        y_start = modal_rect.y + 75
        
        self.rect_bfs = self.draw_checkbox("BFS (Uninformed)", start_x, y_start, self.selected_algos["BFS"])
        self.rect_ids = self.draw_checkbox("Iterative Deepening", start_x, y_start + 35, self.selected_algos["IDS"])
        self.rect_astar = self.draw_checkbox("A* (Heuristic)", start_x, y_start + 70, self.selected_algos["A*"])
        self.rect_wastar = self.draw_checkbox("Weighted A*", start_x, y_start + 105, self.selected_algos["Weighted A*"])
        self.rect_gaussian = self.draw_checkbox("Gaussian Elimination", start_x, y_start + 140, self.selected_algos["Gaussian"])

        self.h_rects = {} 
        show_heuristics = self.selected_algos["A*"] or self.selected_algos["Weighted A*"]
        
        if show_heuristics:
            pygame.draw.line(self.screen, DIVIDER_COLOR, (modal_rect.x + 20, y_start + 185), (modal_rect.right - 20, y_start + 185), 2)
            h_label = self.btn_font.render("Select Heuristics (Checkbox):", True, ACCENT_COLOR)
            self.screen.blit(h_label, (start_x, y_start + 200))
            
            for i, h_name in enumerate(self.selected_heuristics.keys()):
                rect = self.draw_checkbox(h_name, start_x + 15, y_start + 235 + (i * 35), self.selected_heuristics[h_name])
                self.h_rects[h_name] = rect

        btn_y = modal_rect.bottom - 140
        self.btn_run_ai = self.draw_button("Solve Current Board", modal_rect.x + 45, btn_y, modal_w - 90, 40)
        self.btn_gen_bench = self.draw_button("Generate Benchmark", modal_rect.x + 45, btn_y + 50, modal_w - 90, 40, color=(50, 120, 50))
        self.btn_close = self.draw_button("Close", WIDTH//2 - 60, btn_y + 100, 120, 30, color=(150, 50, 50))

    def render_game(self):
        self.screen.fill(BG_COLOR)
        title = self.font_main.render("LIGHTS OUT", True, (255, 255, 255))
        self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 25))
        
        status_color = ACCENT_COLOR if "Solved" in self.message else TEXT_COLOR
        status = self.btn_font.render(self.message, True, status_color)
        self.screen.blit(status, (WIDTH//2 - status.get_width()//2, 65))

        for r in range(self.game.rows):
            for c in range(self.game.cols):
                if self.is_solving:
                    color = CELL_ON if self.game.board[r][c] == 1 else CELL_LOCKED
                else:
                    color = CELL_ON if self.game.board[r][c] == 1 else CELL_OFF
                
                rect = pygame.Rect((WIDTH - (self.game.cols * (CELL_SIZE + MARGIN))) // 2 + c * (CELL_SIZE + MARGIN), 
                                   BOARD_Y_OFFSET + r * (CELL_SIZE + MARGIN), CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, color, rect, border_radius=10)
                if self.game.board[r][c] == 1:
                    pygame.draw.rect(self.screen, (255, 255, 255), rect, 2, border_radius=10)

        ui_active = (self.state == "GAME" and not self.is_solving)
        
        # Compressed UI layout for the game buttons
        self.btn_hint = self.draw_button("Get Hint", WIDTH//2 - 210, 560, 200, 45, color=(180, 120, 50), active=ui_active)
        self.btn_save = self.draw_button("Save Board", WIDTH//2 + 10, 560, 200, 45, color=(50, 150, 150), active=ui_active)
        
        self.btn_open_ai = self.draw_button("AI Options & Benchmark", WIDTH//2 - 150, 620, 300, 45, active=ui_active)
        self.btn_back = self.draw_button("Back to Menu", WIDTH//2 - 100, 680, 200, 45, color=(150, 50, 50), active=ui_active)
        
        if self.state == "MODAL":
            self.render_modal()
        pygame.display.flip()

    def render_menu(self):
        self.screen.fill(BG_COLOR)
        title = self.font_title.render("LIGHTS OUT", True, CELL_ON)
        self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
        
        btn_w = 260
        self.btn_size = self.draw_button(f"Grid Size: {self.grid_size} x {self.grid_size}", WIDTH//2 - btn_w//2, 180, btn_w, 40, color=(100, 50, 150))
        
        subtitle = self.font_main.render("Select Difficulty:", True, TEXT_COLOR)
        self.screen.blit(subtitle, (WIDTH//2 - subtitle.get_width()//2, 250))

        self.btn_easy = self.draw_button("EASY (3 clicks)", WIDTH//2 - btn_w//2, 300, btn_w, 50)
        self.btn_med  = self.draw_button("MEDIUM (7 clicks)", WIDTH//2 - btn_w//2, 370, btn_w, 50)
        self.btn_hard = self.draw_button("HARD (12 clicks)", WIDTH//2 - btn_w//2, 440, btn_w, 50)
        
        pygame.draw.line(self.screen, DIVIDER_COLOR, (WIDTH//2 - 150, 520), (WIDTH//2 + 150, 520), 2)
        
        self.btn_load_menu = self.draw_button("LOAD FROM FILE", WIDTH//2 - btn_w//2, 560, btn_w, 50, color=(100, 100, 100))
        pygame.display.flip()

    def run_custom_ai(self, mode):
        board_copy = [row[:] for row in self.game.board]
        diff_val = self.difficulty
        
        h_map = {
            "Hamming": heuristic_hamming,
            "Light Chasing": heuristic_light_chasing,
            "Islands": heuristic_islands
        }
        
        active_heuristics = [name for name, is_sel in self.selected_heuristics.items() if is_sel]
        if not active_heuristics:
            active_heuristics = ["Hamming"]
            
        first_h_func = h_map[active_heuristics[0]]

        def task():
            if mode == "SOLVE":
                if self.selected_algos["Gaussian"]: res = solve_gaussian(LightsOutState(board=board_copy))
                elif self.selected_algos["Weighted A*"]: res = solve_weighted_astar(LightsOutState(board=board_copy), heuristic=first_h_func)
                elif self.selected_algos["A*"]: res = solve_astar(LightsOutState(board=board_copy), heuristic=first_h_func)
                elif self.selected_algos["IDS"]: res = solve_ids(LightsOutState(board=board_copy))
                else: res = solve_bfs(LightsOutState(board=board_copy))
                
                self.ai_result = ("SOLVE_DONE", res)
            else:
                results = {}
                state = LightsOutState(board=board_copy)
                
                if self.selected_algos["BFS"]: results["BFS"] = solve_bfs(state)
                if self.selected_algos["IDS"]: results["IDS"] = solve_ids(state)
                if self.selected_algos["Gaussian"]: results["Gaussian"] = solve_gaussian(state)
                
                if self.selected_algos["A*"]: 
                    for h_name in active_heuristics:
                        results[f"A* ({h_name})"] = solve_astar(state, heuristic=h_map[h_name])
                        
                if self.selected_algos["Weighted A*"]: 
                    for h_name in active_heuristics:
                        results[f"WA* ({h_name})"] = solve_weighted_astar(state, heuristic=h_map[h_name])
                
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
                    if self.is_solving: continue

                    if self.state == "MENU":
                        if self.btn_size.collidepoint(pos):
                            self.grid_size += 1
                            if self.grid_size > 6: self.grid_size = 3
                        elif self.btn_easy.collidepoint(pos): self.start_game(3)
                        elif self.btn_med.collidepoint(pos): self.start_game(7)
                        elif self.btn_hard.collidepoint(pos): self.start_game(12)
                        elif self.btn_load_menu.collidepoint(pos):
                            path = self.open_file_dialog()
                            if path: 
                                loaded = load_board_from_txt(path)
                                if loaded: self.start_game(0, loaded)
                    
                    elif self.state == "GAME":
                        if self.btn_hint.collidepoint(pos):
                            res = solve_gaussian(LightsOutState(board=[row[:] for row in self.game.board]))
                            if res and res['path']:
                                r, c = res['path'][0]
                                self.message = f"Hint: Click Row {r+1}, Col {c+1}"
                            else:
                                self.message = "Board is already solved or unsolvable!"
                                
                        elif self.btn_save.collidepoint(pos):
                            save_board_to_txt([row[:] for row in self.game.board])
                            self.message = "Board saved to text file!"
                            
                        elif self.btn_open_ai.collidepoint(pos): self.state = "MODAL"
                        elif self.btn_back.collidepoint(pos): self.state = "MENU"
                        else:
                            for r in range(self.game.rows):
                                for c in range(self.game.cols):
                                    rect = pygame.Rect((WIDTH - (self.game.cols * (CELL_SIZE + MARGIN))) // 2 + c * (CELL_SIZE + MARGIN), BOARD_Y_OFFSET + r * (CELL_SIZE + MARGIN), CELL_SIZE, CELL_SIZE)
                                    if rect.collidepoint(pos): 
                                        self.game.toggle(r, c)
                                        if self.game.is_goal(): self.message = "Solved!"
                        
                    elif self.state == "MODAL":
                        if self.rect_bfs.collidepoint(pos): self.selected_algos["BFS"] = not self.selected_algos["BFS"]
                        if self.rect_ids.collidepoint(pos): self.selected_algos["IDS"] = not self.selected_algos["IDS"]
                        if self.rect_astar.collidepoint(pos): self.selected_algos["A*"] = not self.selected_algos["A*"]
                        if self.rect_wastar.collidepoint(pos): self.selected_algos["Weighted A*"] = not self.selected_algos["Weighted A*"]
                        if self.rect_gaussian.collidepoint(pos): self.selected_algos["Gaussian"] = not self.selected_algos["Gaussian"]
                        
                        for h_name, rect in self.h_rects.items():
                            if rect.collidepoint(pos): 
                                self.selected_heuristics[h_name] = not self.selected_heuristics[h_name]
                            
                        if self.btn_close.collidepoint(pos): self.state = "GAME"
                        if self.btn_run_ai.collidepoint(pos):
                            if any(self.selected_algos.values()):
                                self.state = "GAME"; self.is_solving = True
                                self.message = "AI Calculating..."; self.run_custom_ai("SOLVE")
                        if self.btn_gen_bench.collidepoint(pos):
                            if any(self.selected_algos.values()):
                                self.state = "GAME"; self.is_solving = True
                                self.message = "Benchmarking..."; self.run_custom_ai("BENCH")

            self.clock.tick(60)

    def start_game(self, diff, board=None):
        self.game = LightsOutState(board=board, rows=self.grid_size, cols=self.grid_size)
        self.difficulty = diff if board is None else "Custom"
        if board is None: self.game.generate_random_solvable(num_clicks=diff)
        self.message = "Human Play Mode"; self.state = "GAME"

    def animate_solution(self, path):
        self.is_solving = True
        for move in path:
            self.game.toggle(*move)
            self.message = f"AI applying move {move}..."
            self.render_game()
            pygame.time.wait(500)
        self.is_solving = False
        self.message = "Solved!"

    def open_file_dialog(self):
        root = tk.Tk(); root.withdraw(); root.attributes("-topmost", True)
        fp = filedialog.askopenfilename(initialdir=BOARDS_DIR, title="Select Board File", filetypes=(("Text files", "*.txt"), ("all files", "*.*")))
        root.destroy()
        return fp

if __name__ == "__main__":
    app = LightsOutApp(); app.main_loop()