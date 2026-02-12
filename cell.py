import tkinter as tk


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
        self.visited = False
        self.parent = None
        self.in_solution = False

    def draw_current_cell(self, canvas: tk.Canvas,
                          color: str = 'lightgrey') -> None:
        canvas.create_rectangle(
            20 + self.x * self.cell_size,
            20 + self.y * self.cell_size,
            20 + (self.x + 1) * self.cell_size,
            20 + (self.y + 1) * self.cell_size,
            fill=color,
            outline=''
        )

    def get_wall_coordinates(self, position):
        padding = 20
        x = padding + (self.x * self.cell_size)
        y = padding + (self.y * self.cell_size)

        if position == 'top':
            return (x, y, x + self.cell_size, y)
        elif position == 'bottom':
            return (x, y + self.cell_size,
                    x + self.cell_size, y + self.cell_size)
        elif position == 'left':
            return (x, y, x, y + self.cell_size)
        elif position == 'right':
            return (x + self.cell_size, y,
                    x + self.cell_size, y + self.cell_size)

    def draw_walls(self, canvas: tk.Canvas):
        if self.walls['top']:
            coordinates = self.get_wall_coordinates('top')
            canvas.create_line(*coordinates, width=3)
        if self.walls['right']:
            coordinates = self.get_wall_coordinates('right')
            canvas.create_line(*coordinates, width=3)
        if self.walls['bottom']:
            coordinates = self.get_wall_coordinates('bottom')
            canvas.create_line(*coordinates, width=3)
        if self.walls['left']:
            coordinates = self.get_wall_coordinates('left')
            canvas.create_line(*coordinates, width=3)
