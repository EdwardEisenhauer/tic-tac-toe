from game import Game
from player import Player
from enums import Mode, Field

games_to_play = 3
tic_tac_toe = Game((Player(Field.X, mode=Mode.HUMAN), Player(Field.O, mode=Mode.Q, gamma=0.1, epsilon=0.3)), board_size=3, draw=True)
for episode in range(games_to_play):
    tic_tac_toe.play()
    tic_tac_toe.reset()
tic_tac_toe.visualize_stats()
