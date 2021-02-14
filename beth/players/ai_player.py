import random

from .player import Player


class AIBrain:
    def __init__(self):
        pass

    def predict_next(self, game):
        pass


class AIPlayer(Player):
    def __init__(self, brain, wait=None):
        super().__init__(wait=wait)
        self.brain = brain

    def move(self, value=None):

        # Overriding default behavior by calling the moves
        if value is not None:
            return value

        # Default behavior where the brain object predicts the next move
        else:
            self.wait()
            selected_move = self.brain.predict_next(self.game)
            return selected_move
