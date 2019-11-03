from enum import Enum, auto

class Field(Enum):
    EMPTY = 0
    X = 1
    O = -1

def to_char(field):
    return {Field.EMPTY: ' ', Field.X: 'x', Field.O: 'o'}[field]

class Board:
    def __init__(self):
        self.board = [Field.EMPTY] * 9
        self.heuristics = [0] * 8

    def move(self, Field, row, column):
        index = (row-1)*3+column-1
        if self.board[index] is not Field.EMPTY:
            raise ValueError
        self.board[index] = Field
        self._update_heuristics(Field, row, column)

    def _update_heuristics(self, Field, row, column):
        self.heuristics[row-1] += Field.value
        self.heuristics[3+column-1] += Field.value
        if (row == column): self.heuristics[6] += Field.value
        if (row == -column): self.heuristics[7] += Field.value
        print(self.heuristics)
        return

    def is_win(self):
        if 3 in self.heuristics:
            return True
        else:
            return False

    def draw(self):
        board = list(map(to_char,self.board))
        print(board[0:3])
        print(board[3:6])
        print(board[6:9])
        print()

board = Board()
board.draw()
board.move(Field.X, 2, 2)
board.draw()
board.move(Field.O, 3, 3)
board.draw()
board.move(Field.X, 3, 1)
board.draw()
