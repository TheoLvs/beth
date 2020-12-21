from .player import Player


class SequenceGame:
    def __init__(self, sequence, wait, victory_status=None, winner=None):

        self.victory_status = victory_status
        self.winner = winner

        if isinstance(sequence, str):
            sequence = sequence.split(" ")
        self.sequence = sequence
        seq_white = sequence[::2]
        seq_black = sequence[1::2]

        # Init two players
        self.white = SequencePlayer(seq_white, wait=wait)
        self.black = SequencePlayer(seq_black, wait=wait)


class SequencePlayer(Player):
    def __init__(self, sequence, **kwargs):

        super().__init__(**kwargs)
        self.sequence = sequence
        self.turn_number = 0

    def move(self, value):

        self.wait()

        move = self.sequence[self.turn_number]
        self.turn_number += 1
        self.game.board.push_san(move)
