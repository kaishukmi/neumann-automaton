import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel, Button, Frame
from automaton import CellularAutomaton, STATES
from file_io import save_grid_to_file, load_grid_from_file

class CellularAutomatonGUI:
    def __init__(self, root, rows, cols, cell_size):
        self.cell_size = cell_size
        self.automaton = CellularAutomaton(rows, cols)
        self.selected_state = 'U'  # 初期選択状態

        # メインウィンドウのレイアウト
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.canvas = tk.Canvas(self.main_frame, width=cols*cell_size, height=rows*cell_size, borderwidth=0, highlightthickness=0)
        self.canvas.pack()
        self.running = False
        self.update_grid()
        self.canvas.bind("<Button-1>", self.change_cell_state)
        self.canvas.bind("<Button-3>", self.change_cell_state)

        # スペースキーで一時停止と再開を切り替える
        root.bind("<space>", self.toggle_running)

        # 状態選択ウィンドウの作成
        self.state_selection_window(root)

        # メニューの作成
        self.create_menu(root)

    def draw_grid(self):
        self.canvas.delete("all")
        for row in range(self.automaton.rows):
            for col in range(self.automaton.cols):
                color = '#%02x%02x%02x' % self.automaton.get_color(self.automaton.grid[row][col])
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

    def update_grid(self):
        if self.running:
            self.automaton.update_grid()
            self.draw_grid()
        self.canvas.after(100, self.update_grid)

    def toggle_running(self, event=None):
        self.running = not self.running

    def change_cell_state(self, event):
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        if 0 <= row < self.automaton.rows and 0 <= col < self.automaton.cols:
            self.automaton.grid[row][col] = self.selected_state
            self.draw_grid()

    def create_menu(self, root):
        menubar = tk.Menu(root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Save", command=self.save_grid)
        file_menu.add_command(label="Load", command=self.load_grid)
        file_menu.add_command(label="Reset Grid", command=self.reset_grid)
        file_menu.add_command(label="Randomize Grid", command=self.randomize_grid)
        menubar.add_cascade(label="File", menu=file_menu)

        root.config(menu=menubar)

    def save_grid(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            save_grid_to_file(self.automaton.grid, file_path)
            messagebox.showinfo("Save", "Grid saved successfully")

    def load_grid(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            self.automaton.grid = load_grid_from_file(file_path)
            self.draw_grid()
            messagebox.showinfo("Load", "Grid loaded successfully")

    def reset_grid(self):
        self.automaton.grid = [[self.selected_state for _ in range(self.automaton.cols)] for _ in range(self.automaton.rows)]
        self.draw_grid()

    def randomize_grid(self):
        self.automaton.grid = self.automaton.build_grid()
        self.draw_grid()

    def state_selection_window(self, root):
        state_frame = tk.Frame(root)
        state_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        columns = 4  # Number of columns to display buttons
        row = 0
        col = 0

        for state, color in STATES.items():
            color_hex = '#%02x%02x%02x' % color
            btn = Button(state_frame, text=state, bg=color_hex, width=15, command=lambda s=state: self.set_selected_state(s))
            btn.grid(row=row, column=col, padx=5, pady=5)
            col += 1
            if col >= columns:
                col = 0
                row += 1

    def set_selected_state(self, state):
        self.selected_state = state
