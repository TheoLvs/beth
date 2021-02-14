import numpy as np
import pandas as pd
from copy import deepcopy

from ..move import Move


class RandomTreeSearch:
    def __init__(self, board, move=None, stack=None):

        self.board = deepcopy(board)
        self.move = move
        if move is not None:
            self.board.push(move.move)

        if stack is None:
            self.stack = []
        else:
            self.stack = stack

        self.moves = list(self.board.legal_moves)
        self.children = []

    def search_depth(self, breadth=10, depth=5, gamma=1):
        # print(f"Searching for {depth} moves ahead with {breadth} choices - {breadth**depth} possibilities")
        stack = self.explore(breadth, depth, gamma)
        stack = pd.DataFrame(stack)

        # If player is black
        if self.board.turn == 0:
            stack["total"] *= -1

        stack["next_move"] = stack["names"].map(lambda x : x[0])
        stack = stack.sort_values("total", ascending=False)
        return stack

    def discount_rewards(self, rewards, gamma=1):
        return np.round(
            np.multiply(gamma ** np.arange(len(rewards)), np.array(rewards)), 2
        )

    def explore(self, breadth=10, depth=5, gamma=1):

        if depth == 0 or len(self.moves) == 0:
            names, scores, moves = zip(*[(x.move_str, x.score, x) for x in self.stack])
            scores = self.discount_rewards(scores, gamma)
            return [
                {
                    "names": names,
                    "scores": scores,
                    "total": np.sum(scores),
                    # "moves":moves,
                }
            ]
        else:
            stacks = []

            # Parse and analyse each possible move
            moves = [Move(m, self.board) for m in self.moves]

            # Select randomly among possible moves
            if len(moves) > breadth:
                moves = np.random.choice(moves, size=breadth, replace=False)

            # For each move, recursively explore the following moves
            for move in moves:
                child_tree = RandomTreeSearch(self.board, move, stack=self.stack + [move])
                stack = child_tree.explore(breadth, depth - 1, gamma)
                stacks.extend(stack)
                self.children.append(child_tree)

            return stacks
