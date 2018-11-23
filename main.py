from enum import Enum
from random import randrange

class Layer(Enum):
     TOP = 0
     TOP_MIDDLE = 1
     BOTTOM_MIDDLE = 2
     BOTTOM = 3

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

    def get_sums(self):
        return self.sums

    def get_empty_fields(self):
        fields = []
        for layer in self.layers:
            for row in layer:
                for field in row:
                    if field is ' ':
                        fields.append([self.layers.index(layer),layer.index(row),row.index(field)])
        return fields

    def isWin(self):
        if '-4' in str(self.sums):
            return 'o'
        elif '4' in str(self.sums):
            return 'x'
        else:
            return False

    def draw_board(self):
        print("         ________________")
        print("        / {} / {} / {} / {} /|".format(self.layers[0][0][0], self.layers[0][0][1], self.layers[0][0][2], self.layers[0][0][3]))
        print("       /___/___/___/___/ |")
        print("      / " + self.layers[0][1][0] + " / " + self.layers[0][1][1] + " / " + self.layers[0][1][2] + " / " + self.layers[0][1][3] + " /  |")
        print("     /___/___/___/___/   |")
        print("    / " + self.layers[0][2][0] + " / " + self.layers[0][2][1] + " / " + self.layers[0][2][2] + " / " + self.layers[0][2][3] + " /    |")
        print("   /___/___/___/___/     |")
        print("  / " + self.layers[0][3][0] + " / " + self.layers[0][3][1] + " / " + self.layers[0][3][2] + " / " + self.layers[0][3][3] + " /      |")
        print(" /___/___/___/___/       |")
        print("|       |________|_______|")
        print("|       / " + self.layers[1][0][0] + " / " + self.layers[1][0][1] + " /|" + self.layers[1][0][2] + " / " + self.layers[1][0][3] + " /|")
        print("|      /___/___/_|_/___/ |")
        print("|     / " + self.layers[1][1][0] + " / " + self.layers[1][1][1] + " / " + self.layers[1][1][2] + "|/ " + self.layers[1][1][3] + " /  |")
        print("|    /___/___/___|___/   |")
        print("|   / " + self.layers[1][2][0] + " / " + self.layers[1][2][1] + " / " + self.layers[1][2][2] + " /|" + self.layers[1][2][3] + " /    |")
        print("|  /___/___/___/_|_/     |")
        print("| / " + self.layers[1][3][0] + " / " + self.layers[1][3][1] + " / " + self.layers[1][3][2] + " / " + self.layers[1][3][3] + "|/      |")
        print("|/___/___/___/___|       |")
        print("|       |________|_______|")
        print("|       / " + self.layers[2][0][0] + " / " + self.layers[2][0][1] + " /|" + self.layers[2][0][2] + " / " + self.layers[2][0][3] + " /|")
        print("|      /___/___/_|_/___/ |")
        print("|     / " + self.layers[2][1][0] + " / " + self.layers[2][1][1] + " / " + self.layers[2][1][2] + "|/ " + self.layers[2][1][3] + " /  |")
        print("|    /___/___/___|___/   |")
        print("|   / " + self.layers[2][2][0] + " / " + self.layers[2][2][1] + " / " + self.layers[2][2][2] + " /|" + self.layers[2][2][3] + " /    |")
        print("|  /___/___/___/_|_/     |")
        print("| / " + self.layers[2][3][0] + " / " + self.layers[2][3][1] + " / " + self.layers[2][3][2] + " / " + self.layers[2][3][3] + "|/      |")
        print("|/___/___/___/___|       |")
        print("|       |________|_______|")
        print("|       / " + self.layers[3][0][0] + " / " + self.layers[3][0][1] + " /|" + self.layers[3][0][2] + " / " + self.layers[3][0][3] + " / ")
        print("|      /___/___/_|_/___/  ")
        print("|     / " + self.layers[3][1][0] + " / " + self.layers[3][1][1] + " / " + self.layers[3][1][2] + "|/ " + self.layers[3][1][3] + " /   ")
        print("|    /___/___/___|___/    ")
        print("|   / " + self.layers[3][2][0] + " / " + self.layers[3][2][1] + " / " + self.layers[3][2][2] + " /|" + self.layers[3][2][3] + " /     ")
        print("|  /___/___/___/_|_/      ")
        print("| / " + self.layers[3][3][0] + " / " + self.layers[3][3][1] + " / " + self.layers[3][3][2] + " / " + self.layers[3][3][3] + "|/       ")
        print("|/___/___/___/___|        ")

def make_random_move(board):
    return randrange(1,5), randrange(1,5), randrange(1,5)

def minimax(new_board, player):
    
    avail_spots = get_empty_fields(new_board)

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
    board.get_empty_fields()
    print("Choose layer, row and column:")
    try:
        if player == False:
            (layer, row, column) = make_random_move(board)
            print((layer, row, column))
        else:
            (layer, row, column) = map(int, input().split(' '))
    except ValueError:
        print("Provide integers only!")
        continue
    except KeyboardInterrupt:
        print("\n")
        exit(0)
    try:
        board.make_move({True: 'x', False: 'o'}[player], layer-1, row-1, column-1)
    except IndexError:
        print("The size of the board is 4x4x4!")
        continue
    except ValueError:
        print("This field is already taken!")
        continue
    redraw(board)
    player = not player

print("PLAYER " + board.isWin() + " WON")