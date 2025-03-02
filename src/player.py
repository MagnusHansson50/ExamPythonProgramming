from src.inventory import Inventory


class Player:
    marker = "@"

    def __init__(self, x, y):
        self.pos_x = x
        self.pos_y = y
        self.score = 0
        self.all_initial_found = False # Variabel för att hålla koll på om vi samlat alla initiala element
        self.inventory = Inventory()

    # Flyttar spelaren. "dx" och "dy" är skillnaden
    def move(self, dx, dy):
        """Flyttar spelaren.\n
        dx = horisontell förflyttning, från vänster till höger\n
        dy = vertikal förflyttning, uppifrån och ned"""
        self.pos_x += dx
        self.pos_y += dy

    def can_move(self, x, y, grid):
        """Kolla om det finns möjlighet att flytta sig. Returnerar True eller False"""
        new_x = self.pos_x + x
        new_y = self.pos_y + y
        maybe_wall = grid.get(new_x, new_y)
        if new_x == 0 or new_y == 0 or new_x == (grid.width - 1) or new_y == (grid.height - 1):
            return False #Returnera False om spelaren provar att gå utanför spelplanen. Förhindrar också att vi kan använda spaden på ytterväggarna.
        else:
            if maybe_wall == "■": #Kollar om det finns ett väggtecken i vägen.
                if self.inventory.is_in_storage("shovel"):
                    self.inventory.remove_from_inventory("shovel", 1) #Ta bort en spade ur inventory eftersom vi kommer använda den på nästa rad.
                    grid.clear(new_x, new_y) #Ta bort väggelement.
                    return True #Returnera True eftersom vi har kunnat ta bort väggelementet med spaden.
                else:
                    return False #Ingen spade returnera False, väggelement i vägen.
            return True #Returnera True, inget väggelement i vägen.

    def move_right(self, g):
        if self.can_move(1, 0, g):
            self.move(1, 0)
            return True
        return False

    def move_left(self, g):
        if self.can_move(-1, 0, g):
            self.move(-1, 0)
            return True
        return False

    def move_up(self, g):
        if self.can_move(0, -1, g):
            self.move(0, -1)
            return True
        return False

    def move_down(self, g):
        if self.can_move(0, 1, g):
            self.move(0, 1)
            return True
        return False