from enum import Enum
from random import randrange

class Layer(Enum):
    TOP = 1
    TOP_MIDDLE = 2
    BOTTOM_MIDDLE = 3
    BOTTOM = 4

class BoardState:
    layers = {"top":     [[' ', ' ', ' ', ' '],
                          [' ', ' ', ' ', ' '],
                          [' ', ' ', ' ', ' '],
                          [' ', ' ', ' ', ' ']],
              "top_mid": [[' ', ' ', ' ', ' '],
                          [' ', ' ', ' ', ' '],
                          [' ', ' ', ' ', ' '],
                          [' ', ' ', ' ', ' ']],
              "bot_mid": [[' ', ' ', ' ', ' '],
                          [' ', ' ', ' ', ' '],
                          [' ', ' ', ' ', ' '],
                          [' ', ' ', ' ', ' ']],
              "bottom":  [[' ', ' ', ' ', ' '],
                          [' ', ' ', ' ', ' '],
                          [' ', ' ', ' ', ' '],
                          [' ', ' ', ' ', ' ']]}

    sums = {"top": {"rows": [0,0,0,0], "columns": [0,0,0,0], "diagonal": [0,0]},
            "top_mid": {"rows": [0,0,0,0], "columns": [0,0,0,0], "diagonal": [0,0]},
            "bot_mid": {"rows": [0,0,0,0], "columns": [0,0,0,0], "diagonal": [0,0]},
            "bottom": {"rows": [0,0,0,0], "columns": [0,0,0,0], "diagonal": [0,0]},
            "verticals": [[0,0,0,0],
                         [0,0,0,0],
                         [0,0,0,0],
                         [0,0,0,0]]}
    
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

    def isWin(self):
        if '-4' in str(self.sums):
            return 'o'
        elif '4' in str(self.sums):
            return 'x'
        else:
            return False

    def draw_board(self):
        print("         ________________")
        print("        / {} / {} / {} / {} /|".format(self.layers["top"][0][0], self.layers["top"][0][1], self.layers["top"][0][2], self.layers["top"][0][3]))
        print("       /___/___/___/___/ |")
        print("      / " + self.layers["top"][1][0] + " / " + self.layers["top"][1][1] + " / " + self.layers["top"][1][2] + " / " + self.layers["top"][1][3] + " /  |")
        print("     /___/___/___/___/   |")
        print("    / " + self.layers["top"][2][0] + " / " + self.layers["top"][2][1] + " / " + self.layers["top"][2][2] + " / " + self.layers["top"][2][3] + " /    |")
        print("   /___/___/___/___/     |")
        print("  / " + self.layers["top"][3][0] + " / " + self.layers["top"][3][1] + " / " + self.layers["top"][3][2] + " / " + self.layers["top"][3][3] + " /      |")
        print(" /___/___/___/___/       |")
        print("|       |________|_______|")
        print("|       / " + self.layers["top_mid"][0][0] + " / " + self.layers["top_mid"][0][1] + " /|" + self.layers["top_mid"][0][2] + " / " + self.layers["top_mid"][0][3] + " /|")
        print("|      /___/___/_|_/___/ |")
        print("|     / " + self.layers["top_mid"][1][0] + " / " + self.layers["top_mid"][1][1] + " / " + self.layers["top_mid"][1][2] + "|/ " + self.layers["top_mid"][1][3] + " /  |")
        print("|    /___/___/___|___/   |")
        print("|   / " + self.layers["top_mid"][2][0] + " / " + self.layers["top_mid"][2][1] + " / " + self.layers["top_mid"][2][2] + " /|" + self.layers["top_mid"][2][3] + " /    |")
        print("|  /___/___/___/_|_/     |")
        print("| / " + self.layers["top_mid"][3][0] + " / " + self.layers["top_mid"][3][1] + " / " + self.layers["top_mid"][3][2] + " / " + self.layers["top_mid"][3][3] + "|/      |")
        print("|/___/___/___/___|       |")
        print("|       |________|_______|")
        print("|       / " + self.layers["bot_mid"][0][0] + " / " + self.layers["bot_mid"][0][1] + " /|" + self.layers["bot_mid"][0][2] + " / " + self.layers["bot_mid"][0][3] + " /|")
        print("|      /___/___/_|_/___/ |")
        print("|     / " + self.layers["bot_mid"][1][0] + " / " + self.layers["bot_mid"][1][1] + " / " + self.layers["bot_mid"][1][2] + "|/ " + self.layers["bot_mid"][1][3] + " /  |")
        print("|    /___/___/___|___/   |")
        print("|   / " + self.layers["bot_mid"][2][0] + " / " + self.layers["bot_mid"][2][1] + " / " + self.layers["bot_mid"][2][2] + " /|" + self.layers["bot_mid"][2][3] + " /    |")
        print("|  /___/___/___/_|_/     |")
        print("| / " + self.layers["bot_mid"][3][0] + " / " + self.layers["bot_mid"][3][1] + " / " + self.layers["bot_mid"][3][2] + " / " + self.layers["bot_mid"][3][3] + "|/      |")
        print("|/___/___/___/___|       |")
        print("|       |________|_______|")
        print("|       / " + self.layers["bottom"][0][0] + " / " + self.layers["bottom"][0][1] + " /|" + self.layers["bottom"][0][2] + " / " + self.layers["bottom"][0][3] + " / ")
        print("|      /___/___/_|_/___/  ")
        print("|     / " + self.layers["bottom"][1][0] + " / " + self.layers["bottom"][1][1] + " / " + self.layers["bottom"][1][2] + "|/ " + self.layers["bottom"][1][3] + " /   ")
        print("|    /___/___/___|___/    ")
        print("|   / " + self.layers["bottom"][2][0] + " / " + self.layers["bottom"][2][1] + " / " + self.layers["bottom"][2][2] + " /|" + self.layers["bottom"][2][3] + " /     ")
        print("|  /___/___/___/_|_/      ")
        print("| / " + self.layers["bottom"][3][0] + " / " + self.layers["bottom"][3][1] + " / " + self.layers["bottom"][3][2] + " / " + self.layers["bottom"][3][3] + "|/       ")
        print("|/___/___/___/___|        ")

def make_random_move(board):
    return randrange(1,4), randrange(1,4), randrange(1,4)

def clear_screen():
    print(chr(27) + "[2J")

def redraw(board):
    clear_screen()
    board.draw_board()

def change_player(player):
    if player == 'x':
        return 'o'
    return 'x'

board = BoardState()
board.draw_board()
player = True

while(not board.isWin()):
    print({True: 'x', False: 'o'}[player] + "'s move")
    print("Choose layer, row and column:")
    try:
        if player == False:
            (layer, row, column) = make_random_move(board)
        else:
            (layer, row, column) = map(int, input().split(' '))
    except ValueError:
        print("Provide integers only!")
        continue
    except KeyboardInterrupt:
        print("\n")
        exit(0)
    try:
        board.make_move({True: 'x', False: 'o'}[player], {1: "top", 2: "top_mid", 3: "bot_mid", 4: "bottom"}[layer], row-1, column-1)
    except IndexError:
        print("The size of the board is 4x4x4!")
        continue
    except ValueError:
        print("This field is already taken!")
        continue
    redraw(board)
    player = not player

print("PLAYER " + board.isWin() + " WON")