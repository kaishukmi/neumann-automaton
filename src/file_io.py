import json

def save_grid_to_file(grid, file_path):
    with open(file_path, 'w') as file:
        json.dump(grid, file)

def load_grid_from_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)
