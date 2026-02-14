from maze import Maze
import tkinter as tk


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
            start_x, start_y = self.maze.entry
            start_cell = self.maze.cells[start_y][start_x]
            self.maze.stack = [start_cell]
            start_cell.visited = True

            if not self.maze.perfect:
                self.maze.add_loops()
            if self.maze.width >= 10 and self.maze.height >= 6:
                self.maze.add_42()

            while self.maze.stack:
                self.maze.DFS_step()
                self.draw()
                self.draw_42()
                self.root.update()
        except Exception as e:
            print("Error:", e)

    def render(self):
        if not self.maze.animation:
            self.maze.generate()
            self.draw()
            self.draw_42()
        elif self.maze.animation and self.maze.algorithm == 'dfs':
            self.render_DFS()
        elif self.maze.animation and self.maze.algorithm == 'prim':
            self.render_PRIM()

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
                         self.maze.algorithm,
                         self.maze.animation,
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
