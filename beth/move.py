from chess import parse_square, square_name, Board
from .piece import parse_piece
from .constants import get_unicode_symbol, CHECKMATE_VALUE
from .constants import PIECE_VALUES_BY_NAME,PROMOTED_PIECES


class Move:
    def __init__(self, value: str, board: Board):
        """Helper class to parse moves on a given board status
        The base class from python-chess miss information like piece value, capture and checkmate
        Used across the library to standardize move parsing and evaluation

        Args:
            value (str): The input move as string (SAN, LAN) or chess Move object
            board (Board): The board status at the right moment, moves and notations depend on the context
        """

        # Parse the string input if input value is not already a move object
        if isinstance(value, str):
            self.move = board.parse_san(value)
        else:
            self.move = value

        # Convert to real SAN value to have a uniformed string version
        self.move_str = board.san(self.move)

        # Store board and future board
        self.board_from = board.deepcopy()
        self.board_to = board.deepcopy()
        self.board_to.push_san(self.move_str)

        # Evaluate move characteristics, capture, from and to square
        self.trajectory = (self.move.from_square, self.move.to_square)
        self.is_capture = board.is_capture(self.move)
        self.from_piece = parse_piece(board.piece_at(self.from_square))

        # Prepare features for display and evaluation
        self.color = self.from_piece["color"].upper()
        self.color_factor = 1 if self.color == "WHITE" else -1
        self.name = self.from_piece["name"].upper()

        # Capture rules
        # Parse piece value of the capture
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

        # Use SAN to determine is the move is a checkmate
        # Modify move value if there is a checkmate
        self.checkmate = "#" in self.move_str
        if self.checkmate:
            self.value = CHECKMATE_VALUE

        # Promotion rules
        # Parsing the SAN name to get promotion piece (With a check the san value is appended by +) 
        # Move value increased by the promotion piece minus the pawn value we exchanged
        if "=" in self.move_str:
            self.promoted_piece = PROMOTED_PIECES[self.move_str.split("=")[-1].replace("+","").replace("#","")]
            bonus_promotion = PIECE_VALUES_BY_NAME[self.promoted_piece] - 1
            self.value += bonus_promotion

    def __str__(self):
        return self.move_str


    def __repr__(self):
        """Elegant representation of the move with unicode symbol and move captures

        Returns:
            str: String representation of the move
        """
        x, y = self.trajectory_str
        unicode_symbol = get_unicode_symbol(self.name, self.color)
        value_str = f"(+{self.value})" if self.value > 0 else ""
        return (
            f"{unicode_symbol} {self.color} {self.name} {x} -> {y} {value_str}".strip()
        )

    def evaluate(self,with_heuristics = True,heuristics_matrix=None):
        if self.checkmate:
            return CHECKMATE_VALUE * self.color_factor
        else:
            score_from = self.board_from.evaluate(with_heuristics,heuristics_matrix)
            score_to = self.board_to.evaluate(with_heuristics,heuristics_matrix)
            return score_to[0] - score_from[0]
 
    @property
    def score(self):
        if not hasattr(self,"_score"):
            self._score = self.evaluate()
        return self._score
        # return self.value * self.color_factor
        # return self.evaluate

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
