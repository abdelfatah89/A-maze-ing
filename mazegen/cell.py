import tkinter as tk
from typing import Tuple


class Cell:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.walls = {
            'top': True,
            'right': True,
            'bottom': True,
            'left': True,
        }
        self.cell_size = 50
        self.padding = 20
        self.visited = False
        self.parent = None
        self.in_solution = False

    def draw_current_cell(self, canvas: tk.Canvas,
                          color: str = 'lightgrey') -> None:
        if not canvas.winfo_exists():
            return

        canvas.create_rectangle(
            self.padding + self.x * self.cell_size,
            self.padding + self.y * self.cell_size,
            self.padding + (self.x + 1) * self.cell_size,
            self.padding + (self.y + 1) * self.cell_size,
            fill=color,
            outline=''
        )
        self.draw_walls(canvas)

    def get_wall_coordinates(self, position: str) -> Tuple[int, int, int, int]:
        x = self.padding + (self.x * self.cell_size)
        y = self.padding + (self.y * self.cell_size)

        if position == 'top':
            return (x, y, x + self.cell_size, y)
        elif position == 'bottom':
            return (x, y + self.cell_size,
                    x + self.cell_size, y + self.cell_size)
        elif position == 'left':
            return (x, y, x, y + self.cell_size)
        else:
            return (x + self.cell_size, y,
                    x + self.cell_size, y + self.cell_size)

    def draw_walls(self, canvas: tk.Canvas) -> None:
        if not canvas.winfo_exists():
            return

        for key in self.walls.keys():
            if self.walls[key]:
                coordinates = self.get_wall_coordinates(key)
                canvas.create_line(*coordinates, width=3)
