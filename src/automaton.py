import random

# Define the states with their corresponding colors
STATES = {
    "U": (48, 48, 48),
    "S": (255, 0, 0),
    "S0": (255, 125, 0),
    "S00": (255, 175, 50),
    "S000": (251, 255, 0),
    "S01": (255, 200, 75),
    "S1": (255, 150, 25),
    "S10": (255, 255, 100),
    "S11": (255, 250, 125),
    "C00": (0, 255, 128),
    "C01": (33, 215, 215),
    "C10": (255, 255, 128),
    "C11": (255, 128, 64),
    "N_excited": (36, 200, 36),
    "S_excited": (106, 255, 106),
    "W_excited": (73, 255, 73),
    "E_excited": (27, 176, 27),
    "N_quiescent": (106, 106, 255),
    "S_quiescent": (139, 139, 255),
    "W_quiescent": (122, 122, 255),
    "E_quiescent": (89, 89, 255),
    "N_special_excited": (191, 73, 255),
    "S_special_excited": (203, 106, 255),
    "W_special_excited": (197, 89, 255),
    "E_special_excited": (185, 56, 255),
    "N_special_quiescent": (255, 56, 56),
    "S_special_quiescent": (255, 89, 89),
    "W_special_quiescent": (255, 73, 73),
    "E_special_quiescent": (235, 36, 36)
}

class CellularAutomaton:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = self.build_grid()

    def build_grid(self):
        return [[random.choice(list(STATES.keys())) for _ in range(self.cols)] for _ in range(self.rows)]

    def update_grid(self):
        new_grid = [[self.grid[row][col] for col in range(self.cols)] for row in range(self.rows)]
        for row in range(self.rows):
            for col in range(self.cols):
                state = self.grid[row][col]
                neighbors = self.get_neighbors(row, col)
                new_state = self.apply_rules(state, neighbors)
                new_grid[row][col] = new_state
        self.grid = new_grid

    def get_neighbors(self, row, col):
        neighbors = {
            "N": self.grid[row-1][col] if row > 0 else "U",
            "S": self.grid[row+1][col] if row < self.rows-1 else "U",
            "W": self.grid[row][col-1] if col > 0 else "U",
            "E": self.grid[row][col+1] if col < self.cols-1 else "U"
        }
        return neighbors

    def apply_rules(self, state, neighbors):
        # Define the transition rules based on von Neumann automaton rules
        if state == "U":
            if any(n.startswith("S") for n in neighbors.values()):
                return "S"
        
        if state == "S":
            if any(n.startswith("S") for n in neighbors.values()):
                return "S1"
            return "S0"

        if state == "S0":
            if any(n.startswith("S") for n in neighbors.values()):
                return "S01"
            return "S00"

        if state == "S00":
            if any(n.startswith("S") for n in neighbors.values()):
                return "S000"
            return "S00"

        if state == "S000":
            if any(n.startswith("S") for n in neighbors.values()):
                if neighbors["N"] == "S":
                    return "N_quiescent"
                if neighbors["S"] == "S":
                    return "S_quiescent"
                if neighbors["W"] == "S":
                    return "W_quiescent"
                if neighbors["E"] == "S":
                    return "E_quiescent"
            return "E_quiescent"

        if state == "S01":
            if any(n.startswith("S") for n in neighbors.values()):
                return "E_special_quiescent"
            return "S_quiescent"

        if state == "S1":
            if any(n.startswith("S") for n in neighbors.values()):
                return "S11"
            return "S10"

        if state == "S10":
            if any(n.startswith("S") for n in neighbors.values()):
                if neighbors["N"] == "S":
                    return "N_special_quiescent"
                if neighbors["W"] == "S":
                    return "W_special_quiescent"
            return "S1"

        if state == "S11":
            if any(n.startswith("S") for n in neighbors.values()):
                return "C00"
            if neighbors["S"] == "S":
                return "S_special_quiescent"
            return "C01"

        if state.startswith("C"):
            if any(neighbors[dir].startswith("N") for dir in ["N", "S", "W", "E"]):
                if state == "C00":
                    return "C01"
                if state == "C01":
                    return "C10"
                if state == "C10":
                    return "C11"
            return state

        return state

    def get_color(self, state):
        return STATES[state]
