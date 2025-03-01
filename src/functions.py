def print_status(game_grid, score):
    """Visa spelvärlden och antal poäng."""
    print("--------------------------------------")
    print(f"You have {score} points.")
    print(game_grid)

def print_help():
    print("d moves right")
    print("a moves left")
    print("w moves up")
    print("s moves down")
    print("i prints inventory")
    print("j before a move makes it jump two steps")
    print("b places a bomb, will explode after 3 moves")
    print("t disarms a trap, in case you are on a trap")
    print("h for help")
    print("p for print story")

def print_story():
    print("The player can move one step at the time, unless j is entered before than the player jumps two steps. It is not possible to walk through walls\n"
          "You are getting points by collecting items. To be able to collect a coffin(C), you need to collect a key(k) first.\n"
          "You can get an inventory list by entering i. Your score is deducted by one for every move you make, unless you have collected an item.\n"
          "Than there is a grace period of five moves. There are hidden traps, standing on a trap will deduct 10 from the score.\n"
          "It is possible to disarm traps when standing on them by entering t. You can go through walls if you have collected a shovel.\n"
          "Once it used it is remove from inventory. Every 25th move a random item is added to the grid.\n"
          "When all initial items are collected you can exit by moving to the E. You can place a bomb by entering a b.\n"
          "The bomb explodes after 3 moves, and removes everything in the surrounding 8 tiles.\n"
          "If you are on any of these tiles 50 will be deducted from score. If caught by enemy(^) or running into enemy will deduct 20 from score.\n")