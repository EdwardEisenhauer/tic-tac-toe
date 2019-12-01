from board import Board
from enums import Mode
from funs import state_to_str, state_to_actions
from qtable import QTable

import random


class Player:
    """
    Represents agents and perform actions on the game board
    """
    def __init__(self, token, mode=Mode.RANDOM):
        """""
        :param token: Player's representation on the game board (X or O)
        :param mode: Human/Random/Simple Heuristics/Q-Learning

        """
        self.token = token
        self.mode = mode

    def make_move(self, board):
        """
        Performs a move on the board
        :param board: game board to modify
        :return:
        """
        if self.mode == Mode.RANDOM:
            move = self.make_random_move(board)
        board[move] = self.token
        return move

    @staticmethod
    def make_random_move(board):
        """
        :param board: game board
        :return: index of a random move from the possible ones
        """
        return random.choice(board.get_actions())

    def _calculate_heuristic(self, board):
        heuristic = board.winning_conditions
        if board.size in heuristic:
            return 10*self.token.value
        elif -board.size in heuristic:
            return -10*self.token.value
        else:
            return sum(heuristic)

    def reward(self, board):
        if board.get_winner() is self.token:
            return 10
        elif board.get_winner() is -self.token:
            return -10
        else:
            return 0

    @staticmethod
    def _from_state_str_to_actions(state):
        return [i for i, x in enumerate(state) if x == ' ']

    def get_token(self):
        return self.token


class Human(Player):
    def __init__(self, token):
        self.token = token
        self.mode = Mode.HUMAN

    def make_move(self, board):
        """
        Ask the human player to indicate next move's coordinates and performs it
        :param board: game board to modify
        :return: index of a move chosen by the human player
        """
        row, column = None, None
        while row is None and column is None:
            try:
                row, column = map(int, input().split(' '))
                if row - 1 not in range(board.size) or column - 1 not in range(board.size):
                    raise IndexError
            except IndexError:
                print("The size of the board is " + str(board.size) + "x" + str(board.size) + "!")
                row, column = None, None
                continue
            except ValueError:
                print("Provide two integers (row and column)")
            except KeyboardInterrupt:
                exit(0)
        move = (row - 1) * board.size + column - 1
        board[move] = self.token
        return move


class Heuristic(Player):
    def __init__(self, token):
        self.token = token
        self.mode = Mode.HEURISTIC

    def make_move(self, board):
        """
        Chooses a move based on a simple heuristics and performs it
        :param board: game board to modify
        :return: index of a move chosen by the heuristic algorithm
        """
        current_heuristic_sum = sum(board.winning_conditions)
        optimal_field = None
        current_state = board.get_state()
        for index, field in enumerate(board.get_actions()):
            new_board = Board(state=current_state.copy())
            new_board[field] = self.token
            predicted_heuristic = self._calculate_heuristic(new_board)
            if self.token.value*(predicted_heuristic - current_heuristic_sum) > 0:
                current_heuristic_sum = predicted_heuristic
                optimal_field = field
        if optimal_field is None:
            optimal_field = self.make_random_move(board)
        board[optimal_field] = self.token
        return optimal_field


class QAgent(Player):
    def __init__(self, token, alpha=1.0, gamma=1.0, epsilon=1.0):
        """
        :param alpha: Learning rate [0,1]
        :param gamma: Discount factor [0,1]
        :param epsilon: Exploration factor [0,1]
        """
        self.token = token
        self.mode = Mode.Q
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.q_table = QTable()
        self.states_history = []  # Keeps the information about one episode of a game
        self.actions_history = []  # Keeps the information about the actions in an episode

    def make_move(self, board):
        """
        Chooses a move based on a Q-Learning agent
        :param board: game board to modify
        :return: index of a move chosen by the Q-Learning agent
        """
        current_state = board.get_state()
        current_state_str = state_to_str(current_state)

        if current_state_str not in self.q_table.q_table:
            self.q_table.add_state(current_state_str, board.get_actions())
        print("Q-TABLE BEFORE MOVE")
        self.q_table.draw(current_state_str)
        if random.uniform(0, 1) < self.epsilon:
            q_move = self.make_random_move(board)
            print('RANDOM Q-MOVE: ' + str(q_move + 1))
        else:
            q_move = self.q_table.get_max_q_move(current_state_str)
            print('MAX Q-MOVE: ' + str(q_move + 1))
        board[q_move] = self.token

        self.states_history.append(current_state_str)
        self.actions_history.append(q_move)

        return q_move

    def update_q_table(self, reward, state=None, action=None):
        """
        Updates Q-Table based on the equation:
        Q(s,a) = R(s,a) + maxQ'(s',a')
        :param state:
        :param action:
        :param reward:
        :return:
        """
        if state or action is None:
            state = self.states_history[-1]
            action = self.actions_history[-1]
        else:
            state = state_to_str(state)
            if state not in self.q_table.q_table:
                self.q_table.add_state(state)
        next_state = self._next_state(state, action)                  # s'
        max_q_value = self.q_table.get_max_q_move_value(next_state)  # maxQ'(s',a')
        self.q_table.q_table[state][action] = reward + self.gamma * max_q_value
        print(str(state) + ":" + str(action) + " = " + str(reward) + " + " + str(self.gamma * max_q_value))

    def _next_state(self, state, action) -> str:
        """
        Adds a new previously non-existing state to the Q-Table
        :param state:
        :param action:
        :return:
        """
        next_state = state[:action] + self.token.to_char() + state[action + 1:]
        if next_state not in self.q_table.q_table:
            actions = self._from_state_str_to_actions(next_state)
            self.q_table.add_state(next_state, actions)
        return next_state
