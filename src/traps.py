import sys


class Traps:
    """Representerar saker man kan plocka upp."""
    def __init__(self, name, value=10, symbol="."):
        self.name = name
        self.value = value
        self.symbol = symbol

    def __str__(self):
        return self.symbol


traps = [Traps("trap"), Traps("trap"), Traps("trap")]


def randomize(grid):
    """Placerar ut alla Traps i traps på random position"""
    for trap in traps:
        try:
            x, y = grid.randomize_empty_position_in_grid()
        except RuntimeError as e:
            print(f"Critical error: {e}")
            sys.exit(1)  # Lämnar programmet med en felkod
        else:
            grid.set(x, y, trap)