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


def test_berger():
    """Checkmate in 3 moves test
    Depend on a constant value for checkmates of 100
    """
    # Instantiate player and game
    white = HumanPlayer()
    black = HumanPlayer()
    game = Game(white,black)

    # Play sequences of moves
    berger = ['e4', 'e5', 'Bc4', 'd6', 'Qh5', 'a6', 'Qxf7#']
    scores = game.move(berger)

    assert scores == [0, 0, 0, 0, 0, 0, 100]

def test_promotion():
    """Test if promotion parsing works
    ie for example here when a pawn arrives to the last line and is promoted to Queen
    The move value is = queen value - pawn value exchanged + eventually the piece we captured
    In the example below we capture a knight and transform to queen, hence value = 9 - 1 + 3 
    """

    # Instantiate player and game
    white = HumanPlayer()
    black = HumanPlayer()
    game = Game(white,black)

    # Play sequences of moves
    promotion_moves = ['b4', 'Nf6', 'b5', 'e5', 'b6', 'd5', 'bxa7', 'd4',"axb8=Q"]
    scores = game.move(promotion_moves)

    assert scores == [0, 0, 0, 0, 0, 0, 1, 0, 11]
