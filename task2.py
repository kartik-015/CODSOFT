import tkinter as tk
from tkinter import messagebox, ttk
import numpy as np
import time
import threading
import json
import os
from datetime import datetime

class TicTacToeGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic Tac Toe - AI Challenge")
        self.window.configure(bg='#F0F4F8') 
        
        self.board = np.zeros((3, 3), dtype=int)
        self.current_player = 1  
        self.game_active = True
        self.difficulty = "Hard"  
        self.scores = {"Player": 0, "AI": 0, "Draws": 0}
        self.game_history = []
        self.winning_patterns = [
            [(0,0), (0,1), (0,2)],  
            [(1,0), (1,1), (1,2)],
            [(2,0), (2,1), (2,2)],
            [(0,0), (1,0), (2,0)],  
            [(0,1), (1,1), (2,1)],
            [(0,2), (1,2), (2,2)],
            [(0,0), (1,1), (2,2)],  
            [(0,2), (1,1), (2,0)]
        ]
        
        self.load_statistics()
        
        self.CELL_SIZE = 120
        self.BOARD_PADDING = 20
        self.LINE_WIDTH = 6  # thicker lines
        self.WINDOW_SIZE = self.CELL_SIZE * 3 + self.BOARD_PADDING * 2
        
        self.window.geometry(f"{self.WINDOW_SIZE}x{self.WINDOW_SIZE + 250}")
        self.window.resizable(False, False)
        
        self.main_frame = tk.Frame(self.window, bg='#F0F4F8')
        self.main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        self.canvas = tk.Canvas(
            self.main_frame,
            width=self.WINDOW_SIZE,
            height=self.WINDOW_SIZE,
            bg='#FFFFFF',  # white board background
            highlightthickness=0
        )
        self.canvas.pack(pady=10)
        
        self.create_control_panel()
        
        self.draw_board()
        
        self.canvas.bind('<Button-1>', self.handle_click)
        
    def create_control_panel(self):
        control_frame = tk.Frame(self.main_frame, bg='#F0F4F8')
        control_frame.pack(fill='x', pady=10)
        
        difficulty_frame = tk.Frame(control_frame, bg='#F0F4F8')
        difficulty_frame.pack(side='left', padx=10)
        
        tk.Label(
            difficulty_frame,
            text="Difficulty:",
            font=('Segoe UI', 12, 'bold'),
            bg='#F0F4F8',
            fg='#34495E'
        ).pack(side='left', padx=5)
        
        self.difficulty_var = tk.StringVar(value=self.difficulty)
        difficulty_combo = ttk.Combobox(
            difficulty_frame,
            textvariable=self.difficulty_var,
            values=["Easy", "Medium", "Hard", "Master"],
            state="readonly",
            width=10
        )
        difficulty_combo.pack(side='left', padx=5)
        difficulty_combo.bind('<<ComboboxSelected>>', self.change_difficulty)
        
        score_frame = tk.Frame(control_frame, bg='#F0F4F8')
        score_frame.pack(side='right', padx=10)
        
        self.score_label = tk.Label(
            score_frame,
            text=f"Score - You: {self.scores['Player']} | AI: {self.scores['AI']} | Draws: {self.scores['Draws']}",
            font=('Segoe UI', 12),
            bg='#F0F4F8',
            fg='#2C3E50'
        )
        self.score_label.pack()
        
        self.status_label = tk.Label(
            self.main_frame,
            text="Your turn (X)",
            font=('Segoe UI', 14, 'bold'),
            bg='#F0F4F8',
            fg='#2C3E50'
        )
        self.status_label.pack(pady=10)
        
        button_frame = tk.Frame(self.main_frame, bg='#F0F4F8')
        button_frame.pack(pady=10)
        
        self.restart_button = tk.Button(
            button_frame,
            text="New Game",
            font=('Segoe UI', 12, 'bold'),
            command=self.restart_game,
            bg='#2980B9',
            fg='white',
            activebackground='#1F618D',
            activeforeground='white',
            relief=tk.FLAT,
            padx=20,
            pady=10,
            cursor='hand2'
        )
        self.restart_button.pack(side='left', padx=5)
        
        self.stats_button = tk.Button(
            button_frame,
            text="Statistics",
            font=('Segoe UI', 12, 'bold'),
            command=self.show_statistics,
            bg='#27AE60',
            fg='white',
            activebackground='#1E8449',
            activeforeground='white',
            relief=tk.FLAT,
            padx=20,
            pady=10,
            cursor='hand2'
        )
        self.stats_button.pack(side='left', padx=5)
        
        self.undo_button = tk.Button(
            button_frame,
            text="Undo",
            font=('Segoe UI', 12, 'bold'),
            command=self.undo_move,
            bg='#C0392B',
            fg='white',
            activebackground='#922B21',
            activeforeground='white',
            relief=tk.FLAT,
            padx=20,
            pady=10,
            cursor='hand2'
        )
        self.undo_button.pack(side='left', padx=5)
        self.undo_button.config(state='disabled')
        
    def change_difficulty(self, event=None):
        self.difficulty = self.difficulty_var.get()
        self.restart_game()
        
    def draw_board(self):
        for i in range(1, 3):
            x = self.BOARD_PADDING + i * self.CELL_SIZE
            self.canvas.create_line(
                x, self.BOARD_PADDING,
                x, self.WINDOW_SIZE - self.BOARD_PADDING,
                fill='#34495E',
                width=self.LINE_WIDTH
            )
        
        for i in range(1, 3):
            y = self.BOARD_PADDING + i * self.CELL_SIZE
            self.canvas.create_line(
                self.BOARD_PADDING, y,
                self.WINDOW_SIZE - self.BOARD_PADDING, y,
                fill='#34495E',
                width=self.LINE_WIDTH
            )
    
    def draw_symbol(self, row, col, symbol):
        x = self.BOARD_PADDING + col * self.CELL_SIZE + self.CELL_SIZE // 2
        y = self.BOARD_PADDING + row * self.CELL_SIZE + self.CELL_SIZE // 2
        size = self.CELL_SIZE // 3
        
        if symbol == 1:  # X
            offset = size // 2
            # Draw a stylized X with shadow effect
            self.canvas.create_line(
                x - size, y - size,
                x + size, y + size,
                fill='#E74C3C',
                width=self.LINE_WIDTH + 2
            )
            self.canvas.create_line(
                x + size, y - size,
                x - size, y + size,
                fill='#E74C3C',
                width=self.LINE_WIDTH + 2
            )
            self.canvas.create_line(
                x - size + offset, y - size + offset,
                x + size - offset, y + size - offset,
                fill='#C0392B',
                width=self.LINE_WIDTH
            )
            self.canvas.create_line(
                x + size - offset, y - size + offset,
                x - size + offset, y + size - offset,
                fill='#C0392B',
                width=self.LINE_WIDTH
            )
        else: 
            # Draw a filled circle with gradient-like effect for O
            self.canvas.create_oval(
                x - size, y - size,
                x + size, y + size,
                outline='#2980B9',
                width=self.LINE_WIDTH + 2
            )
            self.canvas.create_oval(
                x - size + 4, y - size + 4,
                x + size - 4, y + size - 4,
                outline='#3498DB',
                width=self.LINE_WIDTH
            )
    
    def show_thinking_animation(self):
        dots = [".", "..", "..."]
        for i in range(10): 
            self.status_label.config(text=f"AI is thinking{dots[i % 3]}")
            self.window.update()
            time.sleep(0.2)
    
    def handle_click(self, event):
        if not self.game_active or self.current_player != 1:
            return
            
        col = (event.x - self.BOARD_PADDING) // self.CELL_SIZE
        row = (event.y - self.BOARD_PADDING) // self.CELL_SIZE
        
        if 0 <= row < 3 and 0 <= col < 3 and self.board[row][col] == 0:
            self.game_history.append(self.board.copy())
            self.undo_button.config(state='normal')
            
            self.make_move(row, col)
            
            if self.game_active:
                threading.Thread(target=self.ai_move, daemon=True).start()
    
    def make_move(self, row, col):
        self.board[row][col] = self.current_player
        self.draw_symbol(row, col, self.current_player)
        
        if self.check_winner():
            self.game_active = False
            winner = "Player" if self.current_player == 1 else "AI"
            self.scores[winner] += 1
            self.update_score_display()
            self.save_statistics()
            if winner == "Player":
                messagebox.showinfo("Congratulations!", "You won! Great job!")
            else:
                messagebox.showinfo("Game Over", f"{winner} won!")
            self.status_label.config(text=f"{winner} won!")
        elif self.is_board_full():
            self.game_active = False
            self.scores["Draws"] += 1
            self.update_score_display()
            self.save_statistics()
            messagebox.showinfo("Game Over", "It's a draw!")
            self.status_label.config(text="It's a draw!")
        else:
            self.current_player *= -1
            self.status_label.config(text="Your turn (X)" if self.current_player == 1 else "AI's turn (O)")
    
    def ai_move(self):
        self.status_label.config(text="AI is thinking...")
        self.window.update()
        
        self.show_thinking_animation()
        
        self.game_history.append(self.board.copy())
        self.undo_button.config(state='normal')
        
        row, col = self.get_ai_move()
        self.make_move(row, col)
    
    def get_ai_move(self):
        if self.difficulty == "Easy":
            empty_cells = self.get_empty_cells()
            return empty_cells[np.random.randint(len(empty_cells))]
            
        elif self.difficulty == "Medium":
            if np.random.random() < 0.3:
                empty_cells = self.get_empty_cells()
                return empty_cells[np.random.randint(len(empty_cells))]
            else:
                return self.get_best_move()
        
        elif self.difficulty in ["Hard", "Master"]:
            return self.get_best_move()
        
        empty_cells = self.get_empty_cells()
        return empty_cells[np.random.randint(len(empty_cells))]

    def get_best_move(self):
        best_score = float('-inf')
        best_move = None
        alpha = float('-inf')
        beta = float('inf')
        
        for i, j in self.get_empty_cells():
            self.board[i][j] = -1
            score = self.minimax(0, alpha, beta, False)
            self.board[i][j] = 0
            
            if score > best_score:
                best_score = score
                best_move = (i, j)
            alpha = max(alpha, best_score)
            
        return best_move

    def find_winning_move(self, player):
        for i, j in self.get_empty_cells():
            self.board[i][j] = player
            if self.check_winner():
                self.board[i][j] = 0
                return (i, j)
            self.board[i][j] = 0
        return None

    def minimax(self, depth, alpha, beta, is_maximizing):
        if self.check_winner():
            return -1 if is_maximizing else 1
        if self.is_board_full():
            return 0
            
        depth_penalty = 0.1 * depth
        
        if is_maximizing:
            best_score = float('-inf')
            for i, j in self.get_empty_cells():
                self.board[i][j] = -1
                score = self.minimax(depth + 1, alpha, beta, False) - depth_penalty
                self.board[i][j] = 0
                best_score = max(score, best_score)
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
            return best_score
        else:
            best_score = float('inf')
            for i, j in self.get_empty_cells():
                self.board[i][j] = 1
                score = self.minimax(depth + 1, alpha, beta, True) + depth_penalty
                self.board[i][j] = 0
                best_score = min(score, best_score)
                beta = min(beta, best_score)
                if beta <= alpha:
                    break
            return best_score

    def check_winner(self):
        for pattern in self.winning_patterns:
            values = [self.board[i][j] for i, j in pattern]
            if all(v == self.current_player for v in values):
                return True
        return False
    
    def undo_move(self):
        if len(self.game_history) >= 2:  
            self.game_history.pop()  
            self.board = self.game_history.pop()  
            self.current_player = 1
            self.game_active = True
            
            self.canvas.delete("all")
            self.draw_board()
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] != 0:
                        self.draw_symbol(i, j, self.board[i][j])
            
            self.status_label.config(text="Your turn (X)")
            self.undo_button.config(state='disabled' if len(self.game_history) == 0 else 'normal')
    
    def show_statistics(self):
        stats_window = tk.Toplevel(self.window)
        stats_window.title("Game Statistics")
        stats_window.configure(bg='#F0F4F8')
        stats_window.geometry("400x300")
        
        stats_frame = tk.Frame(stats_window, bg='#F0F4F8')
        stats_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        tk.Label(
            stats_frame,
            text="Current Session",
            font=('Segoe UI', 14, 'bold'),
            bg='#F0F4F8',
            fg='#34495E'
        ).pack(pady=10)
        
        tk.Label(
            stats_frame,
            text=f"Wins: {self.scores['Player']}",
            font=('Segoe UI', 12),
            bg='#F0F4F8',
            fg='#E74C3C'
        ).pack()
        
        tk.Label(
            stats_frame,
            text=f"Losses: {self.scores['AI']}",
            font=('Segoe UI', 12),
            bg='#F0F4F8',
            fg='#2980B9'
        ).pack()
        
        tk.Label(
            stats_frame,
            text=f"Draws: {self.scores['Draws']}",
            font=('Segoe UI', 12),
            bg='#F0F4F8',
            fg='#7F8C8D'
        ).pack()
        
        total_games = sum(self.scores.values())
        if total_games > 0:
            win_rate = (self.scores['Player'] / total_games) * 100
            tk.Label(
                stats_frame,
                text=f"Win Rate: {win_rate:.1f}%",
                font=('Segoe UI', 12),
                bg='#F0F4F8',
                fg='#27AE60'
            ).pack(pady=10)
    
    def save_statistics(self):
        stats = {
            'scores': self.scores,
            'last_updated': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        with open('tictactoe_stats.json', 'w') as f:
            json.dump(stats, f)
    
    def load_statistics(self):
        try:
            with open('tictactoe_stats.json', 'r') as f:
                stats = json.load(f)
                self.scores = stats['scores']
        except:
            self.scores = {"Player": 0, "AI": 0, "Draws": 0}
    
    def update_score_display(self):
        self.score_label.config(
            text=f"Score - You: {self.scores['Player']} | AI: {self.scores['AI']} | Draws: {self.scores['Draws']}"
        )
    
    def is_board_full(self):
        return not any(0 in row for row in self.board)
    
    def get_empty_cells(self):
        return [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == 0]
    
    def restart_game(self):
        self.board = np.zeros((3, 3), dtype=int)
        self.current_player = 1
        self.game_active = True
        self.game_history = []
        self.canvas.delete("all")
        self.draw_board()
        self.status_label.config(text="Your turn (X)")
        self.undo_button.config(state='disabled')
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = TicTacToeGUI()
    game.run()
