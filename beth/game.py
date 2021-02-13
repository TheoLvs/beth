import chess
from ipywidgets import widgets
from IPython.display import display
from .players.human_player import HumanPlayer
from .move import Move

from chess import scan_forward

from .constants import COLORS,PIECES,PIECE_VALUES_BY_NAME


class Game:
    def __init__(self, white=None, black=None):

        self.init_game(white, black)

    def init_game(self, white=None, black=None):

        # Init board
        self.board = chess.Board()

        # Init Human Players if no player type is specified
        if white is None:
            white = HumanPlayer()
        if black is None:
            black = HumanPlayer()

        # Store as attributes
        self.white = white
        self.black = black

        # Bind each player with the board as well to retrieve the moves
        self.white.bind(self, "WHITE")
        self.black.bind(self, "BLACK")

        # Stack moves
        self.board.moves = []

    def reset_game(self, white=None, black=None):

        # Init board
        self.board = chess.Board()

        # Bind each player with the board as well to retrieve the moves
        self.white.bind(self, "WHITE")
        self.black.bind(self, "BLACK")

        # Stack moves
        self.board.moves = []

    @property
    def turn(self):
        return "WHITE" if self.board.turn else "BLACK"

    @property
    def other_turn(self):
        return "BLACK" if self.board.turn else "WHITE"

    def get_turn_description(self):
        return (
            f"Next is {self.turn} - {self.other_turn} has played {self.get_last_move()}"
        )

    def get_last_move(self):
        return str(self.get_moves()[-1])

    def get_moves(self):
        return self.board.move_stack

    def get_moves_san(self):
        return self.board.moves

    def get_legal_moves_san(self):
        return [self.board.san(x) for x in self.board.legal_moves]

    def move(self, value=None):

        if isinstance(value,list):
            values = [self.move(v) for v in value]
            return values
        else:
            if self.turn == "WHITE":
                move = self.white.move(value)
            else:
                move = self.black.move(value)

            # Store in custom representation
            move = Move(move,self.board)
            self.board.moves.append(move)
            self.board.push_san(move.move_str)
            return move.score

    def notebook_play(self):

        # Define inputs
        move = widgets.Text(description="Next move")
        button = widgets.Button(description="Send")
        inputs = widgets.HBox([move, button])

        # Define output and display everything
        output = widgets.Output()
        display(inputs, output)

        with output:
            print("Next is WHITE")
            display(self.board)

        # Define interactions
        def on_button_clicked(b):
            with output:
                output.clear_output()
                try:
                    self.move(move.value)
                    print(self.get_turn_description())
                    display(self.board)
                except Exception as e:
                    raise e
                    print(e)
                    display(self.board)

        button.on_click(on_button_clicked)

    def done(self):
        """Indicator if the game is finished
        Used to end game loops

        Can be included:
        - board.is_stalemate()
        - board.is_insufficient_material()
        - board.is_game_over()

        Returns:
            bool: If the game is finished
        """
        if self.board.is_checkmate():
            return True
        elif self.board.is_stalemate():
            return True
        elif self.board.is_fivefold_repetition():
            return True
        elif self.board.is_seventyfive_moves():
            return True
        else:
            return False

    def run(self, render=True):

        # Init and display ouput
        output = widgets.Output()
        display(output)

        # Run game loop
        game_loop = True
        error = False

        while game_loop:

            with output:

                # Display and one player move
                try:
                    if render:
                        display(self.board)
                    self.move()

                # Stop on Keyboard Interrupt (debug in notebook)
                except KeyboardInterrupt:
                    game_loop = False

                # Stop on other errors
                except Exception as e:

                    # If errors are due to invalid moves
                    # Restart input only if different than exit
                    # If exit stops the execution (debug in notebook)
                    if "invalid san" in str(e):
                        move = str(e).split(": ")[1].replace("'", "")
                        if move == "exit":
                            game_loop = False

                    # For any other errors, stop the loop and raise the exception
                    else:
                        game_loop = False
                        error = True
                        raise e
            
            # if not game_loop and error:
            #     raise Exception

            # Stop if the game is done
            if self.done():
                game_loop = False

            # Clear the output to simulate an animation
            if not error:
                output.clear_output(wait=True)

        if not error:
            with output:
                display(self.board)

    def make_svg(self, size=400, **kwargs):
        svg_board = chess.svg.board(board=self.board, size=size, **kwargs)
        return svg_board

    def save_svg(self, filepath, size=400):
        svg_board = self.make_svg(size=size)
        with open(filepath, "w") as file:
            file.write(svg_board)


    def get_pieces_positions_by_type(self,piece_type:str,color:str = None):

        # Prepare binary representation of pieces
        piece_type = piece_type.upper()
        if piece_type == "BISHOP":
            pieces = self.board.bishops
        elif piece_type == "PAWN":
            pieces = self.board.pawns
        elif piece_type == "ROOK":
            pieces = self.board.rooks
        elif piece_type == "KNIGHT":
            pieces = self.board.knights
        elif piece_type == "QUEEN":
            pieces = self.board.queens
        elif piece_type == "KING":
            pieces = self.board.kings
        else:
            raise Exception(f"Piece type {piece_type} is not among {PIECES}")

        # Prepare binary color mask
        if color is None:
            mask = self.board.occupied
        else:
            if isinstance(color,str):
                color = 1 if color.upper() == "WHITE" else 0
            mask = self.board.occupied_co[color]

        return list(scan_forward(pieces & mask))



    def get_pieces_positions(self):

        pieces = {}

        for i,color in enumerate(COLORS):
            pieces[color] = {}
            for piece_type in PIECES:
                pieces[color][piece_type] = self.get_pieces_positions_by_type(piece_type,i)

        return pieces


    def get_scores(self):
        pos = self.get_pieces_positions()
        scores = {}

        for i,color in enumerate(COLORS):
            score = 0
            for piece_type in PIECES:
                if piece_type != "KING":
                    n_pieces = len(pos[color][piece_type])
                    score += n_pieces * PIECE_VALUES_BY_NAME[piece_type]
            scores[color] = score

        scores["DIFF"] = scores["WHITE"] - scores["BLACK"] 

        return scores



