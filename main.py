from game import Game
from player import Player, Human, Heuristic, QAgent
from enums import Mode, Field
from funs import visualize_stats

from matplotlib import pyplot
import sys

games_to_play = int(sys.argv[1])

human_player = Human(Field.X)
random_player = Player(Field.X)
heuristic_player = Heuristic(Field.X)
# q_player = QAgent(Field.O, alpha=0.5, gamma=0.9, epsilon=0.1, filename='q_table.pkl')
q_player = QAgent(Field.O, alpha=0.5, gamma=0.9, epsilon=0.1)

tic_tac_toe = Game((random_player, q_player),
                   board_size=3, draw=False)

x = []
y_x = []
y_o = []
y_tie = []
pyplot.plot(x, y_x, '-')
pyplot.plot(x, y_o, '-')
pyplot.plot(x, y_tie, '-')
pyplot.ylim(bottom=0, top=1)
pyplot.plot(x, y_x, '-', color='r', label='X')
pyplot.plot(x, y_o, '-', color='g', label='Y')
pyplot.plot(x, y_tie, '-', color='b', label='Tie')
pyplot.legend(loc='upper right')
pyplot.draw()
pyplot.pause(1)

for episode in range(1, games_to_play+1):
    tic_tac_toe.play()
    tic_tac_toe.reset()
    if not episode % 100 or episode is 1:
        x.append(episode)
        y_x.append(tic_tac_toe.stats['X']/episode)
        y_o.append(tic_tac_toe.stats['O']/episode)
        y_tie.append(tic_tac_toe.stats['Tie']/episode)
        pyplot.plot(x, y_x, '-', color='r', label='X')
        pyplot.plot(x, y_o, '-', color='g', label='O')
        pyplot.plot(x, y_tie, '-', color='b', label='Tie')
        pyplot.draw()
        pyplot.pause(0.1)
    # if not episode % 1000:
    #     print("Press any key to continue")
    #     input()

filename = q_player.token.name + str(games_to_play) + '.pkl'
q_player.q_table.save_to_file(filename)
# visualize_stats(tic_tac_toe)
print(tic_tac_toe.stats)

