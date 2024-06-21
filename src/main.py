import tkinter as tk
from gui import CellularAutomatonGUI

def main():
    root = tk.Tk()
    root.title("Cellular Automaton")
    app = CellularAutomatonGUI(root, rows=50, cols=50, cell_size=10)
    root.mainloop()

if __name__ == "__main__":
    main()
