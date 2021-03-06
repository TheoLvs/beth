COLORS = ["WHITE","BLACK"]
PIECES = ["PAWN", "KNIGHT", "BISHOP", "ROOK", "QUEEN", "KING"]


PIECE_VALUES = {
    1: 1,  # Pawns
    2: 3,  # Knights
    3: 3,  # Bishops
    4: 5,  # Rook
    5: 9,  # Queen
    6: 200,  # King
}

CHECKMATE_VALUE = 200

PROMOTED_PIECES = {
    "Q":"QUEEN",
    "R":"ROOK",
    "N":"KNIGHT",
    "B":"BISHOP",
}


PIECE_VALUES_BY_NAME = {
    "PAWN": 1,  # Pawns
    "KNIGHT": 3,  # Knights
    "BISHOP": 3,  # Bishops
    "ROOK": 5,  # Rook
    "QUEEN": 9,  # Queen
    "KING": 200,  # King
}

PIECE_VALUES_LIST = [1,3,3,5,9,0]


UNICODE_PIECE_SYMBOLS = {
    "WHITE": {
        "PAWN": "♙",
        "KNIGHT": "♘",
        "BISHOP": "♗",
        "ROOK": "♖",
        "QUEEN": "♕",
        "KING": "♔",
    },
    "BLACK": {
        "PAWN": "♟",
        "KNIGHT": "♞",
        "BISHOP": "♝",
        "ROOK": "♜",
        "QUEEN": "♛",
        "KING": "♚",
    },
}


def get_unicode_symbol(piece_type, color):
    return UNICODE_PIECE_SYMBOLS[color][piece_type]
