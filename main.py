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
            "vertical": [[0,0,0,0],
                         [0,0,0,0],
                         [0,0,0,0],
                         [0,0,0,0]]}
    
    def __init__(self):
        print("Board initiated!")
        return

    def make_move(self, character, layer, row, column):
        if self.layers[layer][row][column] is not ' ':
            raise ValueError
            return
        self.layers[layer][row][column] = character

        self.sums[layer]['rows'][row] += {'x': 1, 'o': -1}[character]
        self.sums[layer]['columns'][column] += {'x': 1, 'o': -1}[character]
        self.sums['vertical'][row][column] += {'x': 1, 'o': -1}[character]
        if row == column:
            self.sums[layer]['diagonal'][0] += {'x': 1, 'o': -1}[character]
        if (row + column) == 5:
            self.sums[layer]['diagonal'][1] += {'x': 1, 'o': -1}[character]

        return

    def isWin(self):
        if '4' in str(self.sums):
            return 'x'
        if '-4' in str(self.sums):
            return 'o'
        else:
            return False

    def draw_board(self):
        print("         ________________")
        print("        / " + self.layers["top"][0][0] + " / " + self.layers["top"][0][1] + " / " + self.layers["top"][0][2] + " / " + self.layers["top"][0][3] + " /|")
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


board = BoardState()
board.draw_board()
player = True

while(True):
    winner = board.isWin()
    if winner:
        print("PLAYER " + winner + " WON")
        break
    try:
        print("Choose layer, row and column:")
        (layer, row, column) = map(int, input().split(' '))
        board.make_move({True: 'x', False: 'o'}[player], {1: "top", 2: "top_mid", 3: "bot_mid", 4: "bottom"}[layer], row-1, column-1)
        print(chr(27) + "[2J")
        board.draw_board()
        player = not player
    except ValueError:
        print("This field is already taken!")