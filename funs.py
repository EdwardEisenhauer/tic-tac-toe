def state_to_str(state: list) -> str:
    return ''.join(list(map(lambda x: x.to_char(), state)))


def state_to_actions(state: str) -> list:
    return [i for i, x in enumerate(state) if x == ' ']


def draw_board(board, heuristics=False):
    to_draw = list(map(lambda x: x.to_char(), board.state))
    if heuristics:
        header = "    " + "{:2}" * board.size
        print(header.format(*board.winning_conditions[0:board.size]))
        line = "{:2} {} " + "{:2}" * board.size + "|"
        for i in range(board.size):
            print(line.format(
                board.winning_conditions[board.size + i], '|', *to_draw[board.size * i:(i + 1) * board.size]
            ))
        footer = "{:4}{:" + str(2 * board.size + 2) + "}"
        print(footer.format(board.winning_conditions[2 * board.size + 1], board.winning_conditions[2 * board.size]))
    else:
        line = "| " + "{:2}" * board.size + "|"
        for i in range(board.size):
            print(line.format(*to_draw[board.size * i:(i + 1) * board.size]))
