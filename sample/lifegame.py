import tkinter as tk
import random

class CellularAutomaton:
    def __init__(self, root, rows, cols, cell_size):
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.grid = self.build_grid()
        self.canvas = tk.Canvas(root, width=cols*cell_size, height=rows*cell_size, borderwidth=0, highlightthickness=0)
        self.canvas.pack()
        self.running = False
        self.update_grid()
        self.canvas.bind("<Button-1>", self.toggle_running)

    def build_grid(self):
        return [[random.randint(0, 1) for _ in range(self.cols)] for _ in range(self.rows)]

    def draw_grid(self):
        self.canvas.delete("all")
        for row in range(self.rows):
            for col in range(self.cols):
                color = "black" if self.grid[row][col] == 1 else "white"
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

    def update_grid(self):
        if self.running:
            new_grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
            for row in range(self.rows):
                for col in range(self.cols):
                    num_neighbors = self.count_neighbors(row, col)
                    if self.grid[row][col] == 1:
                        new_grid[row][col] = 1 if num_neighbors in [2, 3] else 0
                    else:
                        new_grid[row][col] = 1 if num_neighbors == 3 else 0
            self.grid = new_grid
            self.draw_grid()
        self.canvas.after(100, self.update_grid)

    def count_neighbors(self, row, col):
        neighbors = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),          (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        count = 0
        for dr, dc in neighbors:
            r, c = row + dr, col + dc
            if (0 <= r < self.rows) and (0 <= c < self.cols):
                count += self.grid[r][c]
        return count

    def toggle_running(self, event):
        self.running = not self.running

def main():
    root = tk.Tk()
    root.title("Cellular Automaton")
    app = CellularAutomaton(root, rows=50, cols=50, cell_size=10)
    root.mainloop()

if __name__ == "__main__":
    main()
