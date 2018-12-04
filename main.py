import random
import math
import copy
import inspect


class Board:
    def __init__(self):
        self.board_state = [
            [[' ', ' ', ' ', ' '],
             [' ', ' ', ' ', ' '],
             [' ', ' ', ' ', ' '],
             [' ', ' ', ' ', ' ']],

            [[' ', ' ', ' ', ' '],
             [' ', ' ', ' ', ' '],
             [' ', ' ', ' ', ' '],
             [' ', ' ', ' ', ' ']],

            [[' ', ' ', ' ', ' '],
             [' ', ' ', ' ', ' '],
             [' ', ' ', ' ', ' '],
             [' ', ' ', ' ', ' ']],

            [[' ', ' ', ' ', ' '],
             [' ', ' ', ' ', ' '],
             [' ', ' ', ' ', ' '],
             [' ', ' ', ' ', ' ']]]

        self.field_heuristics = [
            [[0, 0, 0, 0],
             [0, 0, 0, 0],
             [0, 0, 0, 0],
             [0, 0, 0, 0]],

            [[0, 0, 0, 0],
             [0, 0, 0, 0],
             [0, 0, 0, 0],
             [0, 0, 0, 0]],

            [[0, 0, 0, 0],
             [0, 0, 0, 0],
             [0, 0, 0, 0],
             [0, 0, 0, 0]],

            [[0, 0, 0, 0],
             [0, 0, 0, 0],
             [0, 0, 0, 0],
             [0, 0, 0, 0]]]

        self.wins = []
        for i in range(76):
            self.wins.append(0)
        return

    def get_empty_fields(self):
        empty_fields = []
        for layer_idx, layer in enumerate(self.board_state):
            for row_idx, row in enumerate(layer):
                for col_idx, field in enumerate(row):
                    if field is ' ':
                        empty_fields.append([layer_idx, row_idx, col_idx])
        return empty_fields

    def get_lowest_empty_field(self):
        empty_fields = self.get_empty_fields()
        lowest_field = [math.inf, empty_fields[0]]
        for idx, field in enumerate(self.get_empty_fields()):
            field_heuristic = self.field_heuristics[field[0]][field[1]][field[2]]
            if  field_heuristic< lowest_field[0]:
                lowest_field = [field_heuristic, field]
        return lowest_field[1]

    def get_highest_empty_field(self):
        empty_fields = self.get_empty_fields()
        highest_field = [-math.inf, empty_fields[0]]
        for idx, field in enumerate(self.get_empty_fields()):
            field_heuristic = self.field_heuristics[field[0]][field[1]][field[2]]
            if field_heuristic > highest_field[0]:
                highest_field = [field_heuristic, field]
        return highest_field

    def get_vertical_fields(self, field):
        row, column = field[1], field[2]
        fields = []
        for z in range(4):
            fields.append([z, row, column])
        return fields

    def get_column_fields(self, field):
        layer, column = field[0], field[2]
        fields = []
        for y in range(4):
            fields.append([layer, y, column])
        return fields

    def get_row_fields(self, field):
        layer, row = field[0], field[1]
        fields = []
        for x in range(4):
            fields.append([layer, row, x])
        return fields

    def get_diagonal_fields(self, field):
        layer, row, column = field[0], field[1], field[2]
        fields = []
        if row == column:
            for x in range(4):
                fields.append([layer, x, x])
        if (row + column) == 3:
            for x in range(4):
                fields.append([layer, x, 3-x])
        if layer == column:
            for x in range(4):
                fields.append([x, row, x])
        if (layer + column) == 3:
            for x in range(4):
                fields.append([x, row, 3-x])
        if layer == row:
            for x in range(4):
                fields.append([x, x, column])
        if (layer + row) == 3:
            for x in range(4):
                fields.append([x, 3-x, column])
        if layer == row == column:
            for x in range(4):
                fields.append([x, x, x])
        if layer == row and row + column == 3:
            for x in range(4):
                fields.append([x, x, 3-x])
        if row == column and layer + row == 3:
            for x in range(4):
                fields.append([x, 3-x, 3-x])
        if layer == column and layer + row == 3:
            for x in range(4):
                fields.append([x, 3-x, x])
        return fields

    def make_move(self, player, layer, row, column):
        if self.board_state[layer][row][column] is not ' ':
            raise ValueError
        self.board_state[layer][row][column] = player
        self._update_field_heuristic(player, layer, row, column)
        self._update_wins(player, layer, row, column)

    def _update_field_heuristic(self, player, layer, row, column):
        for field in self.get_vertical_fields([layer, row, column]):
            self.field_heuristics[field[0]][field[1]][field[2]] = self.field_heuristics[field[0]][field[1]][field[2]] + {'x': -1, 'o': 1}[player]
        for field in self.get_row_fields([layer, row, column]):
            self.field_heuristics[field[0]][field[1]][field[2]] = self.field_heuristics[field[0]][field[1]][field[2]] + {'x': -1, 'o': 1}[player]
        for field in self.get_column_fields([layer, row, column]):
            self.field_heuristics[field[0]][field[1]][field[2]] = self.field_heuristics[field[0]][field[1]][field[2]] + {'x': -1, 'o': 1}[player]
        for field in self.get_diagonal_fields([layer, row, column]):
            self.field_heuristics[field[0]][field[1]][field[2]] = self.field_heuristics[field[0]][field[1]][field[2]] + {'x': -1, 'o': 1}[player]

    def _update_wins(self, player, layer, row, column):
        self.wins[4 * row + column] = self.wins[4 * row + column] + {'x': -1, 'o': 1}[player]
        self.wins[16 + 4 * layer + column] = self.wins[16 + 4 * layer + column] + {'x': -1, 'o': 1}[player]
        self.wins[32 + 4 * layer + row] = self.wins[32 + 4 * layer + row] + {'x': -1, 'o': 1}[player]
        if row == column:
            self.wins[48 + layer] += {'x': -1, 'o': 1}[player]
        if (row + column) == 3:
            self.wins[52 + layer] += {'x': -1, 'o': 1}[player]
        if layer == column:
            self.wins[56 + row] += {'x': -1, 'o': 1}[player]
        if (layer + column) == 3:
            self.wins[60 + row] += {'x': -1, 'o': 1}[player]
        if layer == row:
            self.wins[64 + column] += {'x': -1, 'o': 1}[player]
        if (layer + row) == 3:
            self.wins[68 + column] += {'x': -1, 'o': 1}[player]
        if layer == row == column:
            self.wins[72] += {'x': -1, 'o': 1}[player]
        if layer == row and row + column == 3:
            self.wins[73] += {'x': -1, 'o': 1}[player]
        if row == column and layer + row == 3:
            self.wins[74] += {'x': -1, 'o': 1}[player]
        if layer == column and layer + row == 3:
            self.wins[75] += {'x': -1, 'o': 1}[player]

    def is_win(self):
        if '-4' in str(self.wins):
            return 'x'
        elif '4' in str(self.wins):
            return 'o'
        else:
            return False

    def draw_board(self):
        print("         ________________")
        print("        / {} / {} / {} / {} /|".format(self.board_state[0][0][0], self.board_state[0][0][1], self.board_state[0][0][2],
                                                      self.board_state[0][0][3]))
        print("       /___/___/___/___/ |")
        print("      / {} / {} / {} / {} /  |".format(self.board_state[0][1][0], self.board_state[0][1][1], self.board_state[0][1][2], self.board_state[0][1][3]))
        print("     /___/___/___/___/   |")
        print("    / " + self.board_state[0][2][0] + " / " + self.board_state[0][2][1] + " / " + self.board_state[0][2][2] + " / " +
              self.board_state[0][2][3] + " /    |")
        print("   /___/___/___/___/     |")
        print("  / " + self.board_state[0][3][0] + " / " + self.board_state[0][3][1] + " / " + self.board_state[0][3][2] + " / " +
              self.board_state[0][3][3] + " /      |")
        print(" /___/___/___/___/       |")
        print("|       |________|_______|")
        print(
            "|       / " + self.board_state[1][0][0] + " / " + self.board_state[1][0][1] + " /|" + self.board_state[1][0][2] + " / " +
            self.board_state[1][0][3] + " /|")
        print("|      /___/___/_|_/___/ |")
        print("|     / " + self.board_state[1][1][0] + " / " + self.board_state[1][1][1] + " / " + self.board_state[1][1][2] + "|/ " +
              self.board_state[1][1][3] + " /  |")
        print("|    /___/___/___|___/   |")
        print("|   / " + self.board_state[1][2][0] + " / " + self.board_state[1][2][1] + " / " + self.board_state[1][2][2] + " /|" +
              self.board_state[1][2][3] + " /    |")
        print("|  /___/___/___/_|_/     |")
        print("| / " + self.board_state[1][3][0] + " / " + self.board_state[1][3][1] + " / " + self.board_state[1][3][2] + " / " +
              self.board_state[1][3][3] + "|/      |")
        print("|/___/___/___/___|       |")
        print("|       |________|_______|")
        print(
            "|       / " + self.board_state[2][0][0] + " / " + self.board_state[2][0][1] + " /|" + self.board_state[2][0][2] + " / " +
            self.board_state[2][0][3] + " /|")
        print("|      /___/___/_|_/___/ |")
        print("|     / " + self.board_state[2][1][0] + " / " + self.board_state[2][1][1] + " / " + self.board_state[2][1][2] + "|/ " +
              self.board_state[2][1][3] + " /  |")
        print("|    /___/___/___|___/   |")
        print("|   / " + self.board_state[2][2][0] + " / " + self.board_state[2][2][1] + " / " + self.board_state[2][2][2] + " /|" +
              self.board_state[2][2][3] + " /    |")
        print("|  /___/___/___/_|_/     |")
        print("| / " + self.board_state[2][3][0] + " / " + self.board_state[2][3][1] + " / " + self.board_state[2][3][2] + " / " +
              self.board_state[2][3][3] + "|/      |")
        print("|/___/___/___/___|       |")
        print("|       |________|_______|")
        print(
            "|       / " + self.board_state[3][0][0] + " / " + self.board_state[3][0][1] + " /|" + self.board_state[3][0][2] + " / " +
            self.board_state[3][0][3] + " / ")
        print("|      /___/___/_|_/___/  ")
        print("|     / " + self.board_state[3][1][0] + " / " + self.board_state[3][1][1] + " / " + self.board_state[3][1][2] + "|/ " +
              self.board_state[3][1][3] + " /   ")
        print("|    /___/___/___|___/    ")
        print("|   / " + self.board_state[3][2][0] + " / " + self.board_state[3][2][1] + " / " + self.board_state[3][2][2] + " /|" +
              self.board_state[3][2][3] + " /     ")
        print("|  /___/___/___/_|_/      ")
        print("| / " + self.board_state[3][3][0] + " / " + self.board_state[3][3][1] + " / " + self.board_state[3][3][2] + " / " +
              self.board_state[3][3][3] + "|/       ")
        print("|/___/___/___/___|        ")

    def draw_heuristics(self):
        print("         ________________")
        print("        / {} / {} / {} / {} /|".format(self.field_heuristics[0][0][0], self.field_heuristics[0][0][1],
                                                      self.field_heuristics[0][0][2],
                                                      self.field_heuristics[0][0][3]))
        print("       /___/___/___/___/ |")
        print("      / {} / {} / {} / {} /  |".format(self.field_heuristics[0][1][0], self.field_heuristics[0][1][1],
                                                      self.field_heuristics[0][1][2], self.field_heuristics[0][1][3]))
        print("     /___/___/___/___/   |")
        print("    / {} / {} / {} / {} /    |".format(self.field_heuristics[0][2][0], self.field_heuristics[0][2][1], self.field_heuristics[0][2][2], self.field_heuristics[0][2][3]))
        print("   /___/___/___/___/     |")
        print("  / {} / {} / {} / {} /      |".format(self.field_heuristics[0][3][0], self.field_heuristics[0][3][1], self.field_heuristics[0][3][2], self.field_heuristics[0][3][3]))
        print(" /___/___/___/___/       |")
        print("|       |________|_______|")
        print("|       / {} / {} /|{} / {} /|".format(self.field_heuristics[1][0][0], self.field_heuristics[1][0][1], self.field_heuristics[1][0][2], self.field_heuristics[1][0][3]))
        print("|      /___/___/_|_/___/ |")
        print(            "|     / {} / {} / {}|/ {} /  |".format(self.field_heuristics[1][1][0], self.field_heuristics[1][1][1], self.field_heuristics[1][1][2], self.field_heuristics[1][1][3]))
        print("|    /___/___/___|___/   |")


def make_random_move(board):
    empty_fields = board.get_empty_fields()
    return random.choice(empty_fields)


def make_best_move(board):
    return board.get_highest_empty_field()


def minimax(board, player, depth):
    new_board = copy.deepcopy(board)
    if new_board.is_win():
        return {'x': -math.inf, 'o': math.inf}[new_board.is_win()]
    if depth == 0:
        return new_board.get_highest_empty_field()

    if player == 'o':
        best = [-math.inf, []]
        for field in new_board.get_empty_fields():
            next_board = copy.deepcopy(new_board)
            next_board.make_move(player, field[0], field[1], field[2])
            value = minimax(next_board, 'x', depth-1)
            if value == math.inf:
                return [value, field]
            if value[0] > best[0]:
                best = [value[0], field]
    else:
        best = [math.inf, []]
        for field in new_board.get_empty_fields():
            next_board = copy.deepcopy(new_board)
            next_board.make_move(player, field[0], field[1], field[2])
            value = minimax(next_board, 'o', depth-1)
            if value == -math.inf:
                return [value, field]
            if not type(value) == type(list()):
                print(value, best)
            if value[0] < best[0]:
                best = [value[0], field]
    if best[0] == -math.inf:
        return next_board.get_highest_empty_field()
    elif best[0] == math.inf:
        return next_board.get_highest_empty_field()
    return best


def make_minimax_move(board, player):
    score, move = minimax(board, player, 2)
    return move


def change_player(player):
    if player == 'x':
        return 'o'
    return 'x'


def clear_screen():
    print(chr(27) + "[2J")


def redraw(board):
    clear_screen()
    board.draw_board()


player = 'x'
board = Board()
board.draw_board()

while not board.is_win():
    print(player + "'s move")
    print("Choose layer, row and column:")
    try:
        if player == 'o':
            print("Calculating move...")
            layer, row, column = make_minimax_move(copy.deepcopy(board), player)
            print(layer, row, column)
        else:
            # layer, row, column = make_minimax_move(copy.deepcopy(board), player)
            # print(layer, row, column)
            (layer, row, column) = [x - 1 for x in map(int, input().split(' '))]
    except ValueError:
        print("Provide integers only!")
        continue
    except KeyboardInterrupt:
        print("\n")
        exit(0)
    try:
        board.make_move(player, layer, row, column)
    except IndexError:
        print("The size of the board is 4x4x4!")
        continue
    except ValueError:
        print("This field is already taken!")
        continue

    redraw(board)
    board.draw_heuristics()
    player = change_player(player)

print("PLAYER " + board.is_win() + " WON")