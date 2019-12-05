from enums import Field
import copy
from math import sqrt


class Board:
    """
    TicTacToe game board representation.
    """
    def __init__(self, size=3, state=None):
        """
        :param size: Board size. Eg. 5 for 5x5 board.
        """
        self.size = size
        self.state = [Field.EMPTY] * size**2
        self.winning_conditions = [0] * (2 * self.size + 2)
        if state is not None:
            self.state = state
            self.size = int(sqrt(len(state)))
            self._calculate_winning_conditions()

    def __setitem__(self, index, token):
        """
        Set board field.

        Usage:
        b = Board(5)
        b[14] = Field.X

        :raises IndexError
        :param index: Field index
        :param token: one of enums.Field
        """
        row = int(index / self.size)
        column = index % self.size
        if self.state[index] is not Field.EMPTY:
            raise ValueError
        if row not in range(self.size) or column not in range(self.size):
            raise IndexError
        self.state[index] = token
        self._update_winning_conditions(token, index)

    def __getitem__(self, index):
        """
        :raises IndexError
        :param index: Field index
        :return: Field value
        """
        if index > self.size**2:
            raise IndexError("Out of index")

        return self.state[index]

    def _calculate_winning_conditions(self):
        for index, field in enumerate(self.state):
            row = int(index / self.size)
            column = index % self.size
            self.winning_conditions[column] += field.value
            self.winning_conditions[self.size + row] += field.value
            if row == column:
                self.winning_conditions[2 * self.size] += field.value
            if row + column == self.size - 1:
                self.winning_conditions[2 * self.size + 1] += field.value

    def _update_winning_conditions(self, token, index):
        row = int(index / self.size)
        column = index % self.size
        self.winning_conditions[column] += token.value
        self.winning_conditions[self.size + row] += token.value
        if row == column:
            self.winning_conditions[2 * self.size] += token.value
        if row + column == self.size - 1:
            self.winning_conditions[2 * self.size + 1] += token.value

    def get_winner(self):
        """
        Verifies if the current state is the terminating one and/or has a winner.
        :return: Field.EMPTY if there is a Tie.
        """
        if self.size in self.winning_conditions:
            return Field.X
        elif -self.size in self.winning_conditions:
            return Field.O
        elif not self.get_actions():
            return Field.EMPTY
        else:
            return None

    def get_state(self):
        return copy.copy(self.state)

    def get_actions(self):
        """ Returns list of indices where a move is possible. """
        return list(index for index, value in enumerate(self.state) if value == Field.EMPTY)

    def copy(self):
        """ Returns copy of board. """
        result = Board(size=self.size, state=self.state.copy())
        return result
