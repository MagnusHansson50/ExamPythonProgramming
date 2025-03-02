import copy
import random
import sys


class Item:
    """Representerar saker man kan plocka upp."""
    def __init__(self, name, value=10, symbol="?", source="initial"):
        self.name = name
        self.value = value
        self.symbol = symbol
        self.source = source

    def __str__(self):
        return self.symbol


pickups = [Item("carrot"), Item("apple", 20), Item("strawberry", 20), Item("cherry", 20), Item("watermelon"), Item("radish"), Item("cucumber"), Item("meatball"), Item("shovel", 0, "S"), Item("key", 0, "k"), Item("key", 0, "k"), Item("coffin", 100, "C"), Item("coffin", 100, "C")]


def randomize(grid):
    """Placerar ut alla Items i pickups på random position"""
    for item in pickups:
        try:
            x, y = grid.randomize_empty_position_in_grid()
        except RuntimeError as e:
            print(f"Critical error: {e}")
            sys.exit(1)  # Lämnar programmet med en felkod
        else:
            grid.set(x, y, item)

def randomize_one_item(grid):
    """Slumpar ut en item på spelplanen"""
    excluded_items = {"spade", "coffin"} #Skapa en exclude lista för att endast få frukt/grönsak eller nyckel eftersom vi kan spränga bort nyckel. Och vi behöver en för att öppna kista
    filtered_items = [item for item in pickups if item.name not in excluded_items]
    # Välj en random item ifrån den filtrerade listan
    random_item = random.choice(filtered_items) if filtered_items else None
    copy_of_random_item = copy.deepcopy(random_item) #Gör en kopia av original item för att kunna skilja på ursprungliga item och tillagda
    copy_of_random_item.source = "added" #Sätter added tag för att kunna skilja ifrån initial items

    print("Added a random chosen item, the following is added:", random_item.name)
    # Slumpar en position tills vi hittar en som är ledig
    try:
        x, y = grid.randomize_empty_position_in_grid()
    except RuntimeError as e:
        print(f"Critical error: {e}")
        sys.exit(1)  # Lämnar programmet med en felkod
    else:
        grid.set(x, y, copy_of_random_item)

def add_the_end(grid):
    """Slumpar ut en Exit på spelplanen"""
    ending = Item("ending", 0, "E", "The End")
    # slumpa en position tills vi hittar en som är ledig
    try:
        x, y = grid.randomize_empty_position_in_grid()
    except RuntimeError as e:
        print(f"Critical error: {e}")
        sys.exit(1)  # Lämnar programmet med en felkod
    else:
        grid.set(x, y, ending)