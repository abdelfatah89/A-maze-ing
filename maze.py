from cell import Cell
from typing import List, Tuple
import tkinter as tk
import random


class Maze():
    def __init__(self, height:int, width:int,
                 entry:Tuple[int, int], exit_:Tuple[int, int],
                 perfect:bool, seed:int=None) -> None:
        self.height = height
        self.width = width
        self.entry = entry
        self.exit = exit_ if exit_ else (width - 1, height - 1)
        self.perfect = perfect
        self.seed = seed
        if self.seed:
            random.seed(self.seed)

        self.current_cell = None
        self.cells: List[List[Cell]] = [
            [Cell(x, y) for x in range(self.width)]
            for y in range(self.height)]

        self.finished = False

        self.generated = False
        self.cells42 = self.add_42()
        self.has_42 = False
        self.solution_path: List[Cell] = None

    def remove_walls(self, current: Cell, next: Cell) -> None:
        dx = current.x - next.x
        if dx == 1:
            current.walls['left'] = False
            next.walls['right'] = False
        elif dx == -1:
            current.walls['right'] = False
            next.walls['left'] = False

        dy = current.y - next.y
        if dy == 1:
            current.walls['top'] = False
            next.walls['bottom'] = False
        elif dy == -1:
            current.walls['bottom'] = False
            next.walls['top'] = False

    def get_neighbors(self, cell: Cell):
        neighbors = []
        directions = [
            ('top', 0, -1),
            ('right', 1, 0),
            ('bottom', 0, 1),
            ('left', -1, 0)
        ]

        for direction, dx, dy in directions:
            dx, dy = cell.x + dx, cell.y + dy
            neighbor = self.get_cell(dx, dy)
            if neighbor:
                neighbors.append((direction, neighbor))

        return neighbors

    def get_cell(self, x:int, y:int):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.cells[y][x]
        return None

    def DFS_generator(self, stack: List[Cell]):
        try:
            self.current_cell = stack[-1]
            neighbors = self.get_neighbors(self.current_cell)
            unvisited_neighbors = [
                (direction, neighbor) 
                for direction, neighbor in neighbors 
                if not neighbor.visited
            ]

            if unvisited_neighbors:
                direction, next_cell = random.choice(unvisited_neighbors)
                self.remove_walls(self.current_cell, next_cell)
                next_cell.visited = True
                stack.append(next_cell)
            else:
                stack.pop()
        except Exception as e:
            print("Error:", e)

    def get_solution_path(self) -> List[Cell]:
        path = []
        current = self.cells[-1]

        while current:
            path.append(current)
            current = current.parent

        path.reverse()
        return path

    def generate(self):
        for row in self.cells:
            for cell in row:
                cell.visited = False
                cell.walls = {
                    'top': True,
                    'right': True,
                    'bottom': True,
                    'left': True
                    }
        if not self.perfect:
            self.add_loops()
        if self.width >= 10 and self.height >= 6:
            self.add_42()
        else:
            self.has_42 = False
            self.cells42 = []
            print(f"Maze too small ({self.width}x{self.height}). "
                f"Skipping 42 pattern.")

    def add_42(self):
        """Add a '42' pattern of completely closed cells."""
        # Pattern for '4'
        pattern_4 = [
            (1, 1), (1, 2), (1, 3),
            (2, 3),
            (3, 3), (3, 2), (3, 3), (3, 4), (3, 5), (3, 1)
        ]

        # Pattern for '2'
        pattern_2 = [
            (6, 1), (7, 1), (8, 1),
            (8, 2),
            (6, 3), (7, 3), (8, 3),
            (6, 4),
            (6, 5), (7, 5), (8, 5)
        ]

        if self.width < 10 or self.height < 6:
            print("Maze is too small to add '42' pattern")
            self.has_42 = False
            return

        offset_x = (self.width - 10) // 2
        offset_y = (self.height - 6) // 2
        pattern_cells = []
        for x, y in pattern_4 + pattern_2:
            px, py = x + offset_x, y + offset_y
            if 0 <= px < self.width and 0 <= py < self.height:
                cell = self.cells[py][px]
                cell.visited = True
                cell.walls = {
                    'top': True,
                    'right': True,
                    'bottom': True,
                    'left': True
                }
                pattern_cells.append(cell)
        self.has_42 = len(pattern_cells) > 0
        if self.has_42:
            print("Added '42' pattern to the maze")
        return pattern_cells

    def add_loops(self, loop_probability: float = 0.1) -> None:
        import random
        
        for y in range(self.height):
            for x in range(self.width):
                cell = self.cells[y][x]
                if self.cells42 and cell in self.cells42:
                    continue
                
                # Randomly remove walls to adjacent cells
                if random.random() < loop_probability:
                    # Check right neighbor
                    if x + 1 < self.width and random.random() < 0.5:
                        cell.walls['right'] = False
                        self.cells[y][x + 1].walls['left'] = False
                
                if random.random() < loop_probability:
                    # Check bottom neighbor
                    if y + 1 < self.height and random.random() < 0.5:
                        cell.walls['bottom'] = False
                        self.cells[y + 1][x].walls['top'] = False

    def find_shortest_path(self) -> List[Tuple[int, int]]:
        """Find shortest path from entry
        to exit using BFS with animation."""
        from collections import deque
        
        start = self.cells[self.entry[1]][self.entry[0]]
        end = self.cells[self.exit[1]][self.exit[0]]

        # BFS setup
        queue = deque([start])
        came_from = {start: None}
        
        while queue:
            
            current = queue.popleft()
            # current.draw_current_cell(canvas, color='lightblue')
            # current.draw_walls(canvas)
            # canvas.update()
            # canvas.after(50)  # 100ms delay
            if current == end:
                break

            # Check all possible moves
            directions = [
                ('top', 0, -1),
                ('right', 1, 0),
                ('bottom', 0, 1),
                ('left', -1, 0)
            ]

            for direction, dx, dy in directions:
                # Check if wall is open
                if not current.walls[direction]:
                    nx, ny = current.x + dx, current.y + dy
                    neighbor = self.get_cell(nx, ny)
                    
                    if neighbor and neighbor not in came_from:
                        if self.has_42 and neighbor in self.cells42:
                            continue
                        came_from[neighbor] = current
                        queue.append(neighbor)
        
        # Reconstruct path
        if end not in came_from:
            return []  # No path found
        
        path = []
        current = end
        
        while current is not None:
            path.insert(0, (current.x, current.y))
            current = came_from[current]
        
        self.solution_path = [self.cells[y][x]
                              for x, y in path]
        return path

    def path_to_directions(self):
        if not self.solution_path:
            return []
        
        directions = []
        for i in range(1, len(self.solution_path)):
            current = self.solution_path[i - 1]
            next_cell = self.solution_path[i]
            dx = next_cell.x - current.x
            dy = next_cell.y - current.y
            
            if dx == 1 and dy == 0:
                directions.append('E')
            elif dx == -1 and dy == 0:
                directions.append('W')
            elif dx == 0 and dy == 1:
                directions.append('S')
            elif dx == 0 and dy == -1:
                directions.append('N')
            else:
                print("Invalid path step")
        
        return ''.join(directions)

    def write_to_file(self, filename='output_maze.txt'):
        with open(filename, 'w') as f:
            for row in self.cells:
                row_string = ''
                for cell in row:
                    value = 0
                    if cell.walls['top']:
                        value |= 1 << 0
                    if cell.walls['right']:
                        value |= 1 << 1
                    if cell.walls['bottom']:
                        value |= 1 << 2
                    if cell.walls['left']:
                        value |= 1 << 3
                    row_string += f"{value:X}"
                row_string += '\n'
                f.write(row_string)

            f.write('\n')
            f.write(f"{self.entry[0]},{self.entry[1]}\n")
            f.write(f"{self.exit[0]},{self.exit[1]}\n")
            f.write(f"{self.path_to_directions()}\n")

class MazeRenderer():
    def __init__(self, maze: Maze):
        self.maze = maze
        self.path_shown = True
        self.solution = []
        self.solution_index = 0
        self.solution_animated = False
        self.root = tk.Tk()
        self.root.title("Cell Test")

        self.wall_color = 'black'
        self.current_color_index = 0
        self.colors = ['lightgrey', 'lightyellow', 'lightpink', 'lightblue']
        self.root.bind('1', lambda e: self.regenerate())
        self.root.bind('2', lambda e: self.toggle_path())
        self.root.bind('3', lambda e: self.change_color())
        self.root.bind('4', lambda e: self.quit())

        CELL_SIZE = 50
        PADDING = 20
        canvas_width  = self.maze.width  * CELL_SIZE + PADDING * 2
        canvas_height = self.maze.height * CELL_SIZE + PADDING * 2

        self.canvas = tk.Canvas(self.root, width=canvas_width, height=canvas_height, bg='white')
        self.canvas.pack()

    def draw_42(self):
        if self.maze.has_42:
            for cell in self.maze.cells42:
                cell.draw_current_cell(self.canvas, color='black')
                cell.draw_walls(self.canvas)

    def draw(self):
        color = self.colors[self.current_color_index]
        self.canvas.delete("all")
        for row in self.maze.cells:
            for cell in row:
                if cell in self.maze.cells42:
                    continue
                if cell.visited:
                    cell.draw_current_cell(self.canvas, color)
                else:
                    cell.draw_current_cell(self.canvas, color='white')
                cell.draw_walls(self.canvas)

        self.maze.current_cell.draw_current_cell(self.canvas, color='salmon')

    def render_DFS(self):
        try:
            self.maze.generate()
            start_x, start_y = self.maze.entry
            start_cell = self.maze.cells[start_y][start_x]
            stack = [start_cell]
            start_cell.visited = True

            while stack:
                self.maze.DFS_generator(stack)
                self.draw()
                self.draw_42()
                self.root.update()
        except Exception as e:
            print("Error:", e)

    def render(self):
        # self.maze.generate()
        self.render_DFS()

        self.maze.find_shortest_path()
        self.animate_solution()
        self.maze.write_to_file()

    def gameloop(self):
        self.root.mainloop()

    def animate_solution(self):
        """Animate the solution path with visual feedback."""
        if not self.maze.solution_path:
            return
        if not self.canvas.winfo_exists():
            return

        # Initialize animation on first call
        if self.solution_index == 0:
            self.solution = self.maze.solution_path.copy()
        
        # Draw all solution cells up to current index
        for i, cell in enumerate(self.solution[:self.solution_index + 1]):
            color = 'lightgreen' if i < self.solution_index else 'red'
            cell.draw_current_cell(self.canvas, color=color)
            cell.draw_walls(self.canvas)
        
        self.solution_index += 1
        
        # Continue animation or reset
        if self.solution_index < len(self.solution):
            self.root.after(100, self.animate_solution)
        else:
            self.solution_animated = True
            self.path_shown = True
            self.toggle_path()

    def regenerate(self):
        """Regenerate the maze with proper cleanup and reset."""
        try:
            self.canvas.delete("all")
        except Exception as e:
            print(f"Canvas error: {e}")
            return

        self.maze = Maze(self.maze.height,
                         self.maze.width,
                         self.maze.entry,
                         self.maze.exit,
                         self.maze.perfect,
                         self.maze.seed)
        self.solution_animated = False
        self.solution_index = 0
        self.solution = []
        self.maze.solution_path = None
        
        # 5. Find solution path
        self.solution = self.maze.find_shortest_path()
        
        # 6. Render (ensure canvas exists first)
        if self.canvas.winfo_exists():
            self.render()
            self.toggle_path()

    def toggle_path(self):
        """Toggle solution path visibility."""
        if not self.maze.solution_path:
            print("No solution path found!")
            return
        
        if not self.canvas.winfo_exists():
            return

        try:
            # Only show path if animation is complete
            if self.path_shown and not self.solution_animated:
                return
            
            color = self.colors[self.current_color_index]
            for c in self.maze.solution_path:
                c.draw_current_cell(self.canvas, color='lightgreen' if self.path_shown else color)
                c.draw_walls(self.canvas)
            self.path_shown = not self.path_shown
        except Exception as e:
            print(f"Toggle path error: {e}")

    def change_color(self):
        """Change maze cell colors."""
        if not self.canvas.winfo_exists():
            return

        try:
            self.current_color_index = (self.current_color_index + 1) % len(self.colors)
            color = self.colors[self.current_color_index]
            for row in self.maze.cells:
                for c in row:
                    c.draw_current_cell(self.canvas, color=color)
                    c.draw_walls(self.canvas)
                    if c in self.maze.cells42:
                        c.draw_current_cell(self.canvas, color='black')
                        c.draw_walls(self.canvas)
            self.path_shown =  not self.path_shown
            self.toggle_path()
        except Exception as e:
            print(f"Change color error: {e}")

    def quit(self):
        self.root.quit()
        self.root.destroy()
