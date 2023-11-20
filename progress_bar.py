import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import time
import os

class WorkerThread(QThread):
    update_progress = pyqtSignal(int)
    finished_processing = pyqtSignal()

    def __init__(self, directory):
        super().__init__()
        self.directory = directory
    
    def run(self):
        files = os.listdir(self.directory)
        amountOfFiles = len(files)
        
        for i, file in enumerate(files):
            time.sleep(0.03)
            progress = int((i + 1) * 100 / amountOfFiles)
            self.update_progress.emit(progress)
        
        self.finished_processing.emit()