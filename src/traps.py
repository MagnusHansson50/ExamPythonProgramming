class Traps:
    """Representerar saker man kan plocka upp."""
    def __init__(self, name, value=10, symbol="X"):
        self.name = name
        self.value = value
        self.symbol = symbol

    def __str__(self):
        return self.symbol


traps = [Traps("skull")]


def randomize(grid):
    for trap in traps:
        while True:
            # slumpa en position tills vi hittar en som är ledig
            x = grid.get_random_x()
            y = grid.get_random_y()
            if grid.is_empty(x, y):
                grid.set(x, y, trap)
                break  # avbryt while-loopen, fortsätt med nästa varv i for-loopen