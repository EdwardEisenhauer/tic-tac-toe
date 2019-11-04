from enum import Enum, auto

class Field(Enum):
    EMPTY = 0
    X = 1
    O = -1

    def __neg__(self):
        return Field(-self.value)

    def to_char(self):
        return {self.EMPTY: ' ', self.X: 'x', self.O: 'o'}[self]


class Game():
    def __init__(self):
        self.turn = Field.X
        self.board = Board()

    def play(self):
        while not self.board.is_win():
            self.board.draw()
            print(self.turn.name + "'s turn")
            try:
                row, column = map(int, input().split(' '))
            except ValueError:
                print("Provide integers only!")
                continue
            try:
                self.board.move(self.turn, row, column)
            except ValueError:
                print("This field is already taken!")
                continue
            except IndexError:
                print("The size of the board is 3x3!")
                continue
            self.turn = -self.turn
        self.board.draw()
        print((-self.turn).name + "s have won!")


class Board:
    def __init__(self):
        self.board = [Field.EMPTY] * 9
        self.heuristics = [0] * 8

    def move(self, Field, row, column):
        index = (row-1)*3+column-1
        if self.board[index] is not Field.EMPTY: raise ValueError
        if row > 3 or column > 3: raise IndexError
        self.board[index] = Field
        self._update_heuristics(Field, row, column)

    def _update_heuristics(self, Field, row, column):
        self.heuristics[row-1] += Field.value
        self.heuristics[3+column-1] += Field.value
        if (row == column): self.heuristics[6] += Field.value
        if (row + column == 4): self.heuristics[7] += Field.value
        return

    def is_win(self):
        if 3 in list(map(abs, self.heuristics)):
            return True
        else:
            return False

    def draw(self):
        board = list(map(lambda x: x.to_char(), self.board))
        print(board[0:3])
        print(board[3:6])
        print(board[6:9])
        print()

    def get_state_in_str(self):
        return ''.join(list(map(lambda x: x.to_char(), self.board)))

class Player:
    def __init__(self, field):
        self.token = field

class MDPAgent:
    def __init__(self):
        self.states
        self.actions
        self.gamma
        self.reward
        
game = Game()
game.play()
