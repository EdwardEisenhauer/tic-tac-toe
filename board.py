from enums import Field


class Board:
    def __init__(self, size=3, state=None):
        self.size = size
        self.state = [Field.EMPTY] * int(pow(self.size, 2))
        self.actions = list(range(int(pow(self.size, 2))))
        self.winning_conditions = [0] * (2 * self.size + 2)
        if state is not None:
            self.state = state
            self._update_actions()
            self._calculate_winning_conditions()

    def _update_actions(self):
        self.actions = [i for i, x in enumerate(self.state) if x == Field.EMPTY]

    def _calculate_winning_conditions(self):
        for index, field in enumerate(self.state):
            row = int(index / self.size)
            column = index % self.size
            self.winning_conditions[row] += field.value
            self.winning_conditions[self.size + column] += field.value
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

    def move(self, token, index):
        row = int(index / self.size)
        column = index % self.size
        if self.state[index] is not Field.EMPTY:
            raise ValueError
        if row not in range(self.size) or column not in range(self.size):
            raise IndexError
        self.state[index] = token
        self._update_actions()
        self._update_winning_conditions(token, index)

    def draw(self, heuristics=False):
        to_draw = list(map(lambda x: x.to_char(), self.state))
        if heuristics:
            header = "    " + "{:2}" * self.size
            print(header.format(*self.winning_conditions[0:self.size]))
            line = "{:2} {} " + "{:2}" * self.size + "|"
            for i in range(self.size):
                print(line.format(
                    self.winning_conditions[self.size + i], '|', *to_draw[self.size * i:(i + 1) * self.size]
                ))
            footer = "{:4}{:" + str(2 * self.size + 2) + "}"
            print(footer.format(self.winning_conditions[2 * self.size + 1], self.winning_conditions[2 * self.size]))
        else:
            line = "| " + "{:2}" * self.size + "|"
            for i in range(self.size):
                print(line.format(*to_draw[self.size * i:(i + 1) * self.size]))

    def reset(self):
        self.state = [Field.EMPTY] * int(pow(self.size, 2))
        self.actions = list(range(int(pow(self.size, 2))))
        self.winning_conditions = [0] * (2 * self.size + 2)

    def get_winning_conditions(self):
        return self.winning_conditions

    def get_actions(self):
        return self.actions

    def get_size(self):
        return self.size

    def get_state(self):
        return self.state

    def get_winner(self):
        if self.size in self.winning_conditions:
            return Field.X
        elif -self.size in self.winning_conditions:
            return Field.O
        elif not self.actions:
            return Field.EMPTY
        else:
            return None
