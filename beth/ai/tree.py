from ..players.ai_player import AIPlayer
from ..tree.tree import TreeSearch

import random


class TreeSearchAI(AIPlayer):
    def __init__(self, depth=3, breadth=None, max_time=None, **kwargs):
        brain = TreeSearch(depth=depth, breadth=breadth, max_time=max_time)
        super().__init__(brain, **kwargs)

    def __str__(self):
        return f"TreeSearchAI(depth={self.brain.depth},breadth={self.brain.breadth})"
