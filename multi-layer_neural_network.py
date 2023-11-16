import tensorflow as tf

def logistic(z, derivative=False):
    a = 1 / (1 + tf.exp(-z))
    if derivative:
        da = tf.ones_like(z)
        return a, da
    return a


def tanh(z, derivative=False):
    a = tf.tanh(z)
    if derivative:
        da = 1 - tf.square(a)
        return a, da
    return a


class NeuralNetwork:
    def __init__(self, layers_dim, hidden_activation=tanh, output_activation=logistic):
        self.L = len(layers_dim) - 1
        self.w = [None] * (self.L + 1)
        self.b = [None] * (self.L + 1)
        self.f = [None] * (self.L + 1)
        # Inicializar pesos y bias
        for l in range(1, self.L + 1):
            shape = (layers_dim[l], layers_dim[l-1])
            rango_valores = (-1.0, 1.0)
            self.w[l] = tf.Variable(tf.random.uniform(shape, minval=rango_valores[0], maxval=rango_valores[1]))
            self.b[l] = tf.Variable(tf.zeros(shape=(layers_dim[l], 1)))

            if l == self.L:
                self.f[l] = output_activation
            else:
                self.f[l] = hidden_activation


    def predict(self, X):
        a = X
        for l in range(1, self.L + 1):
            z = tf.tensordot(self.w[l] , a, axes=1) + self.b[l]
            a = self.f[l](z)
        return a
    
    def calculate_loss(self, y_pred, y_true):
        epsilon = 1e-15
        loss = - (y_true * tf.math.log(y_pred + epsilon) + (1 - y_true) * tf.math.log(1 - y_pred + epsilon))
        return tf.reduce_mean(loss).numpy()

    def fit(self, X_train, Y_train, X_valid, Y_valid, epochs=40, lr=0.3):
      p = tf.shape(X_train)[1]
      p = tf.cast(p, dtype=tf.float32)

      for _ in range(epochs):
        if(_%100 == 0):
            print("Epoc: " + str(_) + " Loss: " + str(self.calculate_loss(self.predict(X_train), Y_train)) + 
                " - Val_loss: " + str(self.calculate_loss(self.predict(X_valid), Y_valid)))
        

        # print(np.mean(abs(errors)))
        a = [None] * (self.L + 1)
        da = [None] * (self.L + 1)
        lg = [None] * (self.L + 1) #lg = gradiente local

        # Propagacion adelante
        a[0] = X_train
        for l in range(1, self.L + 1):
            z = tf.tensordot(self.w[l] , a[l-1], axes=1) + self.b[l]
            a[l], da[l] = self.f[l](z, derivative = True)

        # Propagacion atras
        for l in range(self.L, 0, -1):
            if l == self.L:
                lg[l] = (Y_train - a[l]) * da[l]
            else:
                lg[l] = (tf.tensordot(tf.transpose(self.w[l+1]) , lg[l+1], axes=1)) * da[l]

        # ajuste de pesos
        for l in range(1, self.L + 1):
          self.w[l].assign_add((lr/p) * tf.tensordot(lg[l], tf.transpose(a[l-1]), axes=1))
          self.b[l].assign_add((lr/p) * tf.reduce_sum(lg[l], axis=1, keepdims=True))
