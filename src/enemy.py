import random

from src.player import Player


class Enemy(Player):
    def __init__(self, x, y):
        super().__init__(x, y) #Anropar Players konstruktor
        self.marker = "^"
        self.previous_moves = [(0 ,0), (0, 0)]

    def move_toward_player(self, player, grid):
        """Flytta fienden mot spelaren. Inte helt nöjd med algoritmen än"""
        # Möjliga drag: (x, y)
        moves = [
            (1, 0),  # Right
            (-1, 0),  # Left
            (0, 1),  # Down
            (0, -1)  # Up
        ]

        # Sortera så vi får bästa draget först, eller rättare sagt dragen med kortast väg
        moves.sort(key=lambda move: abs((self.pos_x + move[0]) - player.pos_x) + abs((self.pos_y + move[1]) - player.pos_y))
        #Prova bästa dragen och ta bort det om det inte fungerar
        best_moves = [moves.pop(0), moves.pop(0)]
        second_last_move = self.previous_moves.pop(0)
        #random.shuffle(best_moves)
        for dx, dy in best_moves:
            if self.can_move(dx, dy, grid):
                #and (((self.pos_x + dx), (self.pos_y + dy)) != (second_last_move[0], second_last_move[1]))):
                last_move = ((self.pos_x + dx), (self.pos_y + dy))
                self.previous_moves.append(last_move)
                self.move(dx, dy)
                return

        # Slumpa resterande för att prova att undvika att vi hoppar fram och tillbaka bakom en vägg
        # Inte helt nöjd med denna än
        random.shuffle(moves)
        for dx, dy in moves:
            if self.can_move(dx, dy, grid) and (((self.pos_x + dx), (self.pos_y + dy)) != (second_last_move[0], second_last_move[1])):
                last_move = ((self.pos_x + dx), (self.pos_y + dy))
                self.previous_moves.append(last_move)
                self.move(dx, dy)
                return

    def enemy_caught_player(self, player):
        return (self.pos_x, self.pos_y) == (player.pos_x, player.pos_y)

