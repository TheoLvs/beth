import random

from .player import Player


class AIPlayer(Player):

    def __init__(self,brain,wait = None):
        super().__init__(wait = wait)
        self.brain = brain

    def move(self, value):
        self.wait()
        selected_move = self.brain.predict_next(self.game)
        return selected_move
