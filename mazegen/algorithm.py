import random
from .cell import Cell
from abc import ABC, abstractmethod
from .maze import Maze
from typing import List, Optional


class MazeAlgorithm(ABC):
    def __init__(self, maze: Maze) -> None:
        self.maze = maze
        self.name: str = ""
        self.current_cell: Optional[Cell] = None
        self.frontier: List[Cell] = []

    @abstractmethod
    def step(self) -> bool:
        pass

    @abstractmethod
    def generator(self) -> None:
        pass


class DfsAlgorithm(MazeAlgorithm):
    def __init__(self, maze: Maze) -> None:
        super().__init__(maze)
        self.maze = maze
        self.name: str = 'dfs'
        self.current_cell: Optional[Cell] = None

        start_x, start_y = self.maze.entry
        start_cell = self.maze.cells[start_y][start_x]
        self.stack = [start_cell]
        start_cell.visited = True

    def step(self) -> bool:
        try:
            self.current_cell = self.stack[-1]
            neighbors = self.maze.get_neighbors(self.current_cell)
            unvisited_neighbors = [
                neighbor
                for neighbor in neighbors
                if not neighbor.visited
            ]

            if unvisited_neighbors:
                next_cell = random.choice(unvisited_neighbors)
                self.maze.remove_walls(self.current_cell, next_cell)
                next_cell.visited = True
                self.stack.append(next_cell)
            else:
                self.stack.pop()
            return True
        except Exception as e:
            print("Error generator:", e)
            return False

    def generator(self) -> None:
        try:
            while self.stack:
                self.step()
        except Exception as e:
            print("Error generator:", e)


class PrimAlgorithm(MazeAlgorithm):
    def __init__(self, maze: Maze) -> None:
        self.maze = maze
        self.name: str = 'prim'
        self.started: bool = False
        self.current_cell: Optional[Cell] = None
        self.frontier: List[Cell] = []

    def step(self) -> bool:
        if not self.started:
            entry_cell = self.maze.get_cell(*self.maze.entry)
            if entry_cell is None:
                return False
            entry_cell.visited = True
            self.frontier = self.maze.get_neighbors(entry_cell)
            self.current_cell = entry_cell
            self.started = True
            return True

        if not self.frontier:
            return False

        self.current_cell = random.choice(self.frontier)
        self.frontier.remove(self.current_cell)
        self.current_cell.visited = True

        neighbors = self.maze.get_neighbors(self.current_cell)

        visited_neighbors = [cell for cell in neighbors
                             if cell.visited
                             and cell not in self.maze.cells42]

        unvisited_neighbors = [cell for cell in neighbors
                               if not cell.visited]

        if visited_neighbors and self.current_cell not in self.maze.cells42:
            self.maze.remove_walls(self.current_cell,
                                   random.choice(visited_neighbors))

        if not unvisited_neighbors:
            return True

        for cell in unvisited_neighbors:
            if cell not in self.frontier:
                self.frontier.append(cell)
        return True

    def generator(self) -> None:
        self.started = False
        self.frontier = []
        if not self.started:
            self.step()
        while self.frontier:
            self.step()


class HakAlgorithm(MazeAlgorithm):
    def __init__(self, maze: Maze) -> None:
        self.maze = maze
        self.name: str = 'hak'

        start_x, start_y = self.maze.entry
        self.current_cell: Optional[Cell] = self.maze.cells[start_y][start_x]
        if self.current_cell is None:
            raise ValueError(
                "Failed to initialize current cell in HakAlgorithm")
        self.current_cell.visited = True
        self.maze.cells42 = self.maze.add_42()

    def step(self) -> bool:
        unvisited_neighbors = [
            cell for cell in self.maze.get_neighbors(self.current_cell)
            if not cell.visited]

        if unvisited_neighbors:
            next_cell = random.choice(unvisited_neighbors)
            if next_cell not in self.maze.cells42:
                self.maze.remove_walls(self.current_cell, next_cell)
                next_cell.visited = True
                self.current_cell = next_cell
            return True

        found = False
        for row in self.maze.cells:
            for cell in row:
                if not cell.visited:
                    self.current_cell = cell
                    visited_neighbors = [
                        c for c in self.maze.get_neighbors(self.current_cell)
                        if c.visited and c not in self.maze.cells42]
                    if visited_neighbors:
                        self.current_cell = cell
                        neighbor = random.choice(visited_neighbors)
                        self.maze.remove_walls(cell, neighbor)
                        cell.visited = True
                        found = True
                        break
            if found:
                break
        return found

    def generator(self) -> None:
        while True:
            if not self.step():
                break
