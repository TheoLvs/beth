from chess import parse_square, square_name
from .piece import parse_piece
from .constants import get_unicode_symbol


class Move:
    def __init__(self, value: str, board):

        if isinstance(value,str):
            self.move = board.parse_san(value)
        else:
            self.move = value

        self.move_str = board.san(self.move)
        self.trajectory = (self.move.from_square, self.move.to_square)
        self.is_capture = board.is_capture(self.move)
        self.from_piece = parse_piece(board.piece_at(self.from_square))
        self.color = self.from_piece["color"].upper()
        self.name = self.from_piece["name"].upper()

        if self.is_capture:
            try:
                self.to_piece = parse_piece(board.piece_at(self.to_square))
                self.value = self.to_piece["value"]
            except:
                self.to_piece = {}
                self.value = 0
        else:
            self.to_piece = {}
            self.value = 0

    def __repr__(self):
        x, y = self.trajectory_str
        unicode_symbol = get_unicode_symbol(self.name, self.color)
        value_str = f"(+{self.value})" if self.value > 0 else ""
        return (
            f"{unicode_symbol} {self.color} {self.name} {x} -> {y} {value_str}".strip()
        )

    @property
    def score(self):
        return self.value * (1 if self.color == "WHITE" else -1)

    @property
    def from_square(self):
        return self.trajectory[0]

    @property
    def to_square(self):
        return self.trajectory[1]

    @property
    def trajectory_str(self):
        x, y = self.trajectory
        return square_name(x), square_name(y)
