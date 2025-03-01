class Traps:
    """Representerar saker man kan plocka upp."""
    def __init__(self, name, value=10, symbol="X"):
        self.name = name
        self.value = value
        self.symbol = symbol

    def __str__(self):
        return self.symbol


traps = [Traps("skull"), Traps("skull"), Traps("skull")]


def randomize(grid):
    for trap in traps:
        x, y = grid.randomize_empty_position_in_grid()
        grid.set(x, y, trap)