from ..players.ai_player import AIPlayer, AIBrain
from ..tree.random import RandomTreeSearch

import random


class TreeSearchBrain(AIBrain):
    def __init__(self, breadth=10, depth=3,gamma = 1):

        self.breadth = breadth
        self.depth = depth
        self.gamma = gamma
        self.memory = []

    def predict_next(self, game):

        tree = RandomTreeSearch(game.board)
        moves = tree.search_depth(self.breadth, self.depth,self.gamma)
        best_moves = moves.loc[moves["total"] == moves["total"].max()]
        self.memory.append(best_moves)
        next_moves = best_moves["next_move"].tolist()
        move = random.choice(next_moves)
        return move


class TreeSearchAI(AIPlayer):

    def __init__(self, breadth=10, depth=3,gamma=1, **kwargs):
        brain = TreeSearchBrain(breadth, depth,gamma)
        super().__init__(brain, **kwargs)

    def __str__(self):
        return f"TreeSearchAI(breadth={self.brain.breadth},depth={self.brain.depth},gamma={self.brain.gamma})"