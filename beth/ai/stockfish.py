from ..players.ai_player import AIPlayer

import random
import chess.engine


class StockfishAI(AIPlayer):

    def __init__(self,path,ELO=None,depth = None,level = None,wait = 0,limit = 0.1):

        self.path = path
        self.engine = chess.engine.SimpleEngine.popen_uci(path)
        self.wait_duration = wait
        self.limit = 0.1

        if ELO is not None:
            self.engine.configure({"UCI_Elo":ELO})

    def __str__(self):
        return f"StockfishAI()"
    
    def predict_next(self,board,limit = None):
        if limit is None:
            limit = self.limit
        result = self.engine.play(board, chess.engine.Limit(time=limit))
        return result.move

    def move(self, value=None):

        # Overriding default behavior by calling the moves
        if value is not None:
            return value

        # Default behavior where the brain object predicts the next move
        else:
            self.wait()
            return self.predict_next(self.game.board)
