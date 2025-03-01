class Bomb:
    def __init__(self, x, y, grid, countdown=3, symbol = "B"):
        self.pos_x = x
        self.pos_y = y
        self.countdown = countdown  #Exploderar efter 3 spelar drag som default
        self.symbol = symbol
        grid.set(x, y, symbol)

    def tick(self):
        """Räknar ner countdown med 1. Returnerar True om en bomb ska explodera."""
        self.countdown -= 1
        return self.countdown <= 0