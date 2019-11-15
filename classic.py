import copy
import random
import time
from enum import Enum, auto


class Field(Enum):
    EMPTY = 0
    X = 1
    O = -1

    def __neg__(self):
        return Field(-self.value)

    def to_char(self):
        return {self.EMPTY: ' ', self.X: 'x', self.O: 'o'}[self]

class Game:
    def __init__(self, player1, player2):
        self.turn = Field.X
        self.board = Board()
        self.winner = None
        self.playerX = player1
        self.playerO = player2
        self.current_player = self.playerX
        self.stats = {'X': 0, 'O': 0, 'Tie': 0}

    def play(self):
        while not self.winner:
            # self.board.draw()
            # print(self.turn.name + "'s turn")
            # time.sleep(1)
            try:
                self.board.move(self.turn, self.current_player.make_move(self.board))
            except ValueError:
                print("This field is already taken!")
                continue
            except IndexError:
                print("The size of the board is 3x3!")
                continue
            self._end_turn()
        # self.board.draw()
        self._update_stats()
        return self.winner

    def reset(self):
        self.turn = Field.X
        self.board = Board()
        self.current_player = self.playerX
        self.winner = None

    def _update_stats(self):
        if self.winner == Field.X:
            self.stats['X'] = self.stats['X'] + 1
        elif self.winner == Field.O:
            self.stats['O'] = self.stats['O'] + 1
        elif self.winner == Field.EMPTY:
            self.stats['Tie'] = self.stats['Tie'] + 1

    def get_stats(self):
        return self.stats

    def _end_turn(self):
        self.turn = -self.turn
        self.current_player = {self.playerX: self.playerO, self.playerO: self.playerX}[self.current_player]
        self.winner = self.board.get_winner()


class Board:
    def __init__(self):
        self.state = [Field.EMPTY] * 9
        # self.state = [Field.X,Field.X,Field.O,
        #               Field.O,Field.O,Field.X,
        #               Field.X,Field.O,Field.EMPTY]
        self.action = list(range(9))
        self.heuristics = [0] * 8

    def move(self, token, index):
        row = int(index / 3)
        column = index % 3
        if self.state[index] is not Field.EMPTY: raise ValueError
        if row > 2 or column > 2: raise IndexError
        self.state[index] = token
        self._update_action()
        self._update_heuristics(token, row, column)

    def _update_action(self):
        self.action = [i for i, x in enumerate(self.state) if x == Field.EMPTY]

    def _update_heuristics(self, token, row, column):
        self.heuristics[row] += token.value
        self.heuristics[3 + column] += token.value
        if row == column: self.heuristics[6] += token.value
        if row + column == 2: self.heuristics[7] += token.value

    def get_winner(self):
        if 3 in self.heuristics: return Field.X
        if -3 in self.heuristics: return Field.O
        if not self.action: return Field.EMPTY

    def draw(self):
        board = list(map(lambda x: x.to_char(), self.state))
        print(board[0:3])
        print(board[3:6])
        print(board[6:9])
        print()

    def get_state(self):
        return self.state

    def get_state_in_str(self):
        return ''.join(list(map(lambda x: x.to_char(), self.state)))

    def get_possible_moves(self):
        random.shuffle(self.action)
        return self.action

    def get_heuristics(self):
        return self.heuristics

class Mode(Enum):
    HUMAN = auto()
    RANDOM = auto()
    AI = auto()


class Player:
    def __init__(self, field, mode):
        self.token = field
        self.mode = mode

    def make_move(self, board):
        if self.mode == Mode.HUMAN:
            while row is None and column is None:
                try:
                    row, column = map(int, input().split(' '))
                except ValueError:
                    print("Provide two integers (row and column)")
                    continue
                except KeyboardInterrupt:
                    print('\n')
                    exit(0)
            return (row - 1) * 3 + column - 1

        elif self.mode == Mode.RANDOM: return random.choice(board.get_possible_moves())
        elif self.mode == Mode.AI:
            current_heuristic = sum(board.get_heuristics())
            optimal_field = None
            for idx, field in enumerate(board.get_possible_moves()):
                new_board = copy.deepcopy(board)
                new_board.move(self.token, field)
                predicted_heuristics = sum(new_board.get_heuristics())
                if self.token.value*(predicted_heuristics - current_heuristic) > 0:
                    current_heuristic = predicted_heuristics
                    optimal_field = field
            if optimal_field == None: return random.choice(new_board.get_possible_moves())
            else: return optimal_field


# class MDPAgent:
#     def __init__(self):
#         self.states
#         self.actions
#         self.gamma
#         self.reward


game = Game(Player(Field.X, Mode.RANDOM), Player(Field.O, Mode.AI))
# result = game.play()
# if result == Field.EMPTY:
    # print("It is a tie!")
# else:
    # print(result.name + "s have won!")

for i in range(100):
    game.play()
    game.reset()
print(game.get_stats())