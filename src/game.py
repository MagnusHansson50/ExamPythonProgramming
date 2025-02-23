from .grid import Grid
from .pickups import randomize_one_item
from .player import Player
from . import pickups
from . import traps


player = Player(17, 5) #Positionera spelaren mitt på planen
score = 0
inventory = []
time_for_random_item = 0
all_initial_found = False

g = Grid()
g.set_player(player)
g.make_walls()
g.make_four_inner_walls()
#g.make_random_walls_in_game()
pickups.randomize(g)
pickups.add_the_end(g)
traps.randomize(g)

# TODO: flytta denna till en annan fil
def print_status(game_grid):
    """Visa spelvärlden och antal poäng."""
    print("--------------------------------------")
    print(f"You have {score} points.")
    print(game_grid)

command = "a"
# Loopa tills användaren trycker Q eller X.
while not command.casefold() in ["q", "x"]:
    if time_for_random_item >= 25:
        time_for_random_item = 0
        randomize_one_item(g)
    print_status(g)

    command = input("Use WASD to move, Q/X to quit. ")
    command = command.casefold()[:1]
    can_move = False

    if command == "d":
        can_move = player.move_right(g) # move right
    elif command == "a":
        can_move = player.move_left(g) # move left
    elif command == "w":
        can_move = player.move_up(g) # move up
    elif command == "s":
        can_move = player.move_down(g) # move down
    elif command == "i":
        player.inventory.show_inventory()

    if can_move:
        score -= 1
        time_for_random_item += 1
        maybe_item = g.get(player.pos_x, player.pos_y)

        if isinstance(maybe_item, pickups.Item):
            # we found something
            if maybe_item.name == "ending":
                if all_initial_found:
                    break
                else:
                    continue
            elif maybe_item.name == "coffin":
                if player.inventory.is_in_storage("key"):
                    score += maybe_item.value
                    player.inventory.add_to_inventory(maybe_item.name)
                    all_initial_found = player.inventory.remove_from_items_to_pickup_before_end_if_initial(maybe_item)
                    print(f"You found a {maybe_item.name}, +{maybe_item.value} points.")
                    g.clear(player.pos_x, player.pos_y)
                    player.inventory.remove_from_inventory("key", 1)
            else:
                score += maybe_item.value
                player.inventory.add_to_inventory(maybe_item.name)
                all_initial_found = player.inventory.remove_from_items_to_pickup_before_end_if_initial(maybe_item)
                print(f"You found a {maybe_item.name}, +{maybe_item.value} points. {maybe_item.source}")
                #g.set(player.pos_x, player.pos_y, g.empty)
                g.clear(player.pos_x, player.pos_y)

        if isinstance(maybe_item, traps.Traps):
            # we found something
            score -= maybe_item.value
            print(f"You found a {maybe_item.name}, -{maybe_item.value} points.")


# Hit kommer vi när while-loopen slutar
print("Thank you for playing!")
