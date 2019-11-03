from enum import Enum, auto

class Field(Enum):
    EMPTY = auto()
    X = auto()
    O = auto()

def to_char(field):
    return {Field.EMPTY: ' ', Field.X: 'x', Field.O: 'o'}[field]


class Board:
    def __init__(self):
        self.board = [Field.EMPTY] * 9

    def move(self, Field, row, column):
        index = (row-1)*3+column-1
        print(index)
        if self.board[index] is not ' ':
            print("ok")
            self.board[index] = Field

    def draw(self):
        board = list(map(to_char,self.board))
        print(board[0:3])
        print(board[3:6])
        print(board[6:9])

board = Board()
board.draw()
board.move(Field.X, 2, 2)
board.draw()
