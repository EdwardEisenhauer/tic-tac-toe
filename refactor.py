from enum import Enum, auto
from math import pow
from matplotlib import pyplot
import copy
import random


class Field(Enum):
    EMPTY = 0
    X = 1
    O = -1

    def to_char(self):
        return {self.EMPTY: ' ', self.X: 'x', self.O: 'o'}[self]


class Mode(Enum):
    HUMAN = auto()
    RANDOM = auto()
    HEURISTIC = auto()
    Q = auto()


class Game:
    def __init__(self, players, board_size=3, draw=False):
        self.draw = draw
        self.board = Board(board_size)
        self.players = players
        self.current_player = players[0]
        self.winner = None
        self.stats = {'X': 0, 'O': 0, 'Tie': 0}

    def play(self):
        if self.draw:
            self.board.draw(heuristics=True)
        while self.winner is None:
            try:
                self.board.move(self.current_player.get_token(), self.current_player.make_move(self.board))
            except ValueError:
                print("This field is already taken!")
                continue
            except IndexError:
                print("The size of the board is 3x3!")
                continue
            if self.draw:
                self.board.draw(heuristics=True)
            self.winner = self.board.get_winner()
            self._switch_players()
        self._update_stats()

    def reset(self):
        self.board.reset()
        self.current_player = self.players[0]
        self.winner = None

    def _update_stats(self):
        self.stats[self.winner] = self.stats[self.winner] + 1

    def _switch_players(self):
        self.current_player = {self.players[0]: self.players[1], self.players[1]: self.players[0]}[self.current_player]

    def visualize_stats(self):
        pyplot.subplot(111)
        pyplot.bar(range(len(self.stats)), self.stats.values())
        pyplot.xticks(range(len(self.stats)), self.stats.keys())
        pyplot.show()


class Board:
    def __init__(self, size=3, state=None):
        self.size = size
        self.state = [Field.EMPTY] * int(pow(self.size, 2))
        self.actions = list(range(int(pow(self.size, 2))))
        self.heuristics = [0] * (2 * self.size + 2)
        if state is not None:
            self.state = state
            self._update_actions()
            self._calculate_heuristics()

    def _update_actions(self):
        self.actions = [i for i, x in enumerate(self.state) if x == Field.EMPTY]

    def _calculate_heuristics(self):
        for index, field in enumerate(self.state):
            row = int(index / self.size)
            column = index % self.size
            self.heuristics[row] += field.value
            self.heuristics[self.size + column] += field.value
            if row == column:
                self.heuristics[2 * self.size] += field.value
            if row + column == self.size - 1:
                self.heuristics[2 * self.size + 1] += field.value

    def _update_heuristics(self, token, index):
        row = int(index / self.size)
        column = index % self.size
        self.heuristics[column] += token.value
        self.heuristics[self.size + row] += token.value
        if row == column:
            self.heuristics[2 * self.size] += token.value
        if row + column == self.size - 1:
            self.heuristics[2 * self.size + 1] += token.value

    def move(self, token, index):
        if self.state[index] is not Field.EMPTY:
            raise ValueError
        if index > int(pow(self.size, 2)):
            raise IndexError
        self.state[index] = token
        self._update_actions()
        self._update_heuristics(token, index)

    def draw(self, heuristics=False):
        to_draw = list(map(lambda x: x.to_char(), self.state))
        if heuristics:
            header = "    " + "{:2}" * self.size
            print(header.format(*self.heuristics[0:self.size]))
            line = "{:2} {} " + "{:2}" * self.size + "|"
            for i in range(self.size):
                print(line.format(self.heuristics[self.size+i], '|', *to_draw[self.size * i:(i + 1) * self.size]))
            footer = "{:4}{:8}"
            print(footer.format(self.heuristics[2 * self.size + 1], self.heuristics[2 * self.size]))
        else:
            line = "| " + "{:2}" * self.size + "|"
            for i in range(self.size):
                print(line.format(*to_draw[self.size * i:(i + 1) * self.size]))
        print()

    def reset(self):
        self.state = [Field.EMPTY] * int(pow(self.size, 2))
        self.actions = list(range(int(pow(self.size, 2))))
        self.heuristics = [] * (2 * self.size + 2)

    def get_heuristics(self):
        return self.heuristics

    def get_possible_actions(self):
        return self.actions

    def get_size(self):
        return self.size

    def get_state(self):
        return self.state

    def get_winner(self):
        if self.size in self.heuristics:
            return 'X'
        elif -self.size in self.heuristics:
            return 'O'
        elif not self.actions:
            return 'Tie'
        else:
            return None


class Player:
    def __init__(self, token, mode=Mode.RANDOM):
        self.token = token
        self.mode = mode
        if mode is Mode.Q:
            self.q_agent = QAgent()

    def make_move(self, board):
        if self.mode == Mode.HUMAN:
            return self.make_human_move(board)
        elif self.mode == Mode.RANDOM:
            return self.make_random_move(board)
        elif self.mode == Mode.HEURISTIC:
            return self.make_heuristic_move(board)
        elif self.mode == Mode.Q:
            pass

    @staticmethod
    def make_human_move(board):
        row, column = None, None
        while row is None and column is None:
            try:
                row, column = map(int, input().split(' '))
            except ValueError:
                print("Provide two integers (row and column)")
            except KeyboardInterrupt:
                exit(0)
        return (row - 1) * board.get_size() + column - 1

    @staticmethod
    def make_random_move(board):
        return random.choice(board.get_possible_actions())

    def make_heuristic_move(self, board):
        current_heuristic_sum = sum(board.get_heuristics())
        optimal_field = None
        current_state = board.get_state()
        for index, field in enumerate(board.get_possible_actions()):
            new_board = Board(state=current_state.copy())
            new_board.move(self.token, field)
            predicted_heuristic = self._reward(new_board)
            if self.token.value*(predicted_heuristic - current_heuristic_sum) > 0:
                current_heuristic_sum = predicted_heuristic
                optimal_field = field
        if optimal_field is None:
            optimal_field = random.choice(board.get_possible_actions())
        return optimal_field

    def make_q_move(self, board):
        pass

    def _reward(self, board):
        heuristic = board.get_heuristics()
        if board.get_size() in heuristic:
            return 100*self.token.value
        elif -board.get_size() in heuristic:
            return -100*self.token.value
        else:
            return sum(heuristic)

    def get_token(self):
        return self.token


class QAgent:
    def __init__(self, alpha=1, gamma=0, epsilon=0):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon


tic_tac_toe = Game((Player(Field.X), Player(Field.O, Mode.HEURISTIC)), board_size=3, draw=True)
tic_tac_toe.play()
# tic_tac_toe.visualize_stats()
