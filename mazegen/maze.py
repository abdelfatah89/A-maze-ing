from .cell import Cell
from typing import Dict, List, Tuple, Optional
import random


class Maze():
    def __init__(self, height: int, width: int,
                 entry: Tuple[int, int], exit_: Tuple[int, int],
                 perfect: bool, algorithm: str,
                 animation: bool, seed: Optional[int]) -> None:
        from .algorithm import DfsAlgorithm, PrimAlgorithm
        from .algorithm import HakAlgorithm, MazeAlgorithm
        self.height = height
        self.width = width
        self.entry = entry
        self.exit = exit_ if exit_ else (width - 1, height - 1)
        self.perfect = perfect
        self.cells: List[List[Cell]] = [
            [Cell(x, y) for x in range(self.width)]
            for y in range(self.height)]

        if algorithm == 'dfs':
            self.algorithm: MazeAlgorithm = DfsAlgorithm(self)
        elif algorithm == 'prim':
            self.algorithm = PrimAlgorithm(self)
        elif algorithm == 'hak':
            self.algorithm = HakAlgorithm(self)

        self.animation = animation
        self.seed = seed
        if self.seed is not None:
            random.seed(self.seed)

        self.cells42 = self.add_42()
        self.has_42 = False
        self.solution_path: List[Cell] = []

    def remove_walls(self, current: Optional[Cell],
                     next: Optional[Cell]) -> None:
        if current is None or next is None:
            return
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

    def get_neighbors(self, cell: Optional[Cell]) -> List[Cell]:
        if not cell:
            return []
        neighbors = []
        directions = {
            'top': (0, -1),
            'right': (1, 0),
            'bottom': (0, 1),
            'left': (-1, 0)
        }

        for dx, dy in directions.values():
            dx, dy = cell.x + dx, cell.y + dy
            neighbor = self.get_cell(dx, dy)
            if neighbor:
                neighbors.append(neighbor)

        return neighbors

    def get_cell(self, x: int, y: int) -> Cell | None:
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.cells[y][x]
        return None

    def add_42(self) -> List[Cell]:
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
            return []

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
        for column in self.cells:
            for cell in column:
                if self.cells42 and cell in self.cells42:
                    continue
                # Randomly remove walls to adjacent cells
                if random.random() < loop_probability:
                    # Check right neighbor
                    if cell.x + 1 < self.width:
                        cell.walls['right'] = False
                        self.cells[cell.y][cell.x + 1].walls['left'] = False
                        continue

                if random.random() < loop_probability:
                    # Check bottom neighbor
                    if cell.y + 1 < self.height:
                        cell.walls['bottom'] = False
                        self.cells[cell.y + 1][cell.x].walls['top'] = False

    def find_shortest_path(self) -> List[Tuple[int, int]] | None:
        """Find shortest path from entry
        to exit using BFS with animation."""
        from collections import deque

        start = self.cells[self.entry[1]][self.entry[0]]
        end = self.cells[self.exit[1]][self.exit[0]]

        current: Cell | None
        # BFS setup
        queue = deque([start])
        came_from: Dict[Cell, Cell | None] = {start: None}

        while queue:

            current = queue.popleft()
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
                        came_from[neighbor] = current
                        queue.append(neighbor)

        # Reconstruct path
        if end not in came_from:
            return []  # No path found

        current = end

        while current is not None:
            self.solution_path.insert(0, self.cells[current.y][current.x])
            current = came_from[current]

        return None

    def path_to_directions(self) -> str:
        if not self.solution_path:
            return ""

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

    def write_to_file(self, filename: str = 'output_maze.txt') -> None:
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
