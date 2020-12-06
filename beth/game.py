
import chess
from ipywidgets import widgets
from IPython.display import display




class Game:

    def __init__(self):

        self.reset_game()


    def _repr_html_(self):
        return self.board._repr_html_()
        

    def reset_game(self):
        self.board = chess.Board() 
    
    def get_turn(self):
        return "WHITE" if self.board.turn else "BLACK"

    def notebook_play(self):

        # Define inputs
        move = widgets.Text(description="Next move")
        button = widgets.Button(description="Send")
        inputs = widgets.HBox([move, button])

        # Define output and display everything
        output = widgets.Output()
        display(inputs,output)

        with output:
            print(self.get_turn())
            display(self.board)

        # Define interactions
        def on_button_clicked(b):
            with output:
                output.clear_output()
                try:
                    print(self.get_turn())
                    self.board.push_san(move.value)
                    display(self.board)
                except Exception as e:
                    print(e)
                    display(self.board)




        button.on_click(on_button_clicked)