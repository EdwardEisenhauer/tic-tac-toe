#!/usr/local/bin/python3
from game import Game
from player import Player, Human, Heuristic, QAgent
from enums import Field
from funs import game_to_filename, visualize_stats

import argparse
from matplotlib import pyplot

"""
Arguments handling and configuration
"""


def assign_object_to_arg(arg: str, token: Field, params=None, filename=None) -> Player:
    return {'human': Human(token),
            'random': Player(token),
            'heuristic': Heuristic(token),
            'q': QAgent(token, *params, filename)}[arg]


parser_help = eval(open('help.py').read())        # Load help from the file

parser = argparse.ArgumentParser(
    description='Tic-Tac-Toe',
    epilog='Created by Edward Eisenhauer')

parser.add_argument('players', action='append', type=str, help=parser_help['player_x'], metavar='player_x')
parser.add_argument('players', action='append', type=str, help=parser_help['player_o'], metavar='player_o')
parser.add_argument('-n', '--games', type=int, required=True, help=parser_help['games'])
parser.add_argument('-b', '--board', type=int, default=3)
parser.add_argument('-d', '--draw', action='store_true', required=False, help=parser_help['draw'])
parser.add_argument('--live', action='store_true', default=False, required=False, help=parser_help['live'])
parser.add_argument('-o', '--output_file', nargs='?', const=' ', type=str, default='', help=parser_help['output_file'])
parser.add_argument('-p', '--percentage', action='store_true', default=False, help=parser_help['percentage'])
parser.add_argument('-a', '--alpha', type=float, action='append', default=None, help=parser_help['alpha'])
parser.add_argument('-g', '--gamma', type=float, action='append', default=None, help=parser_help['gamma'])
parser.add_argument('-e', '--epsilon', type=float, action='append', default=None, help=parser_help['epsilon'])
parser.add_argument('--version', action='version', version='%(prog)s 0.1')

args = parser.parse_args()

tokens = [Field.X, Field.O]
players = []
params = []
draw = args.draw
title = ''
q_agents = 0

for i, player in enumerate(args.players):
    """
    This shit needs to be handled
    """
    title = title + player
    if player == 'human':
        draw = True
    if player == 'q':
        q_agents = q_agents + 1
        if args.alpha is None or args.gamma is None or args.gamma is None:
            parser.error("QAgents requires alpha, gamma and epsilon values!")
        if len(args.alpha) == 1:
            params = [args.alpha[0], args.gamma[0], args.epsilon[0]]
        else:
            params = [args.alpha[i], args.gamma[i], args.epsilon[i]]
        title = title + str(params)
    players.append(assign_object_to_arg(args.players[i], tokens[i], params))
    if i == 0:
        title = title + ' vs. '

games_to_play = args.games


"""
Game configuration
"""

tic_tac_toe = Game(players, board_size=args.board, draw=draw)

pyplot.title(title)
x = []
y_x = []
y_o = []
y_tie = []
pyplot.ylim(bottom=0, top=1)
pyplot.plot(x, y_x, '-', color='r', label='X')
pyplot.plot(x, y_o, '-', color='g', label='O')
pyplot.plot(x, y_tie, '-', color='b', label='Tie')
pyplot.legend(loc='upper right')

for episode in range(1, games_to_play+1):
    """
    OMFG this needs rewriting too
    """
    tic_tac_toe.play()
    tic_tac_toe.reset()
    if not episode % int(games_to_play/100+1) or episode == 1:
        x.append(episode)
        y_x.append(tic_tac_toe.stats['X']/episode)
        y_o.append(tic_tac_toe.stats['O']/episode)
        y_tie.append(tic_tac_toe.stats['Tie']/episode)
        pyplot.plot(x, y_x, '-', color='r', label='X')
        pyplot.plot(x, y_o, '-', color='g', label='O')
        pyplot.plot(x, y_tie, '-', color='b', label='Tie')
        pyplot.pause(1e-6)
        if args.percentage:
            print(str(int(episode/games_to_play*100)) + "%")

if args.output_file is not None:
    if args.output_file == ' ':
        filename = game_to_filename(tic_tac_toe)
    else:
        filename = args.output_file
    pyplot.savefig(filename)

# filename = q_player.token.name + str(games_to_play) + '.pkl'
# q_player.q_table.save_to_file(filename)
# visualize_stats(tic_tac_toe)
print(tic_tac_toe.stats)
pyplot.show()
print()
