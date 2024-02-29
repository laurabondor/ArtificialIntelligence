
def initialize(input_array):
    return input_array + [-1]


def is_final(state) -> bool:
    length = len(state)

    for index in range(0, length - 2):
        if state[index] == 0:
            continue
        else:
            if state[index + 1] == 0 and index + 2 < length - 1:
                if state[index] >= state[index + 2]:
                    return False
            elif state[index + 1] != 0:
                if state[index] >= state[index + 1]:
                    return False
    return True

def transition_up(state, col0, row0):
    state[-1] = state[row0 * 3 + col0] = state[(row0 - 1) * 3 + col0]
    state[(row0 - 1) * 3 + col0] = 0

    # print("up", state)
    return state


def transition_down(state, col0, row0):
    state[-1] = state[row0 * 3 + col0] = state[(row0 + 1) * 3 + col0]
    state[(row0 + 1) * 3 + col0] = 0

    # print("down", state)
    return state


def transition_left(state, col0, row0):
    state[-1] = state[row0 * 3 + col0] = state[row0 * 3 + col0 - 1]
    state[row0 * 3 + col0 - 1] = 0

    # print("left", state)
    return state


def transition_right(state, col0, row0):
    state[-1] = state[row0 * 3 + col0] = state[row0 * 3 + col0 + 1]
    state[row0 * 3 + col0 + 1] = 0

    # print("right", state)
    return state


def validate_transition_up(state, col0, row0):
    if row0 - 1 >= 0 and state[-1] != state[(row0 - 1) * 3 + col0]:
        return True
    else:
        return False


def validate_transition_down(state, col0, row0):
    if row0 + 1 < 3 and state[-1] != state[(row0 + 1) * 3 + col0]:
        return True
    else:
        return False


def validate_transition_left(state, col0, row0):
    if col0 - 1 >= 0 and state[-1] != state[row0 * 3 + col0 - 1]:
        return True
    else:
        return False


def validate_transition_right(state, col0, row0):
    if col0 + 1 < 3 and state[-1] != state[row0 * 3 + col0 + 1]:
        return True
    else:
        return False


def dls(state, current_depth) -> bool:
    poz0 = state.index(0)
    col0 = poz0 % 3
    row0 = poz0 // 3

    if is_final(state):
        return True

    if current_depth <= 0:
        return False

    if validate_transition_up(state, col0, row0):
        next_transition = transition_up(state.copy(), col0, row0)
        if dls(next_transition, current_depth - 1):
            return True

    if validate_transition_down(state, col0, row0):
        next_transition = transition_down(state.copy(), col0, row0)
        if dls(next_transition, current_depth - 1):
            return True

    if validate_transition_left(state, col0, row0):
        next_transition = transition_left(state.copy(), col0, row0)
        if dls(next_transition, current_depth - 1):
            return True

    if validate_transition_right(state, col0, row0):
        next_transition = transition_right(state.copy(), col0, row0)
        if dls(next_transition, current_depth - 1):
            return True

    return False


def iddfs(state, max_depth) -> bool:
    for i in range(max_depth):
        if dls(state, i):
            print(i)
            return True
    return False


def main():
    _input = [8, 6, 7, 2, 5, 4, 0, 3, 1]
    print(iddfs(initialize(_input), 100))


main()



