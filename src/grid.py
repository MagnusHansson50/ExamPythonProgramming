import random

class Grid:
    """Representerar spelplanen. Du kan ändra standardstorleken och tecknen för olika rutor. """
    width = 36
    height = 12
    empty = "."  # Tecken för en tom ruta
    wall = "■"   # Tecken för en ogenomtränglig vägg

    def __init__(self):
        """Skapa ett objekt av klassen Grid"""
        # Spelplanen lagras i en lista av listor. Vi använder "list comprehension" för att sätta tecknet för "empty" på varje plats på spelplanen.
        self.data = [[self.empty for y in range(self.width)] for z in range(
            self.height)]


    def get(self, x, y):
        """Hämta det som finns på en viss position"""
        return self.data[y][x]

    def set(self, x, y, value):
        """Ändra vad som finns på en viss position"""
        self.data[y][x] = value

    def set_player(self, player):
        self.player = player

    def clear(self, x, y):
        """Ta bort item från position"""
        self.set(x, y, self.empty)

    def __str__(self):
        """Gör så att vi kan skriva ut spelplanen med print(grid)"""
        xs = ""
        for y in range(len(self.data)):
            row = self.data[y]
            for x in range(len(row)):
                if x == self.player.pos_x and y == self.player.pos_y:
                    xs += "@"
                else:
                    xs += str(row[x])
            xs += "\n"
        return xs


    def make_walls(self):
        """Skapa väggar runt hela spelplanen"""
        for i in range(self.height):
            self.set(0, i, self.wall)
            self.set(self.width - 1, i, self.wall)

        for j in range(1, self.width - 1):
            self.set(j, 0, self.wall)
            self.set(j, self.height - 1, self.wall)

    def make_four_inner_walls(self):
        # Definiera fyra väggar
        walls = [
            (5, 3, 6, True),  # Vertikal vägg (x=5, from y=3 to y=10)
            (15, 2, 6, True),  # Vertikal vägg (x=15, from y=2 to y=8)
            (20, 6, 12, False),  # Horisontell vägg (y=6, from x=20 to x=32)
            (8, 9, 20, False)  # Horisontell vägg (y=9, from x=8 to x=28)
        ]
        # sätt vägg blocken
        for x, y, length, vertical in walls:
            for i in range(length):
                if vertical and (y+i) < self.height: # Kolla att vi är inom ramen
                    self.set(x, (y+i), self.wall)
                elif not vertical and (x+i) < self.width: # Kolla att vi är inom ramen
                    self.set((x+i), y, self.wall)

    def make_random_walls_in_game(self, wall_chance=0.2):
        """Skapa slumpade väggblock i spelplanen, används inte för tillfället"""
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                if random.random() < wall_chance:
                    self.set(x, y, self.wall)

    # Används i filen pickups.py
    def get_random_x(self):
        """Slumpa en x-position på spelplanen"""
        return random.randint(0, self.width-1)

    def get_random_y(self):
        """Slumpa en y-position på spelplanen"""
        return random.randint(0, self.height-1)


    def is_empty(self, x, y):
        """Returnerar True om det inte finns något på aktuell ruta"""
        return self.get(x, y) == self.empty
