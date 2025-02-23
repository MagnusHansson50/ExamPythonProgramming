import random


class Item:
    """Representerar saker man kan plocka upp."""
    def __init__(self, name, value=10, symbol="?"):
        self.name = name
        self.value = value
        self.symbol = symbol

    def __str__(self):
        return self.symbol


pickups = [Item("carrot"), Item("apple", 20, ""), Item("strawberry", 20, "s"), Item("cherry", 20, "c"), Item("watermelon"), Item("radish"), Item("cucumber"), Item("meatball"), Item("spade", 0, "S"), Item("key", 0, "k"), Item("key", 0, "k"), Item("coffin", 100, "C"), Item("coffin", 100, "C")]


def randomize(grid):
    for item in pickups:
        while True:
            # slumpa en position tills vi hittar en som är ledig
            x = grid.get_random_x()
            y = grid.get_random_y()
            if grid.is_empty(x, y):
                grid.set(x, y, item)
                break  # avbryt while-loopen, fortsätt med nästa varv i for-loopen

def randomize_one_item(grid):
    excluded_items = {"spade", "key", "coffin"} #Skapa en exclude list för att endast få frukt/grönsak
    filtered_items = [item for item in pickups if item.name not in excluded_items]
    # Välj en random item ifrån den filtrerade listan
    random_item = random.choice(filtered_items) if filtered_items else None

    print("Slumpvis vald frukt/grönsak är tillagd:", random_item.name)

    while True:
        # slumpa en position tills vi hittar en som är ledig
        x = grid.get_random_x()
        y = grid.get_random_y()
        if grid.is_empty(x, y):
            grid.set(x, y, random_item)
            break  # avbryt while-loopen, fortsätt med nästa varv i for-loopen