import numpy as np
import pandas as pd
from .node import TreeNode


class BaseTreeSearch:
    def __init__(self, board):

        self.node = TreeNode(board)

    def select_moves_fn(self,*args,**kwargs):
        raise NotImplementedError("The method select_moves_fn has not be overriden")
        

    def search(self,depth=5):
        best_score,stack = self.node.expand(depth,self.select_moves_fn)
        print(best_score,self.node.debug_score[1:])
        stack = pd.DataFrame(stack)

        # # If player is black
        # if self.node.board.turn == 0:
        #     stack["total"] *= -1

        stack["next_move"] = stack["names"].map(lambda x : x[0])
        stack["is_best_move"] = (stack["scores"] == tuple(self.node.debug_score[1:]))
        stack = stack.sort_values("is_best_move", ascending=False)
        return stack
