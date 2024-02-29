import copy
import pandas as pd
import numpy as np
import math

class DataLoader:
    def __init__(self, path):
        self.dataframe = pd.read_csv(path, delimiter='\t')


    def split_and_format(self, train_procent):
        train_size = int(self.dataframe.shape[0] * train_procent)

        data = self.dataframe.to_numpy()
        
        permutation = np.random.permutation(data.shape[0])
        data = data[permutation]
    
        train_x = data[:train_size, :-1]
        train_y = data[:train_size, -1]

        test_x = data[train_size:, :-1]
        test_y = data[train_size:, -1]

        train_y_enocoded = np.zeros((train_y.shape[0], 3))
        test_y_enocoded = np.zeros((test_y.shape[0], 3))

        for i in range(train_y.shape[0]):
            train_y_enocoded[i][int(train_y[i]) - 1] = 1

        for i in range(test_y.shape[0]):
            test_y_enocoded[i][int(test_y[i]) - 1] = 1

        
        return (train_x, train_y_enocoded), (test_x, test_y_enocoded)
    
    


class NeuralNetwork:
    def __init__(self, X, Y, alpha = 0.1, epochs = 10) -> None:
        self.X = copy.deepcopy(X)
        self.Y = copy.deepcopy(Y)
        self.alpha = alpha
        self.epochs = epochs

        self.W1 = np.random.rand(7, 21) - 0.5
        self.W2 = np.random.rand(21, 3) - 0.5


    def relu(self, x):
        return np.maximum(0, x)
        
    def relu_derivative(self, x):
        return np.where(x >= 0, 1, 0)

    
    def sigmoid(self, x):
        formula = lambda elem: 1/(1 + math.exp(-elem))
        
        vfunc = np.vectorize(formula)
        return vfunc(x)

    def sigmoid_derivative(self, x):
        formula = lambda elem: (1/(1 + math.exp(-elem))) * (1 - 1/(1 + math.exp(-elem)))
        
        vfunc = np.vectorize(formula)
        return vfunc(x)

    def forward(self, x):
        w1 = np.dot(x, self.W1) 
        a1 = self.relu(w1)
        w2 = np.dot(a1, self.W2)
        a2 = self.sigmoid(w2)
        return (w1, a1, w2, a2)

    def train_run(self):
        for _ in range(self.epochs):
            w1, a1, w2, a2 = self.forward(self.X)

            d_loss_a2 = (a2 - self.Y) / self.Y.shape[0] # shape = (146, 3)

            d_a2_w2 = self.sigmoid_derivative(w2) # shape = (146, 3)
            d_loss_w2 = d_loss_a2 * d_a2_w2 # shape = (146, 3)
            dw2 = np.dot(a1.T, d_loss_w2) # shape = (21, 3)

            d_loss_a1 = np.dot(d_loss_w2, self.W2.T) # shape = (146, 21)
            d_a1_w1 = self.relu_derivative(w1) # shape = (146, 21)
            d_loss_w1 = d_loss_a1 * d_a1_w1 # shape = (146, 21)
            dw1 = np.dot(self.X.T, d_loss_w1) # shape = (7, 21)

            self.W1 -= self.alpha * dw1
            self.W2 -= self.alpha * dw2
                
                
    def loss(self, y, y_hat):
        return 1/2 * np.sum((y - y_hat)**2)
 
    def test_run(self, x, y):
        _, _, _, y_hat = self.forward(x)

        predicted_classes = np.argmax(y_hat, axis=1)
        correct_classes = np.argmax(y, axis=1)

        accuracy = np.mean(predicted_classes == correct_classes)
    
        tp = 0
        fn = 0
        fp = 0

        for i in range(predicted_classes.shape[0]):
            if predicted_classes[i] == 1 and correct_classes[i] == 1:
                tp += 1
            elif predicted_classes[i] == 0 and correct_classes[i] == 1:
                fn += 1
            elif predicted_classes[i] == 1 and correct_classes[i] == 0:
                fp += 1

        recall = tp / (tp + fn)
        precision = tp / (tp + fp)
        f_score = 2 * (precision * recall) / (precision + recall)

        print("Accuracy: ", accuracy)
        print("Recall: ", recall)
        print("Precision: ", precision)
        print("F-score: ", f_score)
        print()


if __name__ == '__main__':
    loader = DataLoader('seeds_dataset.txt')
    (train_x, train_y), (test_x, test_y) = loader.split_and_format(0.7)

    nn = NeuralNetwork(train_x, train_y, epochs=10000)

    nn.train_run()

    nn.test_run(train_x, train_y)

    nn.test_run(test_x, test_y)