from board import Board
from enums import Field, Mode
from funs import draw_board


class Game:
    def __init__(self, players, board_size=3, draw=False):
        """

        :param players:
        :param board_size:
        :param draw:
        """
        self.board_size = board_size
        self.draw: bool = draw
        self.board = Board(board_size)
        self.players = players
        self.current_player = players[0]
        self.winner = None
        self.stats = {'X': 0, 'O': 0, 'Tie': 0}

    def play(self):
        if self.draw:
            draw_board(self.board, heuristics=True)
        while self.winner is None:
            try:
                self.current_player.make_move(self.board)
            except ValueError:
                print("This field is already taken!")
                continue
            if self.draw:
                draw_board(self.board, heuristics=True)
            self.winner = self.board.get_winner()
            self._switch_players()
            # print("------------")
        for player in self.players:
            if player.mode is Mode.Q:
                player.update_q_table(player.reward(self.board))
                player.reset_history()
        self._update_stats()

    def reset(self):
        self.board = Board(self.board_size)
        self.current_player = self.players[0]
        self.winner = None

    def _update_stats(self):
        try:
            winner_in_str = {Field.X: 'X', Field.O: 'O', Field.EMPTY: 'Tie'}[self.winner]
            self.stats[winner_in_str] = self.stats[winner_in_str] + 1
        except KeyError:
            print("_update_stats() has been called with no winner!")
            exit()

    def _switch_players(self):
        self.current_player = {self.players[0]: self.players[1], self.players[1]: self.players[0]}[self.current_player]
