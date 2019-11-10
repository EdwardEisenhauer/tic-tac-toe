from enum import Enum, auto


class Field(Enum):
    EMPTY = 0
    X = 1
    O = -1

    def __neg__(self):
        return Field(-self.value)

    def to_char(self):
        return {self.EMPTY: ' ', self.X: 'x', self.O: 'o'}[self]


class Board:
    def __init__(self):
        self.state = [Field.EMPTY] * 9
        self.action = list(range(9))
        self.heuristics = [0] * 8

    def move(self, field, row, column):
        index = (row - 1) * 3 + column - 1
        if self.state[index] is not field.EMPTY: raise ValueError
        if row > 3 or column > 3:
            raise IndexError
        self.state[index] = field
        self._update_action()
        self._update_heuristics(field, row, column)

    def _update_action(self):
        self.action = [i for i, x in enumerate(self.state) if x == Field.EMPTY]

    def _update_heuristics(self, field, row, column):
        self.heuristics[row - 1] += field.value
        self.heuristics[3 + column - 1] += field.value
        if row == column:
            self.heuristics[6] += field.value
        if row + column == 4:
            self.heuristics[7] += field.value

    def is_win(self):
        if 3 in list(map(abs, self.heuristics)):
            return True
        else:
            return False

    def draw(self):
        board = list(map(lambda x: x.to_char(), self.state))
        print(board[0:3])
        print(board[3:6])
        print(board[6:9])
        print()

    def get_state_in_str(self):
        return ''.join(list(map(lambda x: x.to_char(), self.state)))


class Mode(Enum):
    PVP = auto()
    PVAI = auto()
    AIVAI = auto()


class Game:
    def __init__(self):
        self.turn = Field.X
        self.board = Board()
        self.mode = Mode.PVP

    def play(self):
        while not self.board.is_win():
            self.board.draw()
            print(self.turn.name + "'s turn")
            try:
                row, column = map(int, input().split(' '))
            except ValueError:
                print("Provide two integers (row and column)")
                continue
            except KeyboardInterrupt:
                print('\n')
                exit(0)
            try:
                self.board.move(self.turn, row, column)
            except ValueError:
                print("This field is already taken!")
                continue
            except IndexError:
                print("The size of the board is 3x3!")
                continue
            self._end_turn()
        self.board.draw()
        print((-self.turn).name + "s have won!")
        return -self.turn

    def _end_turn(self):
        self.turn = -self.turn


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


