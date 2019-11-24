import copy
import random
import sys
import time
from enum import Enum, auto
from matplotlib import pyplot


class Field(Enum):
    EMPTY = 0
    X = 1
    O = -1

    def __neg__(self):
        return Field(-self.value)

    def to_char(self):
        return {self.EMPTY: ' ', self.X: 'x', self.O: 'o'}[self]


class Game:
    def __init__(self, player1, player2, draw=False):
        self.turn = Field.X
        self.board = Board()
        self.winner = None
        self.playerX = player1
        self.playerO = player2
        self.current_player = self.playerX
        self.draw = draw
        self.stats = {'X': 0, 'O': 0, 'Tie': 0}

    def play(self):
        while not self.winner:
            if self.draw == True:
                self.board.draw_heuristics()
                print(self.turn.name + "'s turn")
            try:
                self.board.move(self.turn, self.current_player.make_move(self.board))
            except ValueError:
                print("This field is already taken!")
                continue
            except IndexError:
                print("The size of the board is 3x3!")
                continue
            self._end_turn()
        if self.draw == True:
            self.board.draw_heuristics()
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
    def __init__(self, state=None):
        self.state = [Field.EMPTY] * 9
        self.action = list(range(9))
        self.heuristics = [0] * 8
        if state is not None:
            self.state = state
            self._update_action()
            self._calculate_heuristics()

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

    def _calculate_heuristics(self):
        for index, field in enumerate(self.state):
            row = int(index / 3)
            column = index % 3
            self.heuristics[row] += field.value
            self.heuristics[3 + column] += field.value
            if row == column: self.heuristics[6] += field.value
            if row + column == 2: self.heuristics[7] += field.value

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

    def draw_heuristics(self):
        board = list(map(lambda x: x.to_char(), self.state))
        print("  {} {} {}".format(self.heuristics[3], self.heuristics[4], self.heuristics[5]))
        print("{} |{} {} {}|".format(self.heuristics[0], board[0], board[1], board[2]))
        print("{} |{} {} {}|".format(self.heuristics[1], board[3], board[4], board[5]))
        print("{} |{} {} {}|".format(self.heuristics[2], board[6], board[7], board[8]))
        print("{}       {}".format(self.heuristics[7], self.heuristics[6]))


class Mode(Enum):
    HUMAN = auto()
    RANDOM = auto()
    AI = auto()
    Q = auto()


class Player:
    def __init__(self, field, mode, epsilon=None, learning_rate=None, gamma=None):
        self.token = field
        self.mode = mode
        if mode == Mode.Q:
            self.q_table = {}
            self.epsilon = epsilon
            self.learning_rate = learning_rate
            self.gamma = gamma

    def make_move(self, board):
        if self.mode == Mode.HUMAN:
            row = None
            column = None
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
        elif self.mode == Mode.RANDOM:
            return random.choice(board.get_possible_moves())
        elif self.mode == Mode.AI:
            current_heuristic_sum = sum(board.get_heuristics())
            optimal_field = None
            current_state = board.get_state()
            for idx, field in enumerate(board.get_possible_moves()):
                new_board = Board(current_state.copy())
                new_board.move(self.token, field)
                predicted_heuristics = self._reward(new_board)
                if self.token.value*(predicted_heuristics - current_heuristic_sum) > 0:
                    current_heuristic_sum = predicted_heuristics
                    optimal_field = field
            if optimal_field is None: return random.choice(board.get_possible_moves())
            else: return optimal_field
        elif self.mode == Mode.Q:
            current_state = board.get_state()
            current_state_str = board.get_state_in_str()
            if current_state_str not in self.q_table:
                self.q_table[current_state_str] = {action:0 for action in board.get_possible_moves()}
            if random.uniform(0,1) < self.epsilon:
                random_move = random.choice(board.get_possible_moves())
                new_board = Board(current_state.copy())
                new_board.move(self.token, random_move)
                self.q_table[current_state_str][random_move] = self.q_table[current_state_str][random_move] + self.learning_rate*(self._reward(new_board) + self.gamma*self._get_max_q_table_value(new_board.get_state_in_str()))
                print("RANDOM MOVE")
                print(self._print_q_table(current_state_str))
                return random_move
            else:
                print("MAX_Q")
                print(self._print_q_table(current_state_str))
                max_q_move = self._get_max_q_table_move(current_state_str)
                new_board = Board(current_state.copy())
                new_board.move(self.token, max_q_move)
                self.q_table[current_state_str][max_q_move] = self.q_table[current_state_str][max_q_move] + self.learning_rate*(self._reward(new_board) + self.gamma*self._get_max_q_table_value(new_board.get_state_in_str()))
                return max_q_move

    def _get_max_q_table_move(self, state):
        return max(self.q_table[state], key=lambda k: self.q_table[state][k])

    def _get_max_q_table_value(self, state):
        try:
            max_q = max(self.q_table[state])
        except KeyError:
            return 0
        return max_q

    def _print_q_table(self, state):
        fields = self.q_table[state].copy()
        for field in range(9):
            if field not in fields:
                fields[field] = state[field]
        print("|{} {} {}|".format(fields[0], fields[1], fields[2]))
        print("|{} {} {}|".format(fields[3], fields[4], fields[5]))
        print("|{} {} {}|".format(fields[6], fields[7], fields[8]))

    def _reward(self, board):
        heuristics = board.get_heuristics()
        if 3 in heuristics: return 100*self.token.value
        elif -3 in heuristics: return -100*self.token.value
        else: return sum(heuristics)

    def get_mode(self):
        return self.mode

    # def update_q_table(self,state,action):
    #     self.q_table[current_state_str][max_q_move] = self.q_table[current_state_str][max_q_move] + self.learning_rate*(self._reward(new_board) + self.gamma*self._get_max_q_table_value(new_board.get_state_in_str()))



# class MDPAgent:
#     def __init__(self):
#         self.states
#         self.actions
#         self.gamma
#         self.reward

games_to_play = int(sys.argv[1])

game = Game(Player(Field.X, Mode.Q, epsilon=0.1, learning_rate=0.1, gamma=0), Player(Field.O, Mode.RANDOM), draw=True)
# result = game.play()
# if result == Field.EMPTY:
#     print("It is a tie!")
# else:
#     print(result.name + "s have won!")

x = []
y = []
pyplot.plot(x, y, '-')
pyplot.draw()
pyplot.pause(1)


for i in range(games_to_play):
    game.play()
    game.reset()
    x.append(len(x)+1)
    y.append(game.get_stats()['X']/len(x))
    pyplot.ylim(bottom=0,top=1)
    pyplot.plot(x, y, '-')
    pyplot.draw()
    pyplot.pause(0.0001)

stats = game.get_stats()
print(stats)

pyplot.bar(range(len(stats)), list(stats.values()), align='center')
pyplot.xticks(range(len(stats)), list(stats.keys()))
pyplot.ylim(top=games_to_play)
pyplot.show(block=False)
pyplot.pause(4)
pyplot.close()
