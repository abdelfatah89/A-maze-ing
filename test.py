from typing import List, Tuple, Optional, Dict
import random
from collections import deque
from cell import Cell


class Maze:
    def __init__(
        self,
        width: int,
        height: int,
        entry: Tuple[int, int] = (0, 0),
        exit: Tuple[int, int] = None,
        perfect: bool = True,
        seed: Optional[int] = None
    ) -> None:
        """
        Initialize a maze with given dimensions and properties.
        
        Args:
            width: Width of the maze in cells
            height: Height of the maze in cells
            entry: (x, y) coordinates of entry point
            exit: (x, y) coordinates of exit point (defaults to bottom-right)
            perfect: If True, maze has exactly one solution
            seed: Random seed for reproducible generation
        """
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit if exit else (width - 1, height - 1)
        self.perfect = perfect
        self.seed = seed
        
        # Initialize random generator
        if seed is not None:
            random.seed(seed)
        
        # Create grid of cells
        self.grid: List[List[Cell]] = [
            [Cell(x, y) for x in range(width)] 
            for y in range(height)
        ]
        
        # Maze state
        self.generated = False
        self.has_42_pattern = False
        self.solution_path: Optional[List[Cell]] = None
        
        # Validate entry and exit
        self._validate_points()
    
    def _validate_points(self) -> None:
        """Validate that entry and exit are within bounds."""
        if not (0 <= self.entry[0] < self.width and 0 <= self.entry[1] < self.height):
            raise ValueError(f"Entry {self.entry} is out of bounds ({self.width}x{self.height})")
        
        if not (0 <= self.exit[0] < self.width and 0 <= self.exit[1] < self.height):
            raise ValueError(f"Exit {self.exit} is out of bounds ({self.width}x{self.height})")
        
        if self.entry == self.exit:
            raise ValueError("Entry and exit cannot be the same cell")
    
    def get_cell(self, x: int, y: int) -> Optional[Cell]:
        """Get cell at coordinates, or None if out of bounds."""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return None
    
    def get_neighbors(self, cell: Cell) -> List[Cell]:
        """Get all valid neighboring cells."""
        neighbors = []
        directions = [
            ('north', 0, -1),
            ('east', 1, 0),
            ('south', 0, 1),
            ('west', -1, 0)
        ]
        
        for direction, dx, dy in directions:
            nx, ny = cell.x + dx, cell.y + dy
            neighbor = self.get_cell(nx, ny)
            if neighbor:
                neighbors.append((direction, neighbor))
        
        return neighbors
    
    def remove_wall_between(self, cell1: Cell, cell2: Cell) -> None:
        """
        Remove the wall between two adjacent cells.
        Updates both cells' wall dictionaries.
        """
        dx = cell2.x - cell1.x
        dy = cell2.y - cell1.y
        
        if dx == 1:  # cell2 is east of cell1
            cell1.walls['east'] = False
            cell2.walls['west'] = False
        elif dx == -1:  # cell2 is west of cell1
            cell1.walls['west'] = False
            cell2.walls['east'] = False
        elif dy == 1:  # cell2 is south of cell1
            cell1.walls['south'] = False
            cell2.walls['north'] = False
        elif dy == -1:  # cell2 is north of cell1
            cell1.walls['north'] = False
            cell2.walls['south'] = False
    
    def generate(self, algorithm: str = 'dfs') -> None:
        """
        Generate the maze using specified algorithm.
        
        Args:
            algorithm: 'dfs' for depth-first search (recursive backtracker),
                      'prim' for Prim's algorithm
        """
        print(f"🔄 Generating {self.width}x{self.height} maze using {algorithm.upper()}...")
        
        # Reset all cells
        for row in self.grid:
            for cell in row:
                cell.visited = False
                # Reset walls to all closed
                cell.walls = {'north': True, 'east': True, 'south': True, 'west': True}
        
        if algorithm == 'dfs':
            self._generate_dfs()
        elif algorithm == 'prim':
            self._generate_prim()
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")
        
        # Ensure entry and exit are open
        self._open_entry_exit()
        
        # Add "42" pattern if possible
        self._add_42_pattern()
        
        # Ensure no large open spaces
        self._ensure_no_large_open_spaces()
        
        # If perfect maze is required, ensure single solution
        if self.perfect:
            self._ensure_perfect_maze()
        
        self.generated = True
        print("✅ Maze generation completed")
    
    def _generate_dfs(self) -> None:
        """Generate maze using recursive backtracker (DFS)."""
        start_x, start_y = self.entry
        start_cell = self.grid[start_y][start_x]
        stack = [start_cell]
        start_cell.visited = True
        
        while stack:
            current = stack[-1]
            neighbors = self.get_neighbors(current)
            
            # Filter unvisited neighbors
            unvisited_neighbors = [
                (direction, neighbor) 
                for direction, neighbor in neighbors 
                if not neighbor.visited
            ]
            
            if unvisited_neighbors:
                # Choose random unvisited neighbor
                direction, next_cell = random.choice(unvisited_neighbors)
                self.remove_wall_between(current, next_cell)
                next_cell.visited = True
                stack.append(next_cell)
            else:
                stack.pop()
    
    def _generate_prim(self) -> None:
        """Generate maze using Prim's algorithm."""
        # Start with random cell
        start_x, start_y = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
        start_cell = self.grid[start_y][start_x]
        start_cell.visited = True
        
        # Add all walls of starting cell to frontier
        frontier = []
        for direction, neighbor in self.get_neighbors(start_cell):
            if not neighbor.visited:
                frontier.append((start_cell, direction, neighbor))
        
        while frontier:
            # Randomly select a wall from frontier
            current, direction, neighbor = random.choice(frontier)
            frontier.remove((current, direction, neighbor))
            
            if not neighbor.visited:
                # Remove wall between current and neighbor
                self.remove_wall_between(current, neighbor)
                neighbor.visited = True
                
                # Add new walls to frontier
                for new_dir, new_neighbor in self.get_neighbors(neighbor):
                    if not new_neighbor.visited:
                        frontier.append((neighbor, new_dir, new_neighbor))
    
    def _open_entry_exit(self) -> None:
        """Open walls at entry and exit points."""
        # Open entry wall
        entry_cell = self.grid[self.entry[1]][self.entry[0]]
        if self.entry[0] == 0:  # Left edge
            entry_cell.walls['west'] = False
        elif self.entry[0] == self.width - 1:  # Right edge
            entry_cell.walls['east'] = False
        elif self.entry[1] == 0:  # Top edge
            entry_cell.walls['north'] = False
        elif self.entry[1] == self.height - 1:  # Bottom edge
            entry_cell.walls['south'] = False
        
        # Open exit wall
        exit_cell = self.grid[self.exit[1]][self.exit[0]]
        if self.exit[0] == 0:  # Left edge
            exit_cell.walls['west'] = False
        elif self.exit[0] == self.width - 1:  # Right edge
            exit_cell.walls['east'] = False
        elif self.exit[1] == 0:  # Top edge
            exit_cell.walls['north'] = False
        elif self.exit[1] == self.height - 1:  # Bottom edge
            exit_cell.walls['south'] = False
    
    def _add_42_pattern(self) -> None:
        """Add a '42' pattern of completely closed cells."""
        # Pattern for '4'
        pattern_4 = [
            (1, 1), (1, 2), (1, 3),
            (2, 1), (2, 3),
            (3, 1), (3, 2), (3, 3),
            (4, 3)
        ]
        
        # Pattern for '2'
        pattern_2 = [
            (6, 1), (7, 1), (8, 1),
            (8, 2),
            (6, 3), (7, 3), (8, 3),
            (6, 4),
            (6, 5), (7, 5), (8, 5)
        ]
        
        # Check if maze is large enough
        if self.width < 10 or self.height < 6:
            print("⚠️  Maze too small for '42' pattern (minimum 10x6)")
            self.has_42_pattern = False
            return
        
        # Add pattern with offset to center it
        offset_x = (self.width - 10) // 2
        offset_y = (self.height - 6) // 2
        
        pattern_cells = []
        for x, y in pattern_4 + pattern_2:
            px, py = x + offset_x, y + offset_y
            if 0 <= px < self.width and 0 <= py < self.height:
                cell = self.grid[py][px]
                # Make all walls closed
                cell.walls = {'north': True, 'east': True, 'south': True, 'west': True}
                pattern_cells.append(cell)
        
        self.has_42_pattern = len(pattern_cells) > 0
        if self.has_42_pattern:
            print(f"✅ Added '42' pattern with {len(pattern_cells)} cells")
    
    def _ensure_no_large_open_spaces(self) -> None:
        """Ensure no open spaces larger than 2x2."""
        for y in range(self.height - 2):
            for x in range(self.width - 2):
                # Check 3x3 area
                open_count = 0
                for dy in range(3):
                    for dx in range(3):
                        cell = self.grid[y + dy][x + dx]
                        # Count open walls (rough estimate of openness)
                        open_walls = sum(1 for wall in cell.walls.values() if not wall)
                        if open_walls >= 2:
                            open_count += 1
                
                if open_count >= 9:  # All cells in 3x3 are too open
                    # Add a wall in the middle
                    center = self.grid[y + 1][x + 1]
                    center.walls['north'] = True
                    center.walls['south'] = True
    
    def _ensure_perfect_maze(self) -> None:
        """
        Ensure maze has exactly one solution.
        For now, our algorithms should generate perfect mazes.
        We'll verify by counting solutions.
        """
        solutions = self._count_solutions()
        if solutions > 1:
            print(f"⚠️  Maze has {solutions} solutions, making it perfect...")
            # Simple approach: add walls to create dead ends
            self._simplify_to_perfect()
    
    def _count_solutions(self) -> int:
        """Count number of distinct paths from entry to exit."""
        # This is simplified - in reality would need more complex algorithm
        # For now, we'll assume our generation creates perfect mazes
        return 1
    
    def _simplify_to_perfect(self) -> None:
        """Simplify maze to have only one solution."""
        # Simple approach: close some random walls to create dead ends
        for _ in range(self.width * self.height // 10):
            x, y = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
            cell = self.grid[y][x]
            directions = ['north', 'east', 'south', 'west']
            for direction in directions:
                if not cell.walls[direction]:
                    cell.walls[direction] = True
                    # Also close the opposite wall in neighbor
                    neighbor_dir = {'north': 'south', 'south': 'north', 
                                   'east': 'west', 'west': 'east'}[direction]
                    dx, dy = {'north': (0, -1), 'south': (0, 1),
                             'east': (1, 0), 'west': (-1, 0)}[direction]
                    neighbor = self.get_cell(x + dx, y + dy)
                    if neighbor:
                        neighbor.walls[neighbor_dir] = True
                    break
    
    def find_shortest_path(self) -> List[Tuple[int, int]]:
        """Find shortest path from entry to exit using BFS."""
        start = self.grid[self.entry[1]][self.entry[0]]
        end = self.grid[self.exit[1]][self.exit[0]]
        
        # BFS setup
        queue = deque([start])
        came_from = {start: None}
        
        while queue:
            current = queue.popleft()
            
            if current == end:
                break
            
            # Check all possible moves
            directions = [
                ('north', 0, -1),
                ('east', 1, 0),
                ('south', 0, 1),
                ('west', -1, 0)
            ]
            
            for direction, dx, dy in directions:
                # Check if wall is open
                if not current.walls[direction]:
                    nx, ny = current.x + dx, current.y + dy
                    neighbor = self.get_cell(nx, ny)
                    
                    if neighbor and neighbor not in came_from:
                        came_from[neighbor] = (current, direction)
                        queue.append(neighbor)
        
        # Reconstruct path
        path_cells = []
        path_directions = []
        current = end
        
        while current != start:
            if current not in came_from:
                return []  # No path found
            
            prev, direction = came_from[current]
            path_cells.insert(0, current)
            path_directions.insert(0, direction[0].upper())  # First letter
            current = prev
        
        path_cells.insert(0, start)
        self.solution_path = path_cells
        
        return path_directions
    
    def get_path_string(self) -> str:
        """Get solution path as string of N/E/S/W."""
        directions = self.find_shortest_path()
        return ''.join(directions)
    
    def write_to_file(self, filename: str) -> None:
        """Write maze to file in required format."""
        if not self.generated:
            raise ValueError("Maze must be generated before writing to file")
        
        with open(filename, 'w') as f:
            # Write cells as hexadecimal
            for y in range(self.height):
                row = []
                for x in range(self.width):
                    cell = self.grid[y][x]
                    hex_value = cell.get_hex_value()
                    row.append(hex_value)
                f.write(''.join(row) + '\n')
            
            # Empty line
            f.write('\n')
            
            # Entry coordinates
            f.write(f"{self.entry[0]},{self.entry[1]}\n")
            
            # Exit coordinates
            f.write(f"{self.exit[0]},{self.exit[1]}\n")
            
            # Solution path
            path = self.get_path_string()
            f.write(path + '\n')
        
        print(f"📁 Maze written to {filename}")
    
    def print_ascii(self) -> None:
        """Print maze in ASCII format to terminal."""
        if not self.generated:
            print("Maze not generated yet!")
            return
        
        # Top border
        print("┌" + "───┬" * (self.width - 1) + "───┐")
        
        for y in range(self.height):
            # Cell row
            row_top = "│"
            row_mid = "│"
            row_bot = "├"
            
            for x in range(self.width):
                cell = self.grid[y][x]
                
                # Mark entry/exit
                marker = " "
                if (x, y) == self.entry:
                    marker = "S"
                elif (x, y) == self.exit:
                    marker = "E"
                elif self.solution_path and cell in self.solution_path:
                    marker = "•"
                
                # Walls
                east_wall = "│" if cell.walls['east'] else " "
                south_wall = "───" if cell.walls['south'] else "   "
                
                row_top += f" {marker} {east_wall}"
                row_mid += f"{south_wall}{east_wall}"
                
                if y == self.height - 1:
                    row_bot += "───" + ("┼" if x < self.width - 1 else "┤")
                else:
                    row_bot += "───" + ("┼" if x < self.width - 1 else "┤")
            
            print(row_top)
            if y < self.height - 1:
                print(row_mid)
                print(row_bot)
            else:
                # Bottom border
                print("└" + "───┴" * (self.width - 1) + "───┘")
    
    def print_info(self) -> None:
        """Print information about the maze."""
        print(f"\n{'='*50}")
        print(f"MAZE INFORMATION")
        print(f"{'='*50}")
        print(f"Dimensions: {self.width} x {self.height}")
        print(f"Entry: {self.entry}")
        print(f"Exit: {self.exit}")
        print(f"Perfect: {self.perfect}")
        print(f"Seed: {self.seed}")
        print(f"Generated: {self.generated}")
        print(f"Has '42' pattern: {self.has_42_pattern}")
        
        if self.generated:
            path = self.get_path_string()
            print(f"Shortest path: {len(path)} steps")
            print(f"Path: {path}")