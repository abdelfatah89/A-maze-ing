from typing import Any, Dict, Tuple
import sys


class MazeConfig:
    def __init__(self, config_file: str) -> None:
        self.config_file = config_file
        self.width = 10
        self.height = 10
        self.entry: Tuple[int, int] = (0, 0)
        self.exit_: Tuple[int, int] = (self.width-1, self.height-1)
        self.perfect = True
        self.output_file = "maze.txt"
        self.algorithm = "dfs"
        self.animation = False
        self.seed = None
        self.parse_()

    def parse_(self) -> Dict[str, Any]:
        try:
            config: Dict[str, Any] = {}
            with open(self.config_file, 'r') as file:
                for line in file:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    if '=' not in line:
                        print(f"Warning: Ignoring malformed line: {line}")
                        continue
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip()

            if 'WIDTH' not in config:
                raise ValueError("WIDTH must be provided")
            if not config['WIDTH'].isdigit() or int(config['WIDTH']) <= 0:
                raise ValueError("WIDTH must be a positive integer")

            if 'HEIGHT' not in config:
                raise ValueError("HEIGHT must be provided")
            if not config['HEIGHT'].isdigit() or int(config['HEIGHT']) <= 0:
                raise ValueError("HEIGHT must be a positive integer")
            if int(config['HEIGHT']) <= 3 or int(config['WIDTH']) <= 3:
                raise ValueError("WIDTH and HEIGHT must be greater than 3")

            self.width = int(config['WIDTH'])
            self.height = int(config['HEIGHT'])

            if 'ENTRY' not in config:
                raise ValueError("ENTRY must be provided")
            entry_parts = config['ENTRY'].split(',')
            if len(entry_parts) != 2:
                raise ValueError("ENTRY must be in format x,y")
            try:
                entry_x, entry_y = int(entry_parts[0]), int(entry_parts[1])
            except ValueError:
                raise ValueError("ENTRY coordinates must be integers")
            if not (0 <= entry_x < self.width):
                raise ValueError(
                    "ENTRY coordinates must be within maze bounds")
            if not (0 <= entry_y < self.height):
                raise ValueError(
                    "ENTRY coordinates must be within maze bounds")
            self.entry = (entry_x, entry_y)

            if 'EXIT' not in config:
                raise ValueError("EXIT must be provided")
            exit_parts = config['EXIT'].split(',')
            if len(exit_parts) != 2:
                raise ValueError("EXIT must be in format x,y")
            try:
                exit_x, exit_y = int(exit_parts[0]), int(exit_parts[1])
            except ValueError:
                raise ValueError("EXIT coordinates must be integers")
            if not (0 <= exit_x < self.width):
                raise ValueError(
                    "EXIT coordinates must be within maze bounds")
            if not (0 <= exit_y < self.height):
                raise ValueError(
                    "EXIT coordinates must be within maze bounds")
            self.exit_ = (exit_x, exit_y)

            if self.entry == self.exit_:
                raise ValueError("ENTRY and EXIT must be different")

            if 'PERFECT' not in config:
                raise ValueError("PERFECT must be provided (true or false)")
            perfect_str = config['PERFECT'].lower()
            if perfect_str not in ['true', 'false']:
                raise ValueError("PERFECT must be 'true' or 'false'")
            self.perfect = (perfect_str == 'true')

            if 'OUTPUT_FILE' not in config:
                raise ValueError("OUTPUT_FILE must be provided")
            self.output_file = config['OUTPUT_FILE']
            if not self.output_file:
                raise ValueError("OUTPUT_FILE cannot be empty")

            if "ALGORITHM" in config:
                if config["ALGORITHM"].lower() not in ["dfs", "prim"]:
                    raise ValueError("ALGORITHM must be 'DFS' or 'Prim'")
                self.algorithm = config["ALGORITHM"].lower()

            if 'ANIMATION' not in config:
                raise ValueError("ANIMATION must be provided (true or false)")
            animation_str = config['ANIMATION'].lower()
            if animation_str not in ['true', 'false']:
                raise ValueError("ANIMATION must be 'true' or 'false'")
            self.animation = (animation_str == 'true')

            if 'SEED' in config:
                if not config['SEED'].isdigit():
                    raise ValueError("SEED must be an integer")
                self.seed = int(config['SEED'])

            print("✓ Configuration loaded successfully"
                  f" from '{self.config_file}'")
        except FileNotFoundError:
            print(f"Error: Configuration file '{self.config_file}' not found")
            sys.exit(1)
        except ValueError as e:
            print(f"Configuration error in '{self.config_file}': {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Unexpected error while parsing '{self.config_file}': {e}")
            sys.exit(1)


if __name__ == "__main__":
    config = MazeConfig("config.txt")
    # print(config)

    print("\nUsing config values:")
    print(f"Width: {config.width}")
    print(f"Height: {config.height}")
    print(f"Entry at: {config.entry}")
    print(f"Exit at: {config.exit_}")
