from src import pickups
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


def update_bombs(p, grid, bombs):
    """Uppdaterar alla bomber och spränger när countdown är 0."""
    for boom in bombs[:]:  # Kopiera listan för att undvika att den ändras under loopen
        if boom.tick():
            explode_bomb(boom, p, grid)
            bombs.remove(boom)  # Ta bort bomben från listan.



def explode_bomb(boom, p, grid):
    """Tar bort allt inom de 8 angränsande rutorna inklusive den som bomben står på"""
    for dx in range(-1, 1 + 1):
        for dy in range(-1, 1 + 1):
            blow_pos_x = (boom.pos_x + dx)
            blow_pos_y = (boom.pos_y + dy)
            x_ok = (blow_pos_x != 0) and (blow_pos_x != (grid.width -1)) # Variabel för att kolla att vi inte spränger ramen
            y_ok = (blow_pos_y != 0) and (blow_pos_y != (grid.height - 1)) # Variabel för att kolla att vi inte spränger ramen
            item_at_position = grid.get(blow_pos_x, blow_pos_y)
            ending_not_at_position = True # Variabel för att kolla att vi inte spränger Exit
            item_is_bomb = False # Variabel för att hålla koll på om det är en annan bomb
            if isinstance(item_at_position, pickups.Item):
                ending_not_at_position = item_at_position.name != "ending"
                p.all_initial_found = p.inventory.remove_from_items_to_pickup_before_end_if_initial(item_at_position)
            if item_at_position == "B" and not ((blow_pos_x, blow_pos_y) == (boom.pos_x, boom.pos_y)):
                item_is_bomb = True
            if x_ok and y_ok and ending_not_at_position and not item_is_bomb: #Ta inte bort om det är ett ram vägg element, exit eller en annan bomb.
                grid.clear(blow_pos_x, blow_pos_y)
            if (p.pos_x, p.pos_y) ==  (boom.pos_x + dx, boom.pos_y + dy):
                p.score -= 50
            if boom.original_item:
                grid.set(boom.pos_x, boom.pos_y, boom.original_item)
    print(f"💥 Bomb exploded 💥 ({boom.pos_x}, {boom.pos_y})!")
