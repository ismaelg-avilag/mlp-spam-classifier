import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import time
import os
import re

class WorkerThread(QThread):
    update_progress = pyqtSignal(int)
    finished_processing = pyqtSignal(list)

    def __init__(self, directory):
        super().__init__()
        self.directory = directory
    
    def run(self):
        files = os.listdir(self.directory)
        amountOfFiles = len(files)
        contenidos = []

        # Recorrer el directorio y sus subdirectorios
        for carpeta_actual, _, archivos_en_carpeta in os.walk(self.directory):
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
                        progreso = len(contenidos)*100/amountOfFiles
                        self.update_progress.emit(progreso)
                        

                    print(f"Leyendo archivo: {ruta_completa}")
                except UnicodeDecodeError as e:
                    print(f"Error al decodificar {ruta_completa}: {e}")

        self.finished_processing.emit(contenidos)