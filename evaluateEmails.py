import tensorflow as tf
import os
import re
import joblib
import pickle
import numpy as np
from multi_layer_neural_network import *


def evaluate(data_vec):
    vectorizer = joblib.load('vectorizador_entrenado.joblib')
    X = vectorizer.transform(data_vec).toarray()
    data_vec = []
    X = X/100
    model = None
    with open('model.pkl', 'rb') as archivo:
        model = pickle.load(archivo)

    y_pred = tf.where(model.predict(tf.transpose(tf.convert_to_tensor(X, dtype=tf.float32))) <= 0.3, 0, 1)
    tensor_np = y_pred.numpy()[0]

    cant_spam = np.sum(tensor_np == 1)
    cant_ham = np.sum(tensor_np == 0)
    
    return cant_spam, cant_ham



