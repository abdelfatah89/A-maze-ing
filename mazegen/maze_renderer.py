from .maze import Maze
import tkinter as tk


class MazeRenderer():
    def __init__(self, maze: Maze) -> None:
        self.maze = maze
        self.path_shown = True
        self.solution_index = 0
        self.solution_animated = False

        self.root = tk.Tk()
        self.root.title("Cell Test")

        self.wall_color = 'black'
        self.current_color_index = 0
        self.colors = [
            'lightgrey', 'lightyellow',
            'lightpink', 'lightblue']

        self.root.bind('1', lambda e: self.regenerate())
        self.root.bind('2', lambda e: self.toggle_path())
        self.root.bind('3', lambda e: self.change_color())
        self.root.bind('4', lambda e: self.quit())

        CELL_SIZE = 50
        PADDING = 20
        canvas_width = self.maze.width * CELL_SIZE + PADDING * 2
        canvas_height = self.maze.height * CELL_SIZE + PADDING * 2

        self.canvas = tk.Canvas(self.root,
                                width=canvas_width,
                                height=canvas_height,
                                bg='white')
        self.canvas.pack()

        # Info label for controls (bottom)
        self.controls_label = tk.Label(
            self.root,
            text=(
                "Controls:\n"
                "  1 – Regenerate   |   2 – Toggle Path  "
                "|  3 – Change Color |   4 – Quit"
                ),
            font=("Arial", 12, "bold"),
            anchor="center"
        )

        self.window_opened = True
        self.root.protocol("WM_DELETE_WINDOW", self.on_window_close)

    def on_window_close(self) -> None:
        self.window_opened = False
        self.root.destroy()

    def draw_42(self) -> None:
        if not self.canvas.winfo_exists():
            return
        if not self.root.winfo_exists():
            return

        try:
            if self.maze.has_42:
                for cell in self.maze.cells42:
                    cell.draw_current_cell(self.canvas, color='black')
        except tk.TclError:
            self.window_opened = False
        except Exception as e:
            print(f"Error drawing 42 pattern: {e}")

    def draw(self) -> None:
        if not self.canvas.winfo_exists():
            return
        if not self.root.winfo_exists():
            return

        try:
            color = self.colors[self.current_color_index]
            self.canvas.delete("all")
            for row in self.maze.cells:
                for cell in row:
                    if cell in self.maze.cells42:
                        continue
                    if cell.visited:
                        cell.draw_current_cell(self.canvas, color)
                    elif (self.maze.algorithm.name == "prim"
                          and cell in self.maze.algorithm.frontier):
                        cell.draw_current_cell(self.canvas, color='green')
                    else:
                        cell.draw_current_cell(self.canvas, color='white')

            if self.maze.algorithm.current_cell is not None:
                self.maze.algorithm.current_cell.draw_current_cell(
                    self.canvas, color='salmon')

        except tk.TclError:
            self.window_opened = False
        except Exception as e:
            print(f"Draw error: {e}")

    def maze_animation(self) -> None:
        while True:
            still_running = self.maze.algorithm.step()
            self.draw()
            self.draw_42()
            self.root.update()
            if not still_running:
                break

    def render(self) -> None:
        if not self.canvas.winfo_exists():
            return
        if not self.root.winfo_exists():
            return

        try:
            if not self.maze.perfect:
                self.maze.add_loops()
            if self.maze.width >= 10 and self.maze.height >= 6:
                self.maze.add_42()

            if not self.maze.animation:
                self.maze.algorithm.generator()
                self.draw()
                self.draw_42()
            elif self.maze.animation:
                self.maze_animation()

            if self.maze.algorithm.current_cell is not None:
                color = self.colors[self.current_color_index]
                self.maze.algorithm.current_cell.draw_current_cell(
                    self.canvas, color)
            self.maze.find_shortest_path()
            self.animate_solution()
            self.maze.write_to_file()

        except tk.TclError:
            self.window_opened = False
        except Exception as e:
            print("Error in render:", e)

    def gameloop(self) -> None:
        self.root.mainloop()

    def animate_solution(self) -> None:
        """Animate the solution path with visual feedback."""
        if not self.canvas.winfo_exists():
            return
        if not self.root.winfo_exists():
            return

        try:
            if not self.maze.solution_path:
                return
            # Initialize animation on first call
            if self.solution_index == 0:
                self.solution = self.maze.solution_path.copy()

            # Draw all solution cells up to current index
            for i, cell in enumerate(self.solution[:self.solution_index + 1]):
                color = 'lightgreen' if i < self.solution_index else 'red'
                cell.draw_current_cell(self.canvas, color=color)

            self.solution_index += 1

            # Continue animation or reset
            if self.solution_index < len(self.solution):
                self.root.after(100, self.animate_solution)
            else:
                self.solution_animated = True
                self.path_shown = True
                self.toggle_path()

        except tk.TclError:
            self.window_opened = False
        except Exception as e:
            print(f"Animate solution error: {e}")

    def regenerate(self) -> None:
        """Regenerate the maze with proper cleanup and reset."""
        if not self.canvas.winfo_exists():
            return
        if not self.root.winfo_exists():
            return

        try:
            self.canvas.delete("all")

            self.maze = Maze(
                self.maze.height,
                self.maze.width,
                self.maze.entry,
                self.maze.exit,
                self.maze.perfect,
                self.maze.algorithm.name,
                self.maze.animation,
                self.maze.seed
            )

            self.solution_animated = False
            self.solution_index = 0
            self.maze.solution_path = []

            # 6. Render (ensure canvas exists first)
            if self.canvas.winfo_exists():
                self.render()
                self.toggle_path()
        except tk.TclError:
            self.window_opened = False
        except Exception as e:
            print(f"Canvas error: {e}")
            return

    def toggle_path(self) -> None:
        """Toggle solution path visibility."""
        if not self.canvas.winfo_exists():
            return
        if not self.root.winfo_exists():
            return

        try:
            if not self.maze.solution_path:
                print("No solution path found!")
                return

            # Only show path if animation is complete
            if self.path_shown and not self.solution_animated:
                return

            color = self.colors[self.current_color_index]
            for c in self.maze.solution_path:
                c.draw_current_cell(self.canvas,
                                    color='lightgreen'
                                    if self.path_shown else color)
            self.path_shown = not self.path_shown
        except tk.TclError:
            self.window_opened = False
        except Exception as e:
            print(f"Toggle path error: {e}")

    def change_color(self) -> None:
        """Change maze cell colors."""
        if not self.canvas.winfo_exists():
            return
        if not self.root.winfo_exists():
            return

        try:
            self.current_color_index = ((self.current_color_index + 1)
                                        % len(self.colors))
            color = self.colors[self.current_color_index]
            for row in self.maze.cells:
                for c in row:
                    c.draw_current_cell(self.canvas, color=color)
                    if c in self.maze.cells42:
                        c.draw_current_cell(self.canvas, color='black')
            self.path_shown = not self.path_shown
            self.toggle_path()
        except tk.TclError:
            self.window_opened = False
        except Exception as e:
            print(f"Change color error: {e}")

    def quit(self) -> None:
        try:
            self.canvas.destroy()
            self.root.quit()
            self.root.destroy()
        except Exception as e:
            print(f"Quit error: {e}")
