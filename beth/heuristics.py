# https://www.chessprogramming.org/Simplified_Evaluation_Function
# https://www.freecodecamp.org/news/simple-chess-ai-step-by-step-1d55a9266977/

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from .constants import PIECES, COLORS

PAWN = np.array(
    [
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0],
        [1.0, 1.0, 2.0, 3.0, 3.0, 2.0, 1.0, 1.0],
        [0.5, 0.5, 1.0, 2.5, 2.5, 1.0, 0.5, 0.5],
        [0.0, 0.0, 0.0, 2.0, 2.0, 0.0, 0.0, 0.0],
        [0.5, -0.5, -1.0, 0.0, 0.0, -1.0, -0.5, 0.5],
        [0.5, 1.0, 1.0, -2.0, -2.0, 1.0, 1.0, 0.5],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    ]
)

ROOK = np.array(
    [
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5],
        [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
        [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
        [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
        [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
        [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
        [0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.0],
    ]
)


BISHOP = np.array(
    [
        [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
        [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
        [-1.0, 0.0, 0.5, 1.0, 1.0, 0.5, 0.0, -1.0],
        [-1.0, 0.5, 0.5, 1.0, 1.0, 0.5, 0.5, -1.0],
        [-1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, -1.0],
        [-1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0],
        [-1.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.5, -1.0],
        [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
    ]
)

KNIGHT = np.array(
    [
        [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
        [-4.0, -2.0, 0.0, 0.0, 0.0, 0.0, -2.0, -4.0],
        [-3.0, 0.0, 1.0, 1.5, 1.5, 1.0, 0.0, -3.0],
        [-3.0, 0.5, 1.5, 2.0, 2.0, 1.5, 0.5, -3.0],
        [-3.0, 0.0, 1.5, 2.0, 2.0, 1.5, 0.0, -3.0],
        [-3.0, 0.5, 1.0, 1.5, 1.5, 1.0, 0.5, -3.0],
        [-4.0, -2.0, 0.0, 0.0, 0.0, 0.0, -2.0, -4.0],
        [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
    ]
)

QUEEN = np.array(
    [
        [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
        [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
        [-1.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
        [-0.5, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
        [0.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, 0.0],
        [-1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, -1.0],
        [-1.0, 0.0, 0.5, 0.0, 0.0, 0.5, 0.0, -1.0],
        [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
    ]
)

KING = np.array(
    [
        [-3, -4, -4, -5, -5, -4, -4, -3],
        [-3, -4, -4, -5, -5, -4, -4, -3],
        [-3, -4, -4, -5, -5, -4, -4, -3],
        [-3, -4, -4, -5, -5, -4, -4, -3],
        [-2, -3, -3, -4, -4, -3, -3, -2],
        [1, -2, -2, -2, -2, -2, -2, -1],
        [2, 2, 0, 0, 0, 0, 2, 2],
        [2, 3, 1, 0, 0, 1, 3, 2],
    ]
)


HEURISTICS = {
    "PAWN": PAWN,
    "ROOK": ROOK,
    "KNIGHT": KNIGHT,
    "BISHOP": BISHOP,
    "QUEEN": QUEEN,
    "KING": KING,
}


def make_heuristics_matrix():
    """Returns heuristics as numpy 4D tensor
    Of shape (8,8,2,6) = (width,height,colors,pieces)
    Will be used to easily match with 4D representation of a given board
    Hence to calculate board evaluation heuristics with tensor multiplications
    """

    # Prepare data placeholder
    data = []

    # Iterate for WHITE and BLACK
    for color in COLORS:

        # Prepare heuristics to be stacked for one color
        heur_color = []

        # Iterate for each piece
        for piece in PIECES:

            # Get the heuristics for a given piece
            # Flip it for black pieces
            heur_piece = HEURISTICS[piece]
            if color == "BLACK":
                heur_piece = np.flipud(heur_piece)
            heur_color.append(heur_piece)

        # Stack everything as a numpy array (shape=(6,8,8))
        heur_color = np.stack(heur_color)
        data.append(heur_color)

    # Stack for each color (shape=(2,6,8,8))
    data = np.stack(data, axis=0)

    # Swap axes to be in the same representation (shape=(8,8,2,6))
    data = data.swapaxes(0, 2).swapaxes(1, 3)
    return data


HEURISTICS_MATRIX = make_heuristics_matrix()


def show_heuristics_matrix(x, title="Heuristics", ax=None):

    sns.heatmap(
        x,
        annot=True,
        cmap="RdYlGn",
        square=True,
        ax=ax,
        xticklabels=["a", "b", "c", "d", "e", "f", "g", "h"],
        yticklabels=list(reversed(list(range(1, 9)))),
    )

    if ax is None:
        plt.title(title)
        plt.show()
    else:
        ax.set_title(title)
        return ax


def show_all_heuristics_matrix(matrix):
    fig, axes = plt.subplots(nrows=4, ncols=3, figsize=(15, 15))

    for i, color in enumerate(COLORS):
        for j, piece in enumerate(PIECES):
            x = i * 2 + j // 3
            y = j % 3
            show_heuristics_matrix(matrix, f"{color.title()} {piece.title()}", ax=axes[x, y])

    plt.show()
