import numpy as np

# Dimensiunile mediului
rows = 7
cols = 10

# Poziția de start și poziția obiectivului
start = (3, 0)
goal = (3, 7)

# Definirea puterii vântului în fiecare coloană
wind = [0, 0, 0, 1, 1, 1, 2, 2, 1, 0]

# Inițializarea tabelului Q cu valori aleatorii sau cu zero
Q = np.zeros((rows, cols, 4))  # 4 acțiuni posibile: sus, jos, stânga, dreapta

# Parametri pentru algoritmul Q-learning
alpha = 0.1  # rata de învățare
gamma = 0.9  # factorul de discount
epsilon = 0.1  # explorare vs. exploatare
num_episodes = 1000  # numărul de episoade de antrenament

# Funcție pentru a obține acțiunea în funcție de starea curentă și politica Q
def get_action(state):
    if np.random.uniform(0, 1) < epsilon:
        return np.random.randint(0, 4)  # explorare aleatoare
    else:
        return np.argmax(Q[state])

current_state = start

for episode in range(num_episodes):
    while current_state != goal:
        # Obține acțiunea în funcție de starea curentă
        action = get_action(current_state)
        
        # Aplică acțiunea și ține cont de vânt
        next_row, next_col = current_state
        if action == 0:  # sus
            next_row -= 1
        elif action == 1:  # jos
            next_row += 1
        elif action == 2:  # stânga
            next_col -= 1
        elif action == 3:  # dreapta
            next_col += 1
        
        # Adjustează poziția conform vântului
        next_row -= wind[current_state[1]]
        
        # Limitarea poziției în cadrul mediului
        next_row = max(0, min(next_row, rows - 1))
        next_col = max(0, min(next_col, cols - 1))
        
        # Calculează recompensa și actualizează Q
        reward = -1
        Q[current_state][action] += alpha * (reward + gamma * np.max(Q[(next_row, next_col)]) - Q[current_state][action])
        
        # Actualizează starea curentă
        current_state = (next_row, next_col)

policy = np.argmax(Q, axis=2)

print("Politica determinată de algoritm:")
print(policy)
