import numpy as np
from activation_functions import *


class NeuralNetwork:
    def __init__(self, layers_dim, hidden_activation=tanh, output_activation=logistic):
        self.L = len(layers_dim) - 1
        self.w = [None] * (self.L + 1)
        self.b = [None] * (self.L + 1)
        self.f = [None] * (self.L + 1)
        # initialization of weights and bias
        for l in range(1, self.L + 1):
            self.w[l] = -1 + 2 * np.random.rand(layers_dim[l], layers_dim[l-1])
            self.b[l] = -1 + 2 * np.random.rand(layers_dim[l], 1)
            
            if l == self.L:
                self.f[l] = output_activation
            else:
                self.f[l] = hidden_activation


    def predict(self, X):
        a = X
        for l in range(1, self.L + 1):
            z = self.w[l] @ a + self.b[l]
            a = self.f[l](z)
        return a

    def fit(self, X, Y, epochs=10000, lr=0.3, contour=None):
        p = X.shape[1]
        
        for _ in range(epochs):
            errors = Y - self.predict(X)
            enEjecucion = contour(np.mean(abs(errors)),_)
            if not enEjecucion:
                break
            # Initialize outputs of functions and gradients
            a = [None] * (self.L + 1)
            da = [None] * (self.L + 1)
            lg = [None] * (self.L + 1) #lg = local gradient
            
            # forward propagation
            a[0] = X
            for l in range(1, self.L + 1):
                z = self.w[l] @ a[l-1] + self.b[l]
                a[l], da[l] = self.f[l](z, derivative = True)
                
            # Back propagation
            for l in range(self.L, 0, -1):
                if l == self.L:
                    lg[l] = (Y - a[l]) * da[l]
                else:
                    lg[l] = (self.w[l+1].T @ lg[l+1]) * da[l]
            
            # weight adjustment
            for l in range(1, self.L + 1):
                self.w[l] += (lr/p) * (lg[l] @ a[l-1].T)
                self.b[l] += (lr/p) * np.sum(lg[l])
