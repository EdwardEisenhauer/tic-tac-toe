from funs import state_to_actions, state_to_str

from math import sqrt
import pickle
import time


class QTable:
    def __init__(self):
        self.q_table = {}

    def __setitem__(self, state, action, value):
        """
        Set Q(state, action)
        :param state:
        :param action:
        :param value: new value of Q(s,a)
        :return:
        """
        self.q_table[state][action] = value

    def add_state(self, state, actions=None):
        if actions is None:
            actions = state_to_actions(state)
        self.q_table[state] = {action: 0 for action in actions}

    def get_max_q_move(self, state: str):
        max_q_move = max(self.q_table[state], key=lambda action: self.q_table[state][action])
        # print(max_q_move)
        return max_q_move

    def get_max_q_move_value(self, state: str):
        return max([i for i in self.q_table[state].values()])

    def save_to_file(self, filename=None):
        if filename is None:
            filename = str(time.asctime()) + '.pkl'
        file = open(filename, 'wb')
        pickle.dump(self.q_table, file)
        file.close()

    def read_from_file(self, filename='q_table.pkl'):
        file = open(filename, 'rb')
        self.q_table = pickle.load(file)
        file.close()

    def draw(self, state):
        if type(state) is not str:
            state = state_to_str(state)
        size = int(sqrt(len(state)))
        if state in self.q_table:
            to_draw = self.q_table[state].copy()
        else:
            self.add_state(state)
            to_draw = self.q_table[state].copy()
        for i in range(len(state)):
            if i not in to_draw:
                to_draw[i] = state[i]
        line = "   | " + "{:6}" * size + "|"
        list_to_draw = [''] * len(state)
        for key in to_draw:
            if type(to_draw[key]) is float:
                list_to_draw[int(key)] = str(round(to_draw[key], 3))
            else:
                list_to_draw[int(key)] = str(to_draw[key])
        for i in range(size):
            print(line.format(*list_to_draw[size * i:(i + 1) * size]))
        print()
