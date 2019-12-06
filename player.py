from board import Board
from enums import Field, Mode
from funs import draw_board, state_to_str
from qtable import QTable

import math
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
        if len(board.get_actions()) is 1:
            move = self.make_random_move(board)
            board[move] = self.token
            return move
        else:
            score, move = self.minmax(board, self.token)
            board[move] = self.token
            return move

    def _get_field_with_highest_winning_condition(self, board):
        empty_fields = board.get_actions()
        highest_field = [-math.inf, empty_fields[0]]
        for field in empty_fields:
            field_heuristic = board.winning_conditions[field % board.size] + board.winning_conditions[int(field/board.size) + 3]
            if field % 4:
                field_heuristic = field_heuristic + board.winning_conditions[2 * board.size]
            if field % 2:
                field_heuristic = field_heuristic + board.winning_conditions[2 * board.size + 1]
            if field_heuristic > highest_field[0]:
                highest_field = [field_heuristic, field]
        return highest_field

    def minmax(self, board, token, depth=2):
        new_board = Board(board.size, board.get_state().copy())
        if new_board.get_winner():
            if abs(new_board.get_winner().value) is 1:
                return new_board.get_winner().value * -math.inf
        if depth == 0:
            return self._get_field_with_highest_winning_condition(new_board)

        if token is Field.O:
            best = [-math.inf, []]
            for field in new_board.get_actions():
                if len(new_board.get_actions()) is 1:
                    return self._get_field_with_highest_winning_condition(new_board)
                else:
                    next_board = Board(new_board.size, new_board.get_state().copy())
                    next_board[field] = Field.O
                    value = self.minmax(next_board, Field.X, depth - 1)
                    if value == math.inf:
                        return [value, field]
                    if value[0] > best[0]:
                        best = [value[0], field]
        else:
            best = [math.inf, []]
            for field in new_board.get_actions():
                if len(new_board.get_actions()) is 1:
                    return self._get_field_with_highest_winning_condition(new_board)
                else:
                    next_board = Board(new_board.size, new_board.get_state().copy())
                    next_board[field] = Field.X
                    value = self.minmax(next_board, Field.O, depth - 1)
                    if value == -math.inf:
                        return [value, field]
                    if not isinstance(value, list):
                        print("ops")
                        print(type(value))
                        print(value)
                    if value[0] < best[0]:
                        best = [value[0], field]
        if best[0] == -math.inf:
            return self._get_field_with_highest_winning_condition(next_board)
        elif best[0] == math.inf:
            return self._get_field_with_highest_winning_condition(next_board)
        return best

    # def make_move(self, board):
    #     """
    #     Chooses a move based on a simple heuristics and performs it
    #     :param board: game board to modify
    #     :return: index of a move chosen by the heuristic algorithm
    #     """
    #     current_heuristic_sum = sum(board.winning_conditions)
    #     optimal_field = None
    #     current_state = board.get_state()
    #     for index, field in enumerate(board.get_actions()):
    #         # Gosh this needs rewriting into minmax
    #         new_board = Board(state=current_state.copy())
    #         new_board[field] = self.token
    #         if new_board.get_winner() is self.token:
    #             optimal_field = field
    #             break
    #         predicted_heuristic = self._calculate_heuristic(new_board)
    #         if self.token.value*(predicted_heuristic - current_heuristic_sum) > 0:
    #             current_heuristic_sum = predicted_heuristic
    #             optimal_field = field
    #     if optimal_field is None:
    #         optimal_field = self.make_random_move(board)
    #     board[optimal_field] = self.token
    #     return optimal_field


class QAgent(Player):
    def __init__(self, token, alpha=1.0, gamma=1.0, epsilon=1.0, filename=None):
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
        if filename is not None:
            self.q_table.read_from_file(filename)

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
        # print("Q-TABLE BEFORE MOVE")
        # self.q_table.draw(current_state_str)
        if random.uniform(0, 1) < self.epsilon:
            q_move = self.make_random_move(board)
            # print('RANDOM Q-MOVE: ' + str(q_move + 1))
        else:
            q_move = self.q_table.get_max_q_move(current_state_str)
            # print('MAX Q-MOVE: ' + str(q_move + 1))
        board[q_move] = self.token

        self.states_history.append(current_state_str)
        self.actions_history.append(q_move)

        return q_move

    def update_q_table(self, reward):
        """
        Updates Q-Table based on the equation:
        newQ(s,a) = (1-a) * Q(s,a) + a * *(g^i * R(s,a)) maxQ'(s',a')
        :param state:
        :param action:
        :param reward:
        :return:
        """
        # print("Q(s,a) = R + g*maxQ(s',a')")
        # print(len(self.states_history))
        for i in range(1, len(self.states_history)):
            state = self.states_history[-i]
            action = self.actions_history[-i]
            next_state = self._next_state(state, action)                  # s'
            # max_q_value = self.q_table.get_max_q_move_value(next_state)  # maxQ'(s',a')
            # if max_q_value > 0:
            #     print("maxQ'(s',a') = " + str(max_q_value))
            new_value = (1 - self.alpha) * self.q_table.q_table[state][action] + self.alpha * (self.gamma**i * reward)
            self.q_table.q_table[state][action] = new_value
            # print(str(state) + ":" + str(action) + " = " + str(round(new_value, 3)))
            # print(str(round(new_value, 3)) + "=" + str(self.alpha) + "*(" + str(reward) + " + " + str(round(self.gamma**i, 3)) + " * " + str(max_q_value) + ")")

    def reset_history(self):
        self.states_history = []
        self.actions_history = []

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
