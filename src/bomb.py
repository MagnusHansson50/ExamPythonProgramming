from src.pickups import Item


class Bomb:
    def __init__(self, x, y, grid, countdown=3, symbol = "B"):
        self.pos_x = x
        self.pos_y = y
        self.countdown = countdown  #Exploderar efter 3 spelar drag som default
        self.symbol = symbol

        current_item_at_bomb_pos = grid.get(x, y) # Hämta nuvarande Item på positionen där vi vill sätta bomben

        #Spara original Item om det är Exit
        if isinstance(current_item_at_bomb_pos, Item) and current_item_at_bomb_pos.symbol == "E":
            self.original_item = current_item_at_bomb_pos
        else:
            self.original_item = None

        grid.set(x, y, symbol)

    def tick(self):
        """Räknar ner countdown med 1. Returnerar True om en bomb ska explodera."""
        self.countdown -= 1
        return self.countdown <= 0