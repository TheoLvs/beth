import numpy as np
import pandas as pd
import random
from .node import TreeNode


class TreeSearch:
    def __init__(self, depth=3, breadth=None, pruning=True, max_time=None):

        self.breadth = breadth
        self.depth = depth
        self.pruning = pruning
        self.max_time = max_time
        self.memory = []

    def sample_moves(self, moves):

        # If no breadth-pruning, we simply keep all the moves
        if self.breadth is None or len(moves) < self.breadth:
            return moves

        # Select randomly among the legal moves
        else:
            if True:
                moves = moves[: self.breadth]
            else:
                moves = np.random.choice(moves, size=self.breadth, replace=False)
            return moves

    def explore(self, game, depth=5, pruning=True):

        self.node = TreeNode(game.board, max_time=self.max_time)

        # Expand the node using minimax algorithm
        # Select move function can be overriden
        best_score, stack = self.node.expand(depth, pruning, self.sample_moves)

        # Convert the move stack to a datafrmae
        stack = pd.DataFrame(stack)

        # Extract the next move
        stack["next_move"] = stack["names"].map(lambda x: x[0])

        # Evaluate which moves are considered the best by the minimax rules
        stack["is_best_move"] = stack["scores"] == tuple(self.node.trace_score[1:])
        stack = stack.sort_values("is_best_move", ascending=False)
        return stack

    def predict_next(self, game):

        # Explore the possible moves
        moves = self.explore(game, depth=self.depth, pruning=self.pruning)

        # Selec all the moves that are the best (according to minimax rules)
        # And store to memory
        best_moves = moves.loc[moves["is_best_move"] == True]
        self.memory.append(best_moves)

        # Select a random move among the possible best ones
        next_moves = best_moves["next_move"].tolist()
        move = random.choice(next_moves)
        return move
