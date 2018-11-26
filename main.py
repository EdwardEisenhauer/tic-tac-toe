import random
import time


class BoardState:
    layers = [
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

    sums = {
        0: {
            "rows": [0, 0, 0, 0], "columns": [0, 0, 0, 0], "diagonal": [0, 0]},
        1: {
            "rows": [0, 0, 0, 0], "columns": [0, 0, 0, 0], "diagonal": [0, 0]},
        2: {
            "rows": [0, 0, 0, 0], "columns": [0, 0, 0, 0], "diagonal": [0, 0]},
        3: {
            "rows": [0, 0, 0, 0], "columns": [0, 0, 0, 0], "diagonal": [0, 0]},
        "verticals": [[0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0]]}

    def __init__(self):
        print("Board initiated!")

    def make_move(self, character, layer, row, column):
        if self.layers[layer][row][column] is not ' ':
            raise ValueError
        self.layers[layer][row][column] = character
        self._update_sums(character, layer, row, column)

    def _update_sums(self, character, layer, row, column):
        self.sums[layer]['rows'][row] += {'x': 1, 'o': -1}[character]
        self.sums[layer]['columns'][column] += {'x': 1, 'o': -1}[character]
        self.sums['verticals'][row][column] += {'x': 1, 'o': -1}[character]
        if row == column:
            self.sums[layer]['diagonal'][0] += {'x': 1, 'o': -1}[character]
        if (row + column) == 5:
            self.sums[layer]['diagonal'][1] += {'x': 1, 'o': -1}[character]

    def get_sums(self):
        # print(self.sums)
        return self.sums

    def get_empty_fields(self):
        empty_fields = []
        for layer_idx, layer in enumerate(self.layers):
            for row_idx, row in enumerate(layer):
                for field_idx, field in enumerate(row):
                    if field is ' ':
                        empty_fields.append([layer_idx, row_idx, field_idx])
        return empty_fields

    def isWin(self):
        if '-4' in str(self.sums):
            return 'o'
        elif '4' in str(self.sums):
            return 'x'
        else:
            return False

    def draw_board(self):
        print("         ________________")
        print("        / {} / {} / {} / {} /|".format(self.layers[0][0][0], self.layers[0][0][1], self.layers[0][0][2],
                                                      self.layers[0][0][3]))
        print("       /___/___/___/___/ |")
        print("      / " + self.layers[0][1][0] + " / " + self.layers[0][1][1] + " / " + self.layers[0][1][2] + " / " +
              self.layers[0][1][3] + " /  |")
        print("     /___/___/___/___/   |")
        print("    / " + self.layers[0][2][0] + " / " + self.layers[0][2][1] + " / " + self.layers[0][2][2] + " / " +
              self.layers[0][2][3] + " /    |")
        print("   /___/___/___/___/     |")
        print("  / " + self.layers[0][3][0] + " / " + self.layers[0][3][1] + " / " + self.layers[0][3][2] + " / " +
              self.layers[0][3][3] + " /      |")
        print(" /___/___/___/___/       |")
        print("|       |________|_______|")
        print(
            "|       / " + self.layers[1][0][0] + " / " + self.layers[1][0][1] + " /|" + self.layers[1][0][2] + " / " +
            self.layers[1][0][3] + " /|")
        print("|      /___/___/_|_/___/ |")
        print("|     / " + self.layers[1][1][0] + " / " + self.layers[1][1][1] + " / " + self.layers[1][1][2] + "|/ " +
              self.layers[1][1][3] + " /  |")
        print("|    /___/___/___|___/   |")
        print("|   / " + self.layers[1][2][0] + " / " + self.layers[1][2][1] + " / " + self.layers[1][2][2] + " /|" +
              self.layers[1][2][3] + " /    |")
        print("|  /___/___/___/_|_/     |")
        print("| / " + self.layers[1][3][0] + " / " + self.layers[1][3][1] + " / " + self.layers[1][3][2] + " / " +
              self.layers[1][3][3] + "|/      |")
        print("|/___/___/___/___|       |")
        print("|       |________|_______|")
        print(
            "|       / " + self.layers[2][0][0] + " / " + self.layers[2][0][1] + " /|" + self.layers[2][0][2] + " / " +
            self.layers[2][0][3] + " /|")
        print("|      /___/___/_|_/___/ |")
        print("|     / " + self.layers[2][1][0] + " / " + self.layers[2][1][1] + " / " + self.layers[2][1][2] + "|/ " +
              self.layers[2][1][3] + " /  |")
        print("|    /___/___/___|___/   |")
        print("|   / " + self.layers[2][2][0] + " / " + self.layers[2][2][1] + " / " + self.layers[2][2][2] + " /|" +
              self.layers[2][2][3] + " /    |")
        print("|  /___/___/___/_|_/     |")
        print("| / " + self.layers[2][3][0] + " / " + self.layers[2][3][1] + " / " + self.layers[2][3][2] + " / " +
              self.layers[2][3][3] + "|/      |")
        print("|/___/___/___/___|       |")
        print("|       |________|_______|")
        print(
            "|       / " + self.layers[3][0][0] + " / " + self.layers[3][0][1] + " /|" + self.layers[3][0][2] + " / " +
            self.layers[3][0][3] + " / ")
        print("|      /___/___/_|_/___/  ")
        print("|     / " + self.layers[3][1][0] + " / " + self.layers[3][1][1] + " / " + self.layers[3][1][2] + "|/ " +
              self.layers[3][1][3] + " /   ")
        print("|    /___/___/___|___/    ")
        print("|   / " + self.layers[3][2][0] + " / " + self.layers[3][2][1] + " / " + self.layers[3][2][2] + " /|" +
              self.layers[3][2][3] + " /     ")
        print("|  /___/___/___/_|_/      ")
        print("| / " + self.layers[3][3][0] + " / " + self.layers[3][3][1] + " / " + self.layers[3][3][2] + " / " +
              self.layers[3][3][3] + "|/       ")
        print("|/___/___/___/___|        ")


def make_random_move(board):
    empty_fields = board.get_empty_fields()
    return random.choice(empty_fields)


def make_notrandom_move(board):
    empty_fields = board.get_empty_fields()
    heuristic = board.get_sums()
    # for field in empty_fields:
    #     layer, row, column = field[0], field[1], field[2]
    #     if heuristic[layer]['rows'][row] + heuristic[layer]['columns'][column] + heuristic['verticals'][row][column] > 4:
    #         return [x+1 for x in field]
    for field in empty_fields:
        layer, row, column = field[0], field[1], field[2]
        if heuristic[layer]['rows'][row] > 2 or heuristic[layer]['columns'][column] > 2 or heuristic['verticals'][row][column] > 2:
            print("AI considers: " + str(field))
            print(heuristic['verticals'][row][column])
            print("DANGER!")
            return field
    return make_random_move(board)


def clear_screen():
    print(chr(27) + "[2J")


def redraw(board):
    # clear_screen()
    board.draw_board()


def change_player(player):
    if player == 'x':
        return 'o'
    return 'x'


board = BoardState()
board.draw_board()
player = 'x'

while not board.isWin():
    print(player + "'s move")
    print("Choose layer, row and column:")
    try:
        if player == 'o':
            (layer, row, column) = make_notrandom_move(board)
            print(layer, row, column)
        else:
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
    player = change_player(player)

print("PLAYER " + board.isWin() + " WON")
