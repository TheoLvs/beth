import numpy as np
import pandas as pd
from .tree import BaseTreeSearch


class RandomTreeSearch(BaseTreeSearch):

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