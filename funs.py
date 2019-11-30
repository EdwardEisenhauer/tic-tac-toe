def state_to_str(state: list) -> str:
    return ''.join(list(map(lambda x: x.to_char(), state)))
