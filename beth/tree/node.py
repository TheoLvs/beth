import numpy as np
import pandas as pd
from copy import deepcopy

from ..move import Move


class TreeNode:
    def __init__(self, board, move=None, stack=None,best_score = 0):

        # Prepare attributes
        # In particular copy the board to reproduce and propagate the node
        self.board = deepcopy(board)
        self.move = move
        self.best_score = best_score
        self.score = 0
        self.color = "WHITE" if self.board.turn else "BLACK"

        # If a move is provided, push to the copied board
        if move is not None:
            self.board.push(move.move)
            self.score = self.move.score

        # Recursivity attributes
        # Previous moves will be stacked for each node to traverse backward
        if stack is None:
            self.stack = []
        else:
            self.stack = stack

        # Prepare to stack children nodes
        self.children = []

        # Get all the legal moves
        # Important to compute the legal moves after having pushed the move
        # The parser needs te right context of the board
        self.legal_moves = list(self.board.legal_moves)

    def has_children(self):
        return len(self.legal_moves) > 0 

    def is_white_turn(self):
        # Help to determine who is the maximizing player
        return self.board.turn

    def __repr__(self):
        if len(self.stack) == 0:
            moves_stack = "..."
        else:
            moves_stack = "-".join([str(x) for x in self.stack])
        return f"{self.color.title()}Node({moves_stack},best_score={self.best_score},score={self.score})"

    def discount_rewards(self, rewards, gamma=1):
        return np.round(
            np.multiply(gamma ** np.arange(len(rewards)), np.array(rewards)), 2
        )


    def next_moves(self):

        # Get all the legal moves
        moves = self.legal_moves

        # Parse each move, in particular to get the score
        moves = [Move(m, self.board) for m in moves]

        # We sort by score the moves given the color
        # Indeed self.board.turn = True if it's white turn for example, 
        # Then we want a descending order to get the best moves
        moves = sorted(moves,key = lambda x : x.score,reverse = self.board.turn)
        return moves

    def next_nodes(self,select_moves_fn = None):

        # Parse and analyse each possible move
        moves = self.next_moves()

        # Select randomly among possible moves
        if select_moves_fn is not None:
            moves = select_moves_fn(moves)

        # For each move, recursively explore the following moves
        children = []
        for move in moves:
            child_tree = TreeNode(self.board, move, stack=self.stack + [move],best_score = self.best_score + move.score)
            children.append(child_tree)
        return children


    def expand(self,depth=5,select_moves_fn = None):

        if depth == 0 or not self.has_children():
            self.best_score = self.score
            self.debug_score = [self.score]
            names, scores, moves = zip(*[(x.move_str, x.score, x) for x in self.stack])
            stack = [
                {
                    "names": names,
                    "scores": scores,
                    "total": np.sum(scores),
                }
            ]
            return self.score,stack
        else:
            stacks = []

            # Get all children
            saved_children = []
            children = self.next_nodes(select_moves_fn)

            score = -np.inf if self.is_white_turn() else np.inf
            best_child = None

            for child in children:
                child_score,stack = child.expand(depth-1,select_moves_fn)

                if self.is_white_turn():
                    if child_score > score:
                        score = child_score
                        best_child = child
                else:
                    if child_score < score:
                        score = child_score
                        best_child = child

                stacks.extend(stack)
                saved_children.append(child)
                # print("#"*depth,child,score,child_score,self.is_white_turn())
                    
            self.best_score = self.score + best_child.best_score
            self.debug_score = [self.score,*best_child.debug_score]
            self.children = saved_children
            return self.best_score,stacks