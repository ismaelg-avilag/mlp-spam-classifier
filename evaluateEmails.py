import tensorflow as tf
import os
import re
import joblib
import pickle
import numpy as np
from multi_layer_neural_network import *



def obtener_contenido_archivos_en_subdirectorios(directorio):
    contenidos = []

    # Recorrer el directorio y sus subdirectorios
    for carpeta_actual, _, archivos_en_carpeta in os.walk(directorio):
        for nombre_archivo in archivos_en_carpeta:
            ruta_completa = os.path.join(carpeta_actual, nombre_archivo)

            try:
                with open(ruta_completa, 'r', encoding='utf-8', errors='ignore') as archivo:
                    contenido = archivo.read()
                    contenido = contenido.replace('\n', ' ')
                    patron_url = re.compile(r'https://([A-Za-z0-9.-]+)(?:/[^\s]*)?')
                    patron_ips = re.compile( r'\b(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b')
                    patron_correo = re.compile(r'\b[A-Za-z0-9._%+-]+@([A-Za-z0-9.-]+)\.[A-Z|a-z]{2,}\b')
                    contenido = patron_ips.sub('ipAddress', contenido)
                    contenido = patron_correo.sub(lambda match: f" emailAddress {match.group(1).split('.')[0]} ", contenido)
                    contenido = patron_url.sub(lambda match: f" webURL {match.group(1).split('.')[0]}", contenido)


                    contenidos.append(contenido)

                print(f"Leyendo archivo: {ruta_completa}")
            except UnicodeDecodeError as e:
                print(f"Error al decodificar {ruta_completa}: {e}")

    return contenidos


def evaluate(nombre_carpeta):
    data_vec = obtener_contenido_archivos_en_subdirectorios(nombre_carpeta)
    vectorizer = joblib.load('vectorizador_entrenado.joblib')
    matriz_spam = vectorizer.transform(data_vec).toarray()
    model = None
    with open('model.pkl', 'rb') as archivo:
        model = pickle.load(archivo)

    y_pred = tf.where(model.predict(tf.transpose(tf.convert_to_tensor(matriz_spam, dtype=tf.float32))) <= 0.3, 0, 1)
    tensor_np = y_pred.numpy()[0]

    cant_spam = np.sum(tensor_np == 1)
    cant_ham = np.sum(tensor_np == 0)
    
    return cant_spam, cant_ham



