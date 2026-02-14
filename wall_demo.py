import tkinter as tk
from enum import Enum 
from cell import Cell
from typing import List, Tuple, Optional

class MazeApp:
    def __init__(self, root: tk.Tk, width: int, height: int):
        self.root = root
        self.width = width
        self.height = height
        self.cell_size = 40
        self.canvas = tk.Canvas(root, width=width*self.cell_size + 20, 
                               height=height*self.cell_size + 20, bg="white")
        self.canvas.pack()
        
    def draw_cell_walls(self, x: int, y: int, walls: dict[str, bool]) -> None:
        x1, y1 = x * self.cell_size + 10, y * self.cell_size + 10
        x2, y2 = x1 + self.cell_size, y1 + self.cell_size
        
        if walls.get('NORTH'):
            self.canvas.create_line(x1, y1, x2, y1, width=2, tags=f"w_{x}_{y}")
        if walls.get('EAST'):
            self.canvas.create_line(x2, y1, x2, y2, width=2, tags=f"w_{x}_{y}")
        if walls.get('SOUTH'):
            self.canvas.create_line(x1, y2, x2, y2, width=2, tags=f"w_{x}_{y}")
        if walls.get('WEST'):
            self.canvas.create_line(x1, y1, x1, y2, width=2, tags=f"w_{x}_{y}")
    
    def generate(self) -> None:
        # هنا تضع خوارزمية DFS
        # بعد كل جدار تهدمه، استدعِ:
        self.root.update()

def get_wall_coordinates(grid_x, grid_y, position):
    cell_size = 50
    padding = 20
    x = padding + (grid_x * cell_size)
    y = padding + (grid_y * cell_size)
    
    if position == 'top':
        return (x, y, x + cell_size, y)
    elif position == 'bottom':
        return (x, y + cell_size, x + cell_size, y + cell_size)
    elif position == 'left':
        return (x, y, x, y + cell_size)
    elif position == 'right':
        return (x + cell_size, y, x + cell_size, y + cell_size)


def render_maze(height: int, width: int) -> None:
    cells = [Cell(x, y) for y in range(height) for x in range(width)]
    root = tk.Tk()
    root.title("Walls Demo")

    canvas = tk.Canvas(root, bg="white", width=40 + width * 50, height=40 + height * 50)
    canvas.pack()

    drawn_walls = set()
    c = list()
    for cell in cells:
        if cell.walls['NORTH'] == True:
            wall_key = (cell.x, cell.y, 'top')
            if not wall_key in drawn_walls:
                wall_top = get_wall_coordinates(cell.x, cell.y, 'top')
                n = canvas.create_line(*wall_top, width=3)
                drawn_walls.add(wall_key)

        if cell.walls['EAST'] == True:
            wall_key = (cell.x, cell.y, 'right')
            wall_right = get_wall_coordinates(cell.x, cell.y, 'right')
            e = canvas.create_line(*wall_right, width=3)
            if not wall_key in drawn_walls:
                drawn_walls.add(wall_key)

        if cell.walls['SOUTH'] == True:
            wall_key = (cell.x, cell.y, 'bottom')
            if not wall_key in drawn_walls:
                wall_bottom = get_wall_coordinates(cell.x, cell.y, 'bottom')
                s = canvas.create_line(*wall_bottom, width=3)
                drawn_walls.add(wall_key)

        if cell.walls['WEST'] == True:
            wall_key = (cell.x, cell.y, 'left')
            if not wall_key in drawn_walls:
                wall_left = get_wall_coordinates(cell.x, cell.y, 'left')
                w = canvas.create_line(*wall_left, width=3)
                drawn_walls.add(wall_key)
        c.append((n, e, s, w))

    print(c)
    root.mainloop()


if __name__ == "__main__":
    render_maze(5, 5)