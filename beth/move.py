from chess import parse_square,square_name
from .piece import parse_piece

class Move: 
    def __init__(self,value:str,board):

        self.move = board.parse_san(value)
        self.move_str = board.san(self.move)
        self.trajectory = (self.move.from_square,self.move.to_square)
        self.is_capture = board.is_capture(self.move)
        self.from_piece = parse_piece(board.piece_at(self.from_square))
        if self.is_capture:
            self.to_piece = parse_piece(board.piece_at(self.to_square))
            self.value = self.to_piece["value"]
        else:
            self.to_piece = {}
            self.value = 0

    def __repr__(self):
        x,y = self.trajectory_str
        color = self.from_piece['color'].upper()
        name = self.from_piece['name'].upper()
        return f"Move(piece={color} {name},from={x},to={y},value={self.value})"

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
        x,y = self.trajectory
        return square_name(x),square_name(y)

