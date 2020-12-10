import chess
from ipywidgets import widgets
from IPython.display import display
from .players.human_player import HumanPlayer


class Game:
    def __init__(self, white=None, black=None):

        self.init_game(white, black)

    def _repr_html_(self):
        return self.board._repr_html_()

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
        self.white.bind(self.board, "WHITE")
        self.black.bind(self.board, "BLACK")

    def reset_game(self, white=None, black=None):

        # Init board
        self.board = chess.Board()

        # Bind each player with the board as well to retrieve the moves
        self.white.bind(self.board, "WHITE")
        self.black.bind(self.board, "BLACK")

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

    def move(self, value=None):

        if self.turn == "WHITE":
            return self.white.move(value)
        else:
            return self.black.move(value)

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
                        raise

            # Stop if the game is done
            if self.done():
                game_loop = False

            # Clear the output to simulate an animation
            output.clear_output(wait=True)

        with output:
            display(self.board)
