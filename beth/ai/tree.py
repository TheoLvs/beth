from ..players.ai_player import AIPlayer
from ..tree.tree import TreeSearch

import random


class TreeSearchAI(AIPlayer):

    def __init__(self,depth=3,breadth = None,**kwargs):
        brain = TreeSearch(board = None,depth = depth,breadth = breadth)
        super().__init__(brain, **kwargs)

    def __str__(self):
        return f"TreeSearchAI(depth={self.brain.depth},breadth={self.brain.breadth})"