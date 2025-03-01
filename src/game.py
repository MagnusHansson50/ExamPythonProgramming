import random

from .bomb import Bomb
from .enemy import Enemy
from .functions import print_status, print_help, print_story
from .grid import Grid
from .pickups import randomize_one_item
from .player import Player
from . import pickups
from . import traps

player = Player(17, 5) #Positionera spelaren mitt på planen
score = 0
time_for_random_item = 0
all_initial_found = False
jump_two_steps = False
grace_period = 6
enemy_can_go = 0
bombs = []

g = Grid()
g.set_player(player)
g.make_walls()
g.make_four_inner_walls()
#g.make_random_walls_in_game()
pickups.randomize(g)
pickups.add_the_end(g)
traps.randomize(g)

enemy_one = None
enemy_two = None
enemy_three = None
g.set_enemy_one(enemy_one)
g.set_enemy_two(enemy_two)
g.set_enemy_three(enemy_three)

number_of_enemies = random.randint(1, 3)
if number_of_enemies >= 1:
    x, y = g.randomize_empty_position_in_grid()
    enemy_one = Enemy(x, y)
    g.set_enemy_one(enemy_one)
if number_of_enemies >= 2:
    x, y = g.randomize_empty_position_in_grid()
    enemy_two = Enemy(x, y)
    g.set_enemy_two(enemy_two)
if number_of_enemies == 3:
    x, y = g.randomize_empty_position_in_grid()
    enemy_three = Enemy(x, y)
    g.set_enemy_three(enemy_three)


def update_bombs(p, grid):
    """Uppdaterar alla bomber och spränger när countdown är 0."""
    for boom in bombs[:]:  # Kopiera listan för att undvika att den ändras under loopen
        if boom.tick():
            explode_bomb(boom, p, grid)
            bombs.remove(boom)  # Ta bort bomben från listan.

def explode_bomb(boom, p, grid):
    global score # Inte helt bra med global kanske, men enklaste vägen ut för tillfället.
    global all_initial_found # Inte helt bra med global kanske, men enklaste vägen ut för tillfället.
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
                all_initial_found = p.inventory.remove_from_items_to_pickup_before_end_if_initial(item_at_position)
            if item_at_position == "B" and not ((blow_pos_x, blow_pos_y) == (boom.pos_x, boom.pos_y)):
                item_is_bomb = True
            if x_ok and y_ok and ending_not_at_position and not item_is_bomb: #Ta inte bort om det är ett ram vägg element, exit eller en annan bomb.
                grid.clear(blow_pos_x, blow_pos_y)
            if (p.pos_x, p.pos_y) ==  (boom.pos_x + dx, boom.pos_y + dy):
                print("Räkna ner")
                score -= 50
    print(f"💥 Bomb exploded 💥 ({boom.pos_x}, {boom.pos_y})!")

command = "a"
# Loopa tills användaren trycker Q eller X.
while not command.casefold() in ["q", "x"]:
    if time_for_random_item >= 25:
        time_for_random_item = 0
        randomize_one_item(g)
    print_status(g, score)

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
            score -= 1
        grace_period += 1
        enemy_can_go += 1
        time_for_random_item += 1
        update_bombs(player, g)
        maybe_item = g.get(player.pos_x, player.pos_y)

        if isinstance(maybe_item, pickups.Item):
            # we found something
            if maybe_item.name == "ending":
                if all_initial_found:
                    break
                #else:
                #   continue
            elif maybe_item.name == "coffin":
                if player.inventory.is_in_storage("key"):
                    score += maybe_item.value
                    grace_period = 0
                    player.inventory.add_to_inventory(maybe_item.name)
                    all_initial_found = player.inventory.remove_from_items_to_pickup_before_end_if_initial(maybe_item)
                    print(f"You found a {maybe_item.name}, +{maybe_item.value} points.")
                    g.clear(player.pos_x, player.pos_y)
                    player.inventory.remove_from_inventory("key", 1)
            else:
                score += maybe_item.value
                grace_period = 0
                player.inventory.add_to_inventory(maybe_item.name)
                all_initial_found = player.inventory.remove_from_items_to_pickup_before_end_if_initial(maybe_item)
                print(f"You found a {maybe_item.name}, +{maybe_item.value} points. {maybe_item.source}")
                #g.set(player.pos_x, player.pos_y, g.empty)
                g.clear(player.pos_x, player.pos_y)
        if enemy_can_go > 1:
            enemy_can_go = 0
            if number_of_enemies >= 1:
                if enemy_one.enemy_caught_player(player):
                    score -= 20
                enemy_one.move_toward_player(player, g)
                if enemy_one.enemy_caught_player(player):
                    score -= 20
            if number_of_enemies >= 2:
                if enemy_one.enemy_caught_player(player):
                    score -= 20
                enemy_two.move_toward_player(player, g)
                if enemy_two.enemy_caught_player(player):
                    score -= 20
            if number_of_enemies == 3:
                if enemy_one.enemy_caught_player(player):
                    score -= 20
                enemy_three.move_toward_player(player, g)
                if enemy_three.enemy_caught_player(player):
                    score -= 20

        if isinstance(maybe_item, traps.Traps):
            # we found something
            score -= maybe_item.value
            print(f"⚠️ You entered a {maybe_item.name}, -{maybe_item.value} points. ⚠️")


# Hit kommer vi när while-loopen slutar
print(f"Thank you for playing! Your score is: {score}")
