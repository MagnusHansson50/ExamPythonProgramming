from .grid import Grid
from .player import Player
from . import pickups



player = Player(17, 5) #Positionera spelaren mitt på planen
score = 0
inventory = []

g = Grid()
g.set_player(player)
g.make_walls()
pickups.randomize(g)

# TODO: flytta denna till en annan fil
def print_status(game_grid):
    """Visa spelvärlden och antal poäng."""
    print("--------------------------------------")
    print(f"You have {score} points.")
    print(game_grid)

command = "a"
# Loopa tills användaren trycker Q eller X.
while not command.casefold() in ["q", "x"]:
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
        maybe_item = g.get(player.pos_x, player.pos_y)

        if isinstance(maybe_item, pickups.Item):
            # we found something
            score += maybe_item.value
            player.inventory.add_to_inventory(maybe_item.name)
            print(f"You found a {maybe_item.name}, +{maybe_item.value} points.")
            #g.set(player.pos_x, player.pos_y, g.empty)
            g.clear(player.pos_x, player.pos_y)


# Hit kommer vi när while-loopen slutar
print("Thank you for playing!")
