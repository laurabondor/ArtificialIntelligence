import numpy as np
from sklearn.metrics import (accuracy_score, precision_score, recall_score, f1_score, confusion_matrix)

def load_data(url):
    data = np.genfromtxt(url)
    x = data[:, :-1]  # atribute
    y = data[:, -1]   # etichete
    return x, y

def split_dataset(x, y, test_size=0.3, random_state=None):
    if random_state:
        np.random.seed(random_state)

    indices = np.arange(len(x))
    np.random.shuffle(indices)

    split_index = int(len(x) * (1 - test_size))
    train_indices, test_indices = indices[:split_index], indices[split_index:]

    x_train, x_test = x[train_indices], x[test_indices]
    y_train, y_test = y[train_indices], y[test_indices]

    return x_train, x_test, y_train, y_test

def initialize_weights(shape):
    weights = np.zeros(shape)
    while True:
        weights = np.random.uniform(-1, 1, shape)
        if not np.any(weights == 0):
            break
    return weights

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    return x * (1 - x)

def mean_square_error(y_true, y_pred):
    return np.mean((y_true - y_pred) ** 2)

def forward(x, weights_hidden, weights_output):
    hidden_layer = sigmoid(np.dot(x, weights_hidden))
    output_layer = sigmoid(np.dot(hidden_layer, weights_output))
    return hidden_layer, output_layer

def main():
    x, y = load_data("https://archive.ics.uci.edu/ml/machine-learning-databases/00236/seeds_dataset.txt")

    x_train, x_test, y_train, y_test = split_dataset(x, y, test_size=0.3, random_state=42)
    
    num_classes = len(np.unique(y_train))
    y_train = np.eye(num_classes)[y_train.astype(int) - 1]

    input_layer = 7
    hidden_layer = 56
    output_layer = 3
    learning_rate = 0.0001 
    max_epochs = 1000  
    
    weights_hidden = initialize_weights((input_layer, hidden_layer))
    weights_output = initialize_weights((hidden_layer, output_layer))
    

    for epoch in range(max_epochs):
        hidden_layer, output_layer = forward(x_train, weights_hidden, weights_output)  
        
        if epoch % 100 == 0:
            err = mean_square_error(y_train, output_layer)
            print(f"Epoca {epoch} : {err}")

        output_error = y_train - output_layer
        output_delta = output_error * output_layer * (1 - output_layer)

        hidden_error = output_delta.dot(weights_output.T)
        hidden_delta = hidden_error * hidden_layer * (1 - hidden_layer)

        weights_output += hidden_layer.T.dot(output_delta) * learning_rate
        weights_hidden += x_train.T.dot(hidden_delta) * learning_rate


    hidden_layer, output_layer = forward(x_test, weights_hidden, weights_output)  
    predictions = np.argmax(output_layer, axis=1).astype(int)
    conf_matrix = confusion_matrix(y_test, predictions)

    accuracy = np.mean(predictions == y_test) * 100
    precision = np.mean(precision_score(y_test, predictions, average=None, zero_division=1)) * 100
    recall = np.mean(recall_score(y_test, predictions, average=None, zero_division=1)) * 100
    f1 = np.mean(f1_score(y_test, predictions, average=None, zero_division=1)) * 100

    print(f"Accuracy: {accuracy}")
    print(f"Precision: {precision}")
    print(f"Recall: {recall}")
    print(f"F1 Score: {f1}")

main()
