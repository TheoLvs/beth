from .player import Player


class HumanPlayer(Player):

    def __str__(self):
        return "HumanPlayer"

    def move(self, value=None):
        if value is None:
            value = input(f"{self.color} move: ")
        return value
