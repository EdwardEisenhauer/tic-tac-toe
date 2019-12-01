from game import Game
from player import Player, Human, Heuristic, QAgent
from enums import Mode, Field

import sys

games_to_play = int(sys.argv[1])
human_player = Human(Field.X)
random_player = Player(Field.X)
heuristic_player = Heuristic(Field.X)
q_player = QAgent(Field.O, alpha=1.0, gamma=0.1, epsilon=0.1)
tic_tac_toe = Game((random_player, q_player),
                   board_size=3, draw=True)
for episode in range(games_to_play):
    tic_tac_toe.play()
    tic_tac_toe.reset()
tic_tac_toe.visualize_stats()
tic_tac_toe.print_stats()
