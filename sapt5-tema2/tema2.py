def identify_variables(board):
    variables = []
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                variables.append((i, j, 0)) #admit domeniu (1,9)
            elif board[i][j] == -1:
                variables.append((i, j, -1)) #admit numere pare
    return variables

def used_in_row(board, row, number):
    for i in range(9):
        if(board[row][i] == number):
            return True
    return False
 
def used_in_col(board, col, number):
    for i in range(9):
        if(board[i][col] == number):
            return True
    return False
 
def used_in_box(board, row, col, number):
    for i in range(3):
        for j in range(3):
            if(board[i + row][j + col] == number):
                return True
    return False
 
def can_use(board, row, col, number):
    return (not used_in_row(board, row, number) and 
            (not used_in_col(board, col, number) and 
            (not used_in_box(board, row - row % 3, col - col % 3, number))))
    
def identify_domain(board, variable):
    domain = []
    row = variable[0]
    col = variable[1]
    
    if variable[2] == -1:  # admite numere pare
        for x in range(2, 10, 2):
            if can_use(board, row, col, x):
                domain.append(x)
    else:
        for x in range(1, 10):
            if can_use(board, row, col, x):
                domain.append(x)

    return domain

def initialize(board):
    variables = identify_variables(board)
    domain_variables = []

    for var in variables:
        var_domain = identify_domain(board, var)
        domain_variables.append((var[0], var[1], var_domain))

    return domain_variables

def forward_checking(board):
    variables = identify_variables(board)
    
    if not variables:
        return True  

    row, col, dom = variables[0]
    var_domain = identify_domain(board, (row, col, dom))

    for number in var_domain:
        if can_use(board, row, col, number):
            board[row][col] = number

            if forward_checking(board):
                return True  

            board[row][col] = dom 

    return False  


def mrv(board):
    variables = identify_variables(board)

    if not variables:
        return True 

    variables.sort(key=lambda var: len(identify_domain(board, var)))

    row, col, dom = variables[0]
    var_domain = identify_domain(board, (row, col, dom))

    for number in var_domain:
        if can_use(board, row, col, number):
            board[row][col] = number

            if mrv(board):
                return True  

            board[row][col] = dom  

    return False  

def print_sudoku(board):
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - -")
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")
            if board[i][j] == 0:
                print(". ", end="")
            else:
                print(f"{board[i][j]} ", end="")
        print()


def main():
    
    print("input 1: ")
    
    _input = [[8, 4, 0, 0, 5, 0, -1, 0, 0],
            [3, 0, 0, 6, 0, 8, 0, 4, 0],
            [0, 0, -1, 4, 0, 9, 0, 0, -1],
            [0, 2, 3, 0, -1, 0, 9, 8, 0],
            [1, 0, 0, -1, 0, -1, 0, 0, 4],
            [0, 9, 8, 0, -1, 0, 1, 6, 0],
            [-1, 0, 0, 5, 0, 3, -1, 0, 0],
            [0, 3, 0, 1, 0, 6, 0, 0, 7],
            [0, 0, -1, 0, 2, 0, 0, 1, 3]]
    
    variables = initialize(_input)
    print(len(variables), "variabile:")
    for var in variables:
        print(f"Variabila ({var[0]}, {var[1]}) cu domeniu {var[2]}")
    
    if forward_checking(_input):
        print_sudoku(_input)
    else:
        print("Fara solutie")
        
    _input = [[-1, 0, 0, 6, -1, 2, 1, 5, 0],
        [-1, -1, 0, 0, 0, 0, 7, -1, 8],
        [8, 0, 3, 0, 0, 4, -1, -1, 9],
        [0, 9, 2, -1, 0, -1, -1, 0, 1],
        [3, -1, -1, 0, -1, 0, 0, -1, 0],
        [6, 1, 0, -1, 0, 9, -1, 0, -1],
        [0, 4, -1, 0, 7, -1, 0, 0, 2],
        [0, -1, 5, 0, -1, 0, 3, 8, -1],
        [0, 0, -1, 8, -1, 0, -1, 1, 0]]
    
    print("input 2: ")
    
    if mrv(_input):
        print_sudoku(_input)
    else:
        print("Fara solutie")
    
main()