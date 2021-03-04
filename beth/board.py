import numpy as np
import chess
from chess import scan_forward,pgn
from copy import deepcopy

from .constants import PIECES,COLORS,PIECE_VALUES_BY_NAME,PIECE_VALUES_LIST
from .heuristics import HEURISTICS_MATRIX



class Board(chess.Board):

    def deepcopy(self):
        return deepcopy(self)

    def get_pieces_positions_by_type(self, piece_type: str, color: str = None):

        # Prepare binary representation of pieces
        piece_type = piece_type.upper()
        if piece_type == "BISHOP":
            pieces = self.bishops
        elif piece_type == "PAWN":
            pieces = self.pawns
        elif piece_type == "ROOK":
            pieces = self.rooks
        elif piece_type == "KNIGHT":
            pieces = self.knights
        elif piece_type == "QUEEN":
            pieces = self.queens
        elif piece_type == "KING":
            pieces = self.kings
        else:
            raise Exception(f"Piece type {piece_type} is not among {PIECES}")

        # Prepare binary color mask
        if color is None:
            mask = self.occupied
        else:
            if isinstance(color, str):
                color = 0 if color.upper() == "WHITE" else 1
            mask = self.occupied_co[1-color]

        return list(scan_forward(pieces & mask))

    def get_pieces_positions(self):

        pieces = {}

        for i, color in enumerate(COLORS):
            pieces[color] = {}
            for piece_type in PIECES:
                pieces[color][piece_type] = self.get_pieces_positions_by_type(
                    piece_type, i
                )

        return pieces




    def get_scores(self):
        raise DeprecationWarning()
        pos = self.get_pieces_positions()
        scores = {}

        for i, color in enumerate(COLORS):
            score = 0
            for piece_type in PIECES:
                if piece_type != "KING":
                    n_pieces = len(pos[color][piece_type])
                    score += n_pieces * PIECE_VALUES_BY_NAME[piece_type]
            scores[color] = score

        scores["DIFF"] = scores["WHITE"] - scores["BLACK"]
        return scores



    def evaluate(self,with_heuristics = True,heuristics_matrix = None):

        # Transform board to numpy 4D tensor
        board_array = self.to_array()

        # Retrive piece values
        piece_values = np.array(PIECE_VALUES_LIST)
        # values = np.stack([values,values]) * np.array([[1],[-1]]) (if broadcasting directly the minus sign)

        # Prepare white and black board tensors
        white_board = board_array[:,:,0,:]
        black_board = board_array[:,:,1,:]

        # Compute board scores
        white_score = (white_board * piece_values).sum()
        black_score = (black_board * piece_values).sum()

        # Compute board heuristics
        if with_heuristics:
            if heuristics_matrix is None:
                heuristics_matrix = HEURISTICS_MATRIX

            white_heuristics = (white_board * heuristics_matrix[:,:,0,:]).sum()
            black_heuristics = (black_board * heuristics_matrix[:,:,1,:]).sum()

            white_score += white_heuristics
            black_score += black_heuristics

        return (white_score - black_score,white_score,black_score)


    def to_array(self):
        # Get pieces positions as dictionary
        pos = self.get_pieces_positions()

        # Convert to numpy array
        arrays = []
        for piece in PIECES:
            arr = np.zeros((64,2))
            for i,color in enumerate(COLORS):
                arr[pos[color][piece],i] = 1
            arrays.append(arr.reshape(8,8,2))

        array = np.flipud(np.stack(arrays,axis = 3))
        return array

