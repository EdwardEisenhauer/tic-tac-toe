from enum import Enum, auto
from math import pow, sqrt
from matplotlib import pyplot
# import copy
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


def state_to_str(state):
    return ''.join(list(map(lambda x: x.to_char(), state)))


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
                self.current_player.make_move(self.board)
            except ValueError:
                print("This field is already taken!")
                continue
            if self.draw:
                self.board.draw(heuristics=True)
            self.winner = self.board.get_winner()
            self._switch_players()
            print("------------")
        self._update_stats()

    def reset(self):
        self.board.reset()
        self.current_player = self.players[0]
        self.winner = None

    def _update_stats(self):
        winner_in_str = {Field.X: 'X', Field.O: 'O', Field.EMPTY: 'Tie'}[self.winner]
        self.stats[winner_in_str] = self.stats[winner_in_str] + 1

    def _switch_players(self):
        self.current_player = {self.players[0]: self.players[1], self.players[1]: self.players[0]}[self.current_player]

    def visualize_stats(self):
        pyplot.subplot(111)
        pyplot.bar(range(len(self.stats)), self.stats.values())
        pyplot.xticks(range(len(self.stats)), self.stats.keys())
        print(self.stats)
        pyplot.show()


class Board:
    def __init__(self, size=3, state=None):
        self.size = size
        self.state = [Field.EMPTY] * int(pow(self.size, 2))
        self.actions = list(range(int(pow(self.size, 2))))
        self.winning_conditions = [0] * (2 * self.size + 2)
        if state is not None:
            self.state = state
            self._update_actions()
            self._calculate_winning_conditions()

    def _update_actions(self):
        self.actions = [i for i, x in enumerate(self.state) if x == Field.EMPTY]

    def _calculate_winning_conditions(self):
        for index, field in enumerate(self.state):
            row = int(index / self.size)
            column = index % self.size
            self.winning_conditions[row] += field.value
            self.winning_conditions[self.size + column] += field.value
            if row == column:
                self.winning_conditions[2 * self.size] += field.value
            if row + column == self.size - 1:
                self.winning_conditions[2 * self.size + 1] += field.value

    def _update_winning_conditions(self, token, index):
        row = int(index / self.size)
        column = index % self.size
        self.winning_conditions[column] += token.value
        self.winning_conditions[self.size + row] += token.value
        if row == column:
            self.winning_conditions[2 * self.size] += token.value
        if row + column == self.size - 1:
            self.winning_conditions[2 * self.size + 1] += token.value

    def move(self, token, index):
        row = int(index / self.size)
        column = index % self.size
        print(row, column)
        if self.state[index] is not Field.EMPTY:
            raise ValueError
        if row not in range(self.size) or column not in range(self.size):
            raise IndexError
        self.state[index] = token
        self._update_actions()
        self._update_winning_conditions(token, index)

    def draw(self, heuristics=False):
        to_draw = list(map(lambda x: x.to_char(), self.state))
        if heuristics:
            header = "    " + "{:2}" * self.size
            print(header.format(*self.winning_conditions[0:self.size]))
            line = "{:2} {} " + "{:2}" * self.size + "|"
            for i in range(self.size):
                print(line.format(self.winning_conditions[self.size + i], '|', *to_draw[self.size * i:(i + 1) * self.size]))
            footer = "{:4}{:" + str(2 * self.size + 2) + "}"
            print(footer.format(self.winning_conditions[2 * self.size + 1], self.winning_conditions[2 * self.size]))
        else:
            line = "| " + "{:2}" * self.size + "|"
            for i in range(self.size):
                print(line.format(*to_draw[self.size * i:(i + 1) * self.size]))

    def reset(self):
        self.state = [Field.EMPTY] * int(pow(self.size, 2))
        self.actions = list(range(int(pow(self.size, 2))))
        self.winning_conditions = [0] * (2 * self.size + 2)

    def get_winning_conditions(self):
        return self.winning_conditions

    def get_actions(self):
        return self.actions

    def get_size(self):
        return self.size

    def get_state(self):
        return self.state

    def get_state_in_str(self):
        return ''.join(list(map(lambda x: x.to_char(), self.state)))

    def get_winner(self):
        if self.size in self.winning_conditions:
            return Field.X
        elif -self.size in self.winning_conditions:
            return Field.O
        elif not self.actions:
            return Field.EMPTY
        else:
            return None


class Player:
    def __init__(self, token, mode=Mode.RANDOM, alpha=1.0, gamma=0.0, epsilon=1.0):
        self.token = token
        self.mode = mode
        if mode is Mode.Q:
            self.q_agent = QAgent(alpha, gamma, epsilon)

    def make_move(self, board):
        if self.mode == Mode.HUMAN:
            board.move(self.token, self.make_human_move(board))
        elif self.mode == Mode.RANDOM:
            board.move(self.token, self.make_random_move(board))
        elif self.mode == Mode.HEURISTIC:
            board.move(self.token, self.make_heuristic_move(board))
        elif self.mode == Mode.Q:
            board.move(self.token, self.make_q_move(board))

    @staticmethod
    def make_human_move(board):
        row, column = None, None
        while row is None and column is None:
            try:
                row, column = map(int, input().split(' '))
                if row - 1 not in range(board.get_size()) or column - 1 not in range(board.get_size()):
                    raise IndexError
            except IndexError:
                print("The size of the board is " + str(board.get_size()) + "x" + str(board.get_size()) + "!")
                row, column = None, None
                continue
            except ValueError:
                print("Provide two integers (row and column)")
            except KeyboardInterrupt:
                exit(0)
        return (row - 1) * board.get_size() + column - 1

    @staticmethod
    def make_random_move(board):
        return random.choice(board.get_actions())

    def make_heuristic_move(self, board):
        current_heuristic_sum = sum(board.get_winning_conditions())
        optimal_field = None
        current_state = board.get_state()
        for index, field in enumerate(board.get_actions()):
            new_board = Board(state=current_state.copy())
            new_board.move(self.token, field)
            predicted_heuristic = self._calculate_heuristic(new_board)
            if self.token.value*(predicted_heuristic - current_heuristic_sum) > 0:
                current_heuristic_sum = predicted_heuristic
                optimal_field = field
        if optimal_field is None:
            optimal_field = random.choice(board.get_actions())
        return optimal_field

    def make_q_move(self, board):
        current_state = board.get_state()
        current_state_str = board.get_state_in_str()
        q_move = self.q_agent.make_q_move(board)
        self.q_agent.draw_q_table(current_state_str)
        self.q_agent.update_q_table(current_state, q_move, self._reward(board))
        return q_move

    def _calculate_heuristic(self, board):
        heuristic = board.get_winning_conditions()
        if board.get_size() in heuristic:
            return 10*self.token.value
        elif -board.get_size() in heuristic:
            return -10*self.token.value
        else:
            return sum(heuristic)

    def get_token(self):
        return self.token

    def _reward(self, board):
        if board.get_winner is self.token:
            return 1
        else:
            return -1


class QAgent:
    def __init__(self, alpha=1.0, gamma=0.0, epsilon=1.0):
        self.alpha = alpha      # learning rate
        self.gamma = gamma      #
        self.epsilon = epsilon  # exploration rate
        self.q_table = {}

    def make_q_move(self, board):
        current_state = board.get_state()
        current_state_str = board.get_state_in_str()
        if current_state_str not in self.q_table:
            self.q_table[current_state_str] = {action: 0 for action in board.get_actions()}
        if random.uniform(0, 1) < self.epsilon:
            q_move = random.choice(board.get_actions())
        else:
            q_move = self._get_max_q_move(state_to_str(current_state))
        return q_move

    def draw_q_table(self, state):
        """This function needs rewriting - gonna do this later tho"""
        size = int(sqrt(len(state)))
        to_draw = self.q_table[state].copy()
        for i in range(len(state)):
            if i not in to_draw:
                to_draw[i] = state[i]
        line = "   | " + "{:2}" * size + "|"
        list_to_draw = [''] * len(state)
        for key in to_draw:
            list_to_draw[int(key)] = str(to_draw[key])
        for i in range(size):
            print(line.format(*list_to_draw[size * i:(i + 1) * size]))
        print()

    def update_q_table(self, state, action, reward):
        state = state_to_str(state)
        self.q_table[state][action] = reward
        pass

    def _get_max_q_move(self, state):
        return max(self.q_table[state], key=lambda key: self.q_table[state][key])

    def _reward(self):

        return 0


games_to_play = 1
tic_tac_toe = Game((Player(Field.X), Player(Field.O, mode=Mode.Q, epsilon=0.5)), board_size=3, draw=True)
for episode in range(games_to_play):
    tic_tac_toe.play()
    tic_tac_toe.reset()
# tic_tac_toe.visualize_stats()
