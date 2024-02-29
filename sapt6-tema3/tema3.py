def initialize_game():
    return [1, 2, 3, 4, 5, 6, 7, 8, 9], [], []

def is_game_over(player_a_numbers, player_b_numbers):
    if sum(player_a_numbers) == 15 and len(player_a_numbers)>=3:
        return "A castiga"
    elif sum(player_b_numbers) == 15 and len(player_b_numbers)>=3:
        return "B castiga"
    elif len(player_a_numbers) + len(player_b_numbers) == 9:
        return "Remiza"
    else:
        return None

def make_move(player_numbers, available_numbers, move):
    player_numbers.append(move)
    available_numbers.remove(move)

def is_valid_move(available_numbers, number):
    return number in available_numbers and 1 <= number <= 9

def heuristic(state):
    goal_sum = 15
    sum_a = sum(state[1])
    sum_b = sum(state[2])
    return abs(sum_a - goal_sum) - abs(sum_b - goal_sum)

def minmax(depth, state, player):
    if depth == 0 or is_game_over(state[1], state[2]):
        return heuristic(state)

    if player == 'A':
        max_eval = float('-inf')
        for move in state[0]:
            if is_valid_move(state[0], move):
                new_state = (state[0][:], state[1][:], state[2][:])
                make_move(new_state[1], new_state[0], move)
                eval = minmax(depth - 1, new_state, 'B')
                max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for move in state[0]:
            if is_valid_move(state[0], move):
                new_state = (state[0][:], state[1][:], state[2][:])
                make_move(new_state[2], new_state[0], move)
                eval = minmax(depth - 1, new_state, 'A')
                min_eval = min(min_eval, eval)
        return min_eval

def best_move(state):
    best_score = float('-inf')
    best_move = None

    for move in state[0]:
        if is_valid_move(state[0], move):
            new_state = (state[0][:], state[1][:], state[2][:])
            make_move(new_state[1], new_state[0], move)
            score = minmax(2, new_state, 'B') 
            if score > best_score:
                best_score = score
                best_move = move

    return best_move

def print_board(player_a_numbers, player_b_numbers):
    print(f"A: {player_a_numbers}")
    print(f"B: {player_b_numbers}")

def main():
    available_numbers, player_a_numbers, player_b_numbers = initialize_game()

    while True:
        print_board(player_a_numbers, player_b_numbers)

        move_a = int(input("Alege un numar: "))
        while not is_valid_move(available_numbers, move_a):
            print("Numar folosit. Alege altul: ")
            move_a = int(input("Alege un numar: "))
        make_move(player_a_numbers, available_numbers, move_a)

        game_result = is_game_over(player_a_numbers, player_b_numbers)
        if game_result:
            print_board(player_a_numbers, player_b_numbers)
            print(f"Rezultat: {game_result}")
            break

        move_b = best_move((available_numbers, player_a_numbers, player_b_numbers))
        make_move(player_b_numbers, available_numbers, move_b)

        game_result = is_game_over(player_a_numbers, player_b_numbers)
        if game_result:
            print_board(player_a_numbers, player_b_numbers)
            print(f"Rezultat: {game_result}")
            break

main()
