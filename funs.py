def state_to_str(state: list) -> str:
    return ''.join(list(map(lambda x: x.to_char(), state)))


def state_to_actions(state: str) -> list:
    return [i for i, x in enumerate(state) if x == ' ']
