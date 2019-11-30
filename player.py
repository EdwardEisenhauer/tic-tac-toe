from board import Board
from enums import Mode
from funs import state_to_str

from math import sqrt
import random


class Player:
    def __init__(self, token, mode=Mode.RANDOM, alpha=1.0, gamma=1.0, epsilon=1.0):
        self.token = token
        self.mode = mode
        if self.mode is Mode.Q:
            self.alpha = alpha      # learning rate
            self.gamma = gamma      # discout factor
            self.epsilon = epsilon  # exploration rate
            self.q_table = QTable()

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
        current_state_str = state_to_str(current_state)
        self.q_table.draw(current_state_str)
        if current_state_str not in self.q_table.get_q_table():
            self.q_table.add_state(current_state_str, board.get_actions())
        if random.uniform(0, 1) < self.epsilon:
            q_move = random.choice(board.get_actions())
            print('RANDOM Q-MOVE: ' + str(q_move+1))
        else:
            q_move = self.q_table.get_max_q_move(current_state_str)
            print('MAX Q-MOVE: ' + str(q_move+1))
        self.update_q_table(current_state, q_move, self._reward(board))
        return q_move

    def _calculate_heuristic(self, board):
        heuristic = board.get_winning_conditions()
        if board.get_size() in heuristic:
            return 10*self.token.value
        elif -board.get_size() in heuristic:
            return -10*self.token.value
        else:
            return sum(heuristic)

    def _reward(self, board):
        if board.get_winner() is self.token:
            return 10
        elif board.get_winner() is -self.token:
            return -10
        else:
            return 0

    def update_q_table(self, state, action, reward):
        """Q(s,a) = R(s,a) + maxQ'(s',a')"""
        state = state_to_str(state)                                 # s
        new_state = self._new_state(state, action)                  # s'
        max_q_value = self.q_table.get_max_q_move_value(new_state)  # maxQ'(s',a')
        self.q_table.get_q_table()[state][action] = reward + self.gamma * max_q_value
        print(str(state) + ":" + str(action) + " = " + str(reward) + " + " + str(self.gamma * max_q_value))

    def _new_state(self, state, action) -> str:
        new_state = state[:action] + self.token.to_char() + state[action + 1:]
        if new_state not in self.q_table.get_q_table():
            actions = self._from_state_str_to_actions(new_state)
            self.q_table.add_state(new_state, actions)
        return new_state

    @staticmethod
    def _from_state_str_to_actions(state):
        return [i for i, x in enumerate(state) if x == ' ']

    def get_token(self):
        return self.token


class QTable:
    def __init__(self):
        self.q_table = {}

    def add_state(self, state, actions):
        self.q_table[state] = {action: 0 for action in actions}

    def get_max_q_move(self, state: list):
        return max(self.q_table[state], key=lambda key: self.q_table[state][key])

    def get_max_q_move_value(self, state: list):
        print(max(self.q_table[state]))
        return max(self.q_table[state])

    def get_q_table(self):
        return self.q_table

    def draw(self, state):
        """This function needs rewriting - gonna do this later tho"""
        size = int(sqrt(len(state)))
        if state in self.q_table:
            to_draw = self.q_table[state].copy()
        else:
            return
        for i in range(len(state)):
            if i not in to_draw:
                to_draw[i] = state[i]
        line = "   | " + "{:5}" * size + "|"
        list_to_draw = [''] * len(state)
        for key in to_draw:
            if type(to_draw[key]) is float:
                list_to_draw[int(key)] = str(round(to_draw[key], 3))
            else:
                list_to_draw[int(key)] = str(to_draw[key])
        for i in range(size):
            print(line.format(*list_to_draw[size * i:(i + 1) * size]))
        print()
