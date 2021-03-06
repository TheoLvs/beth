import datetime
import chess
import numpy as np
from chess import scan_forward,pgn
from ipywidgets import widgets, interact
from IPython.display import display
from copy import deepcopy

# Custom imports
from .players.human_player import HumanPlayer
from .move import Move
from .constants import COLORS, PIECES, PIECE_VALUES_BY_NAME,PIECE_VALUES_LIST
from .board import Board


class Game:
    def __init__(self, white=None, black=None):

        self.init_game(white, black)

    def _repr_html_(self):
        display(self.board)
        return None

    def init_game(self, white=None, black=None):

        # Init board
        self.board = Board()

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
        self.board_stack = [self.board.deepcopy()]

    def reset_game(self, white=None, black=None):

        # Init board
        self.board = Board()

        # Bind each player with the board as well to retrieve the moves
        self.white.bind(self, "WHITE")
        self.black.bind(self, "BLACK")

        # Stack moves
        self.board.moves = []
        self.board_stack = [deepcopy(self.board)]

    @property
    def turn(self):
        return "WHITE" if self.board.turn else "BLACK"

    @property
    def other_turn(self):
        return "BLACK" if self.board.turn else "WHITE"


    @property
    def san_moves_stack(self):
        return [str(x) for x in self.board.moves]


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

        if isinstance(value, list) or isinstance(value, tuple):
            values = [self.move(v) for v in value]
            return values
        else:
            if self.turn == "WHITE":
                move = self.white.move(value)
            else:
                move = self.black.move(value)

            # Store in custom representation
            move = Move(move, self.board)
            self.board.moves.append(move)
            self.board.push_san(move.move_str)

            # Append to board stack for game replay
            self.board_stack.append(self.board.deepcopy())

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

    def replay(self, interval=0.5):

        # Prepare widgets
        play = widgets.Play(
            value=0,
            min=0,
            max=len(self.board_stack) - 1,
            step=1,
            interval=interval * 1000,
            description="Press play",
            disabled=False,
        )

        slider = widgets.IntSlider(
            min=0, value=0, max=len(self.board_stack) - 1, step=1
        )
        widgets.jslink((play, "value"), (slider, "value"))

        # Visualize frames and widgets
        @interact(i=play)
        def show(i):
            return self.board_stack[i]

        display(slider)

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
        elif self.board.is_insufficient_material():
            return True
        else:
            return False

    def run(self, render=True):

        value = 0

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
                if self.board.is_checkmate():
                    value = 1 if self.turn == "BLACK" else -1

            # Clear the output to simulate an animation
            if not error:
                output.clear_output(wait=True)

        if not error:
            if render:
                with output:
                    display(self.board)

        return value

    def make_svg(self, size=400, **kwargs):
        svg_board = chess.svg.board(board=self.board, size=size, **kwargs)
        return svg_board

    def save_svg(self, filepath, size=400):
        svg_board = self.make_svg(size=size)
        with open(filepath, "w") as file:
            file.write(svg_board)

    def make_pgn(self,description = None,event = "Beth library development",game_round="1"):

        pgn_game = pgn.Game()
        pgn_game.headers["Date"] = datetime.datetime.now().isoformat()[:10]
        pgn_game.headers["Event"] = event
        pgn_game.headers["Round"] = game_round
        pgn_game.headers["Site"] = "Virtual"
        pgn_game.headers["White"] = str(self.white)
        pgn_game.headers["Black"] = str(self.black)
        if description is not None:
            pgn_game.headers["Description"] = description
        pgn_game.add_line(self.board.move_stack)

        return pgn_game


    def save_pgn(self,filepath = None,description = None,**kwargs):

        if filepath is None:
            date = datetime.datetime.now().isoformat()[:19].replace(":","-")
            filepath = f"PGN_beth_{date}.pgn"

        # Prepare file
        pgn_game = self.make_pgn(description = description,**kwargs)

        # Save file using print output directly in files
        print(pgn_game,file=open(filepath,"w"),end="\n\n")
        print(f"Game saved as pgn file at '{filepath}'")

