
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


def manhattan_distance(state):
    target = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    total_distance = 0
    for num in state:
        if num != 0:
            current_row, current_col = state.index(num) // 3, state.index(num) % 3
            target_row, target_col = target.index(num) // 3, target.index(num) % 3
            total_distance += abs(current_row - target_row) + abs(current_col - target_col)
    return total_distance

def hamming_distance(state):
    target = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    return sum(1 for i in range(len(state)) if state[i] != target[i])

def custom_heuristic(state):
    # returneaaza suma elementelor în poziții greșite
    target = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    return sum(1 for i in range(len(state)) if state[i] != target[i])

def greedy_search(state, heuristic):
    if is_final(state):
        return True

    open_list = [(state, heuristic(state))]
    closed_set = set()

    while open_list:
        open_list.sort(key=lambda x: x[1])
        current_state, _ = open_list.pop(0)
        
        current_state_tuple = tuple(current_state)
        
        if current_state_tuple in closed_set:
            continue

        closed_set.add(current_state_tuple)

        poz0 = current_state.index(0)
        col0 = poz0 % 3
        row0 = poz0 // 3

        next_states = []

        if validate_transition_up(current_state, col0, row0):
            next_states.append(transition_up(current_state.copy(), col0, row0))

        if validate_transition_down(current_state, col0, row0):
            next_states.append(transition_down(current_state.copy(), col0, row0))

        if validate_transition_left(current_state, col0, row0):
            next_states.append(transition_left(current_state.copy(), col0, row0))

        if validate_transition_right(current_state, col0, row0):
            next_states.append(transition_right(current_state.copy(), col0, row0))

        for next_state in next_states:
            if is_final(next_state):
                return True

            next_state_tuple = tuple(next_state) 
            if next_state_tuple not in closed_set:
                open_list.append((next_state, heuristic(next_state)))

    return False


import time

def print_results(strategy, heuristic, result, moves, duration):
    if result:
        print(f"Strategy: {strategy}, Heuristic: {heuristic}")
        print("Solution found.")
        print(f"Number of Moves: {moves}")
        print(f"Duration: {duration} seconds")
    else:
        print(f"Strategy: {strategy}, Heuristic: {heuristic}")
        print("No solution found.")

def main():
    _input = [2, 7, 5, 0, 8, 4, 3, 1, 6]

    strategies = ["IDDFS", "Greedy"]
    heuristics = [manhattan_distance, hamming_distance, custom_heuristic]

    start_time = time.time()
    max_depth = 50 
    iddfs_result = iddfs(_input, max_depth)
    iddfs_duration = time.time() - start_time

    moves_iddfs = -1
    if iddfs_result:
        moves_iddfs = max_depth

    print_results("IDDFS", "None", iddfs_result, moves_iddfs, iddfs_duration)
    print()

    for heuristic in heuristics:
        start_time = time.time()
        greedy_result = greedy_search(_input, heuristic)
        greedy_duration = time.time() - start_time

        moves_greedy = -1
        if greedy_result:
            moves_greedy = heuristic(_input)

        print_results("Greedy", heuristic.__name__, greedy_result, moves_greedy, greedy_duration)
        print()

if __name__ == "__main__":
    main()



