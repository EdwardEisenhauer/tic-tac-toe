import random
from enum import Enum
from itertools import chain


class Layer(Enum):
    TOP = 1
    TOP_MIDDLE = 2
    BOTTOM_MIDDLE = 3
    BOTTOM = 4

    def __repr__(self):
        return self.name

    def from_index(idx):
        if idx == 1:
            return Layer.TOP
        elif idx == 2:
            return Layer.TOP_MIDDLE
        elif idx == 3:
            return Layer.BOTTOM_MIDDLE
        elif idx == 4:
            return Layer.BOTTOM


class Marking(Enum):
    X = 1
    O = 2
    EMPTY = 3

    def __str__(self):
        if self == Marking.EMPTY:
            return " "
        return self.name


class BoardState:
    layers = {
        Layer.TOP: [
            [Marking.EMPTY, Marking.EMPTY, Marking.EMPTY, Marking.EMPTY],
            [Marking.EMPTY, Marking.EMPTY, Marking.EMPTY, Marking.EMPTY],
            [Marking.EMPTY, Marking.EMPTY, Marking.EMPTY, Marking.EMPTY],
            [Marking.EMPTY, Marking.EMPTY, Marking.EMPTY, Marking.EMPTY]
        ],
        Layer.TOP_MIDDLE: [
            [Marking.EMPTY, Marking.EMPTY, Marking.EMPTY, Marking.EMPTY],
            [Marking.EMPTY, Marking.EMPTY, Marking.EMPTY, Marking.EMPTY],
            [Marking.EMPTY, Marking.EMPTY, Marking.EMPTY, Marking.EMPTY],
            [Marking.EMPTY, Marking.EMPTY, Marking.EMPTY, Marking.EMPTY]
        ],
        Layer.BOTTOM_MIDDLE: [
            [Marking.EMPTY, Marking.EMPTY, Marking.EMPTY, Marking.EMPTY],
            [Marking.EMPTY, Marking.EMPTY, Marking.EMPTY, Marking.EMPTY],
            [Marking.EMPTY, Marking.EMPTY, Marking.EMPTY, Marking.EMPTY],
            [Marking.EMPTY, Marking.EMPTY, Marking.EMPTY, Marking.EMPTY]
        ],
        Layer.BOTTOM: [
            [Marking.EMPTY, Marking.EMPTY, Marking.EMPTY, Marking.EMPTY],
            [Marking.EMPTY, Marking.EMPTY, Marking.EMPTY, Marking.EMPTY],
            [Marking.EMPTY, Marking.EMPTY, Marking.EMPTY, Marking.EMPTY],
            [Marking.EMPTY, Marking.EMPTY, Marking.EMPTY, Marking.EMPTY]
        ]}

    sums = {
        Layer.TOP: {
            "rows": [0, 0, 0, 0], "columns": [0, 0, 0, 0], "diagonal": [0, 0]},
        Layer.TOP_MIDDLE: {
            "rows": [0, 0, 0, 0], "columns": [0, 0, 0, 0], "diagonal": [0, 0]},
        Layer.BOTTOM_MIDDLE: {
            "rows": [0, 0, 0, 0], "columns": [0, 0, 0, 0], "diagonal": [0, 0]},
        Layer.BOTTOM: {
            "rows": [0, 0, 0, 0], "columns": [0, 0, 0, 0], "diagonal": [0, 0]}}

    def __init__(self):
        print("Board initiated!")

    def make_move(self, character, layer, row, column):
        if self.layers[layer][row][column] is not Marking.EMPTY:
            raise ValueError
        self.layers[layer][row][column] = character
        self._update_sums(character, layer, row, column)

    def _update_sums(self, character, layer, row, column):
        self.sums[layer]['rows'][row] += self._mark_to_v(character)
        self.sums[layer]['columns'][column] += self._mark_to_v(character)
        if row == column:
            self.sums[layer]['diagonal'][0] += self._mark_to_v(character)
        if (row + column) == 5:
            self.sums[layer]['diagonal'][1] += self._mark_to_v(character)

    def _mark_to_v(self, marking):
        return {Marking.X: 1, Marking.O: -1}[marking]

    def isWin(self):
        if "4" in str(self.sums):
            return Marking.X
        if "-4" in str(self.sums):
            return Marking.O
        else:
            return False

    def draw_board(self):
        board = """
         ________________
        / {} / {} / {} / {} /|
       /___/___/___/___/ |
      / {} / {} / {} / {} /  |
     /___/___/___/___/   |
    / {} / {} / {} / {} /    |
   /___/___/___/___/     |
  / {} / {} / {} / {} /      |
 /___/___/___/___/       |
|       |________|_______|
|       / {} / {} /|{} / {} /|
|      /___/___/_|_/___/ |
|     / {} / {} / {}|/ {} /  |
|    /___/___/___|___/   |
|   / {} / {} / {} /|{} /    |
|  /___/___/___/_|_/     |
| / {} / {} / {} / {}|/      |
|/___/___/___/___|       |
|       |________|_______|
|       / {} / {} /|{} / {} /|
|      /___/___/_|_/___/ |
|     / {} / {} / {}|/ {} /  |
|    /___/___/___|___/   |
|   / {} / {} / {} /|{} /    |
|  /___/___/___/_|_/     |
| / {} / {} / {} / {}|/      |
|/___/___/___/___|       |
|       |________|_______|
|       / {} / {} /|{} / {} / 
|      /___/___/_|_/___/  
|     / {} / {} / {}|/ {} /   
|    /___/___/___|___/    
|   / {} / {} / {} /|{} /     
|  /___/___/___/_|_/      
| / {} / {} / {} / {}|/       
|/___/___/___/___|        
"""
        data = []
        for rows in self.layers.values():
            for row in rows:
                for el in row:
                    data.append(el)
        print(board.format(*data))


def clear_screen():
    print(chr(27) + "[2J")


def get_symbol(player):
    return {True: Marking.X, False: Marking.O}[player]


def redraw(board):
    clear_screen()
    board.draw_board()


def change_player(player):
    if player == Marking.X:
        return Marking.O
    return Marking.X


board = BoardState()
board.draw_board()
player = Marking.X

while(not board.isWin()):
    print("Choose layer, row and column:")
    try:
        layer, row, column = map(int, input().split(' '))
    except ValueError:
        print("Provide integers only")
        continue
    except KeyboardInterrupt:
        print("\n")
        exit(0)
    try:
        board.make_move(player, Layer.from_index(layer), row-1, column-1)
    except ValueError:
        print("This field is already taken!")
        continue
    redraw(board)
    player = change_player(player)

print("PLAYER " + str(board.isWin()) + " WON")
