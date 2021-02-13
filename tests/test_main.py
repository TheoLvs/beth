from beth.game import Game
from beth.players.random_player import RandomPlayer
from beth.players.human_player import HumanPlayer

def test_example_move():
    """Main test will test several aspects
    So much for unitary testing
    - Manual Player is working
    - Game engine is working
    - You can play moves as list of moves
    - It understands san and lan notation
    - It returns scores with piece values as list
    """

    # Instantiate player and game
    white = HumanPlayer()
    black = HumanPlayer()
    game = Game(white,black)

    # Play sequences of moves
    scores = game.move(["e4","d5","d5","g8f6","d4","f6d5"])

    assert scores == [0,0,1,0,0,-1]