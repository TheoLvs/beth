from chess import piece_name, piece_symbol

from .constants import PIECE_VALUES


def parse_piece(piece):

    if piece is None:
        return {}
    else:
        piece_type = piece.piece_type

        data = {
            "color": "WHITE" if piece.color else "BLACK",
            "type": piece_type,
            "name": piece_name(piece_type),
            "symbol": piece_symbol(piece_type),
            "value": PIECE_VALUES[piece_type],
        }

        return data
