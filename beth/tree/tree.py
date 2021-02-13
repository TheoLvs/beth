import numpy as np
import pandas as pd
from copy import deepcopy

from ..move import Move


class MoveTree:
    def __init__(self,board,move=None,stack = None):

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


    def search_depth(self,breadth = 10,depth = 5):
        print(f"Searching for {depth} moves ahead with {breadth} choices - {breadth**depth} possibilities")
        stack = self.explore(breadth,depth)
        stack = pd.DataFrame(stack).sort_values("total",ascending = False)
        stack
        return stack


    def explore(self,breadth = 10,depth = 5):
        if depth == 0:
            names,scores,moves = zip(*[(x.move_str,x.score,x) for x in self.stack])
            return [{
                "names":names,
                "scores":scores,
                "total":np.sum(scores),
                # "moves":moves,
            }]
        else:
            stacks = []

            # Parse and analyse each possible move
            moves = [Move(m,self.board) for m in self.moves]

            # Select randomly among possible moves
            if len(moves) > breadth:
                moves = np.random.choice(moves,size=breadth,replace = False)

            # For each move, recursively explore the following moves
            for move in moves:
                child_tree = MoveTree(self.board,move,stack=self.stack + [move])
                stack = child_tree.explore(breadth,depth - 1)
                stacks.extend(stack)
                self.children.append(child_tree)

            return stacks

