from .player import Player


class HumanPlayer(Player):
    def move(self, value=None):
        if value is None:
            value = input(f"{self.color} move: ")
        self.board.push_san(value)
