import numpy as np
import pandas as pd
from .tree import BaseTreeSearch

class MinimaxTreeSearch(BaseTreeSearch):

    def __init__(self, board,breadth = 3):

        super().__init__(board)
        self.breadth = breadth

        
    def select_moves_fn(self,moves):

        # Select randomly among possible moves
        if len(moves) > self.breadth:
            moves = np.random.choice(moves, size=self.breadth, replace=False)
            return moves
        else:
            return moves


    def expand(self,node,depth,is_maximizing_player = True):
        if depth == 0 or not node.has_children():
            node.final_value = node.value
            return node.value
        else:
            if is_maximizing_player:
                value = -np.inf
                for child in node.children:
                    child_value = minimax(child,depth - 1,False)
                    value = max([value,child_value])
            else:
                value = np.inf
                for child in node.children:
                    child_value = minimax(child,depth - 1,True)
                    value = min([value,child_value])
                    
            node.final_value = node.value + value
            return value