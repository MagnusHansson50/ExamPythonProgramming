import random

from .bomb import Bomb, update_bombs
from .enemy import Enemy
from .functions import print_status, print_help, print_story
from .grid import Grid
from .pickups import randomize_one_item
from .player import Player
from . import pickups
from . import traps

player = Player(17, 5) #Positionera spelaren mitt på planen
time_for_random_item = 0
jump_two_steps = False
grace_period = 6
enemy_can_go = 0
bombs = []
enemies = []

g = Grid()
g.set_player(player)
g.make_walls()
g.make_four_inner_walls()
#g.make_random_walls_in_game()
pickups.randomize(g)
pickups.add_the_end(g)
traps.randomize(g)

number_of_enemies = random.randint(1, 3)
for i in range(number_of_enemies):
    x, y = g.randomize_empty_position_in_grid()
    enemies.append(Enemy(x, y))
    g.set_enemies(enemies)

command = "a"
# Loopa tills användaren trycker Q eller X.
while not command.casefold() in ["q", "x"]:
    if time_for_random_item >= 25:
        time_for_random_item = 0
        randomize_one_item(g)
    print_status(g, player.score)

    command = input("Use WASD to move, Q/X to quit. H for help.")
    command = command.casefold()[:1]
    can_move = False

    if command == "d":
        can_move = player.move_right(g) # move right
        if jump_two_steps and can_move:
            player.move_right(g)  # move right
            jump_two_steps = False
    elif command == "a":
        can_move = player.move_left(g) # move left
        if jump_two_steps and can_move:
            player.move_left(g)  # move left
            jump_two_steps = False
    elif command == "w":
        can_move = player.move_up(g) # move up
        if jump_two_steps and can_move:
            player.move_up(g)  # move up
            jump_two_steps = False
    elif command == "s":
        can_move = player.move_down(g) # move down
        if jump_two_steps and can_move:
            player.move_down(g)  # move down
            jump_two_steps = False
    elif command == "i":
        player.inventory.show_inventory()
    elif command == "j":
        jump_two_steps = True
    elif command == "b":
        bomb = Bomb(player.pos_x, player.pos_y, g)
        bombs.append(bomb)
    elif command == "t":
        maybe_trap = g.get(player.pos_x, player.pos_y)
        if isinstance(maybe_trap, traps.Traps):
            g.clear(player.pos_x, player.pos_y)
            print("You disarmed a trap!!!")
    elif command == "h":
        print_help()
    elif command == "p":
        print_story()

    if can_move:
        if grace_period >= 5:
            player.score -= 1
        grace_period += 1
        enemy_can_go += 1
        time_for_random_item += 1
        update_bombs(player, g, bombs, enemies)
        maybe_item = g.get(player.pos_x, player.pos_y)

        if isinstance(maybe_item, pickups.Item):
            # we found something
            if maybe_item.name == "ending":
                if player.all_initial_found:
                    break
                #else:
                #   continue
            elif maybe_item.name == "coffin":
                if player.inventory.is_in_storage("key"):
                    player.score += maybe_item.value
                    grace_period = 0
                    player.inventory.add_to_inventory(maybe_item.name)
                    player.all_initial_found = player.inventory.remove_from_items_to_pickup_before_end_if_initial(maybe_item)
                    print(f"You found a {maybe_item.name}, +{maybe_item.value} points.")
                    g.clear(player.pos_x, player.pos_y)
                    player.inventory.remove_from_inventory("key", 1)
            else:
                player.score += maybe_item.value
                grace_period = 0
                player.inventory.add_to_inventory(maybe_item.name)
                player.all_initial_found = player.inventory.remove_from_items_to_pickup_before_end_if_initial(maybe_item)
                print(f"You found a {maybe_item.name}, +{maybe_item.value} points. {maybe_item.source}")
                #g.set(player.pos_x, player.pos_y, g.empty)
                g.clear(player.pos_x, player.pos_y)
        if enemy_can_go > 1:
            enemy_can_go = 0
            for i in range(len(enemies)):
                if enemies[i].enemy_caught_player(player):
                    player.score -= 20
                enemies[i].move_toward_player(player, g)
                if enemies[i].enemy_caught_player(player):
                    player.score -= 20


        if isinstance(maybe_item, traps.Traps):
            # we found something
            player.score -= maybe_item.value
            print(f"⚠️ You entered a {maybe_item.name}, -{maybe_item.value} points. ⚠️")


# Hit kommer vi när while-loopen slutar
print(f"Thank you for playing! Your score is: {player.score}")
