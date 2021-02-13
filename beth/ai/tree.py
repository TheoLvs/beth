

from ..players.ai_player import AIPlayer,AIBrain
from ..tree.tree import MoveTree

import random


class TreeSearchBrain(AIBrain):

    def __init__(self,breadth = 10,depth = 3):

        self.breadth = breadth
        self.depth = depth

    
    def predict_next(self,game):

        tree = MoveTree(game.board)
        moves = tree.search_depth(self.breadth,self.depth)
        best_moves = moves.loc[moves["total"] == moves["total"].max()]["names"].tolist()
        move = random.choice(best_moves)[0]
        return move



class TreeSearchAI(AIPlayer):
    def __init__(self,breadth = 10,depth = 3,**kwargs):
        brain = TreeBrain(breadth,depth)
        super().__init__(brain,**kwargs)