# A-maze-ing

A Python maze generator and visualizer with multiple algorithms and
optional animation. The app reads a config file, generates a maze,
shows it in a Tkinter window, and writes an output file with walls
and the solved path.

## Features

- Three algorithms: DFS, Prim, Hunt-and-Kill (HAK)
- Perfect or loopy mazes (toggle with `PERFECT`)
- Optional animation of generation
- Built-in shortest path solver (BFS)
- Optional "42" easter-egg pattern for larger mazes
- Tkinter UI with keyboard controls
- Reproducible mazes with `SEED`

## Requirements

- Python 3.11+
- Tkinter (usually included with Python on Windows)

## Quick Start

1. Edit the config file [config.txt](config.txt) (see below).
2. Run:

```bash
python a_maze_ing.py config.txt
```

This opens a window, generates the maze, animates the solution path,
and writes the output file (see `OUTPUT_FILE` in the config).

## Configuration

The app reads key/value pairs from a config file like [config.txt](config.txt):

```ini
WIDTH=20
HEIGHT=20
ENTRY=0,0
EXIT=19,19
OUTPUT_FILE=maze.txt
ALGORITHM=prim
PERFECT=True
ANIMATION=False
SEED=42
```

### Config keys

- `WIDTH` (int): Maze width, must be > 3
- `HEIGHT` (int): Maze height, must be > 3
- `ENTRY` (x,y): Entry coordinates
- `EXIT` (x,y): Exit coordinates
- `OUTPUT_FILE` (str): Output file path
- `ALGORITHM` (str): `dfs`, `prim`, or `hak`
- `PERFECT` (bool): `True` for perfect maze, `False` to add loops
- `ANIMATION` (bool): `True` to animate generation
- `SEED` (int or None): Reproducible randomness

To switch algorithms, **only change** `ALGORITHM` in the config file.
No code changes are needed.

## Controls (Tkinter window)

- `1`: Regenerate maze with current config
- `2`: Toggle solution path visibility
- `3`: Cycle cell colors
- `4`: Quit

## Output Format

The output file (default `maze.txt`) contains:

1. One line per maze row, each cell as a hex digit (bitmask of walls)
2. Entry coordinates: `x,y`
3. Exit coordinates: `x,y`
4. Path directions as `N`, `S`, `E`, `W`

## How It Works (High Level)

- [a_maze_ing.py](a_maze_ing.py) loads the config and starts rendering
- [mazegen/maze.py](mazegen/maze.py) stores grid, walls, and helpers
- [mazegen/algorithm.py](mazegen/algorithm.py) implements algorithms
- [mazegen/maze_renderer.py](mazegen/maze_renderer.py) handles UI

## Add a New Algorithm

To add a new algorithm (so you can still switch it via `ALGORITHM` only):

1. **Implement the algorithm**
	- Add a class in [mazegen/algorithm.py](mazegen/algorithm.py)
	- Subclass `MazeAlgorithm`
	 - Implement `step()` and `generator()`
	- Set a unique `self.name` (lowercase)

### Algorithm contract (norms)

When you create a new algorithm class, follow these rules:

- `step()` must return `True` while generation should continue, and
	`False` when the algorithm is finished.
- `generator()` must fully generate the maze by repeatedly calling
	`step()` until completion.
- Update `self.current_cell` to the cell currently being processed
	(used for animation).
- If your algorithm uses a frontier/queue/stack for animation, store
	it in `self.frontier` (list of `Cell`) so the renderer can highlight it.
- Mark visited cells by setting `cell.visited = True`.
- Use `maze.remove_walls(current, next)` to carve passages.

2. **Register it in the maze**
	- Update the selection logic in [mazegen/maze.py](mazegen/maze.py)
	- Add an `elif algorithm == "your_name"` branch

3. **Allow it in the config**
	- Update the allowed values in
	  [mazegen/config_parser.py](mazegen/config_parser.py)

After that, you can switch to your algorithm by editing only:

```ini
ALGORITHM=your_name
```

## Development Notes

- The project is packaged as `mazegen`
- Optional dev tools in `pyproject.toml`: `pytest`, `mypy`, `flake8`
- A classic packaging entry point exists in [setup.py](setup.py)
	(for sdist/wheel builds or older tooling)

## Running with Makefile (optional)

On Windows, the `Makefile` may require `make` to be installed. If you
have it, you can run:

```bash
make install
make run
```
