import sys
from config_parser import MazeConfig
from maze import Maze
from maze_renderer import MazeRenderer


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py <config_file>")
        sys.exit(1)

    config = MazeConfig(sys.argv[1])
    maze = Maze(config.height,
                config.width,
                config.entry,
                config.exit_,
                config.perfect,
                config.algorithm,
                config.animation)
    render = MazeRenderer(maze)
    render.render()
    render.gameloop()
