import numpy as np
import pandas as pd
import random
from .node import TreeNode


class TreeSearch:
    def __init__(self,board,depth = 3,breadth = None):
        if board is not None:
            self.node = TreeNode(board)
        self.breadth = breadth
        self.depth = depth
        self.memory = []


    def select_moves_fn(self,moves):

        # If no breadth-pruning, we simply keep all the moves
        if self.breadth is None or len(moves) < self.breadth:
            return moves

        # Select randomly among the legal moves
        else:
            moves = np.random.choice(moves, size=self.breadth, replace=False)
            return moves


    def explore(self,depth=5):

        # Expand the node using minimax algorithm
        # Select move function can be overriden
        best_score,stack = self.node.expand(depth,self.select_moves_fn)

        # Convert the move stack to a datafrmae
        stack = pd.DataFrame(stack)

        # # If player is black
        # if self.node.board.turn == 0:
        #     stack["total"] *= -1

        # Extract the next move
        stack["next_move"] = stack["names"].map(lambda x : x[0])

        # Evaluate which moves are considered the best by the minimax rules
        stack["is_best_move"] = (stack["scores"] == tuple(self.node.debug_score[1:]))
        stack = stack.sort_values("is_best_move", ascending=False)
        return stack

    def predict_next(self, game):

        # Initialize the first node from the board
        self.node = TreeNode(game.board)

        # Explore the possible moves
        moves = self.explore(depth = self.depth)

        # Selec all the moves that are the best (according to minimax rules)
        # And store to memory
        best_moves = moves.loc[moves["is_best_move"] == True]
        self.memory.append(best_moves)

        # Select a random move among the possible best ones
        next_moves = best_moves["next_move"].tolist()
        move = random.choice(next_moves)
        return move