
import random

from .player import Player



class RandomPlayer(Player):

    def move(self,value):

        self.wait()

        moves = list(self.board.legal_moves)
        selected_move = random.choice(moves)
        self.board.push(selected_move)




