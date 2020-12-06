
import time


class Player:
    def __init__(self,wait = None):
        self.wait_duration = wait

    def wait(self):
        if self.wait_duration is not None:
            time.sleep(self.wait_duration)

    def bind(self,board,color):
        self.board = board
        self.color = color

    def move(self,value):
        pass