import random

from .player import Player


class RandomPlayer(Player):
    def move(self, value):

        self.wait()

        moves = list(self.game.board.legal_moves)
        selected_move = str(random.choice(moves))
        return selected_move
