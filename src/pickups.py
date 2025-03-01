import copy
import random

class Item:
    """Representerar saker man kan plocka upp."""
    def __init__(self, name, value=10, symbol="?", source="initial"):
        self.name = name
        self.value = value
        self.symbol = symbol
        self.source = source

    def __str__(self):
        return self.symbol


pickups = [Item("carrot"), Item("apple", 20), Item("strawberry", 20), Item("cherry", 20), Item("watermelon"), Item("radish"), Item("cucumber"), Item("meatball"), Item("spade", 0, "S"), Item("key", 0, "k"), Item("key", 0, "k"), Item("coffin", 100, "C"), Item("coffin", 100, "C")]


def randomize(grid):
    for item in pickups:
        x, y = grid.randomize_empty_position_in_grid()
        grid.set(x, y, item)

def randomize_one_item(grid):
    excluded_items = {"spade", "key", "coffin"} #Skapa en exclude lista för att endast få frukt/grönsak
    filtered_items = [item for item in pickups if item.name not in excluded_items]
    # Välj en random item ifrån den filtrerade listan
    random_item = random.choice(filtered_items) if filtered_items else None
    copy_of_random_item = copy.deepcopy(random_item) #Gör en kopia av original item för att kunna skilja på ursprungliga item och tillagda
    copy_of_random_item.source = "added" #Sätter added tag för att kunna skilja ifrån initial items

    print("Slumpvis vald frukt/grönsak är tillagd:", random_item.name)

    while True:
        # slumpa en position tills vi hittar en som är ledig
        x = grid.get_random_x()
        y = grid.get_random_y()
        if grid.is_empty(x, y):
            grid.set(x, y, copy_of_random_item)
            break  # avbryt while-loopen, fortsätt med nästa varv i for-loopen

def add_the_end(grid):
    ending = Item("ending", 0, "E", "The End")
    while True:
        # slumpa en position tills vi hittar en som är ledig
        x = grid.get_random_x()
        y = grid.get_random_y()
        if grid.is_empty(x, y):
            grid.set(x, y, ending)
            break  # avbryt while-loopen