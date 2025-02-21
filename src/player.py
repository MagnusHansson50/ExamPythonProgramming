class Player:
    marker = "@"

    def __init__(self, x, y):
        self.pos_x = x
        self.pos_y = y

    # Flyttar spelaren. "dx" och "dy" är skillnaden
    def move(self, dx, dy):
        """Flyttar spelaren.\n
        dx = horisontell förflyttning, från vänster till höger\n
        dy = vertikal förflyttning, uppifrån och ned"""
        self.pos_x += dx
        self.pos_y += dy

    def can_move(self, x, y, grid):
        maybe_wall = grid.get(self.pos_x + x, self.pos_y + y)
        if maybe_wall == "■": #Returnerar att det inte går att flytta om det är ett väggtecken i vägen
            return False
        return True

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