import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices
import tensorflow as tf

from main_window import *
from about_window import *
from progress_bar import *
from evaluateEmails import *

tf.device('gpu')

class Ui_MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.pushButtonGitHub.clicked.connect(self.open_github_repo)
        self.pushButtonAboutProject.clicked.connect(self.open_about_project_window)
        self.pushButtonSelectFiles.clicked.connect(self.select_directory)

    def open_github_repo(self):
        repo_url = "https://github.com/ismaelg-avilag/mlp-spam-classifier"
        QDesktopServices.openUrl(QUrl(repo_url))
    
    def open_about_project_window(self):
        self.about_window = QtWidgets.QDialog()
        self.ui = Ui_AboutWindow()
        self.ui.setupUi(self.about_window)
        self.about_window.show()

    def select_directory(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Selecciona una carpeta")
        
        if directory:
            self.labelSelectedDirectory.setText("Carpeta seleccionada: " + directory)
            self.progressBar.setValue(0)
            self.progressBar.setVisible(True)
            self.worker_thread = WorkerThread(directory)
            self.worker_thread.update_progress.connect(self.update_progress_bar)
            self.worker_thread.finished_processing.connect(self.showResults)
            self.worker_thread.start()

    def update_progress_bar(self, progress):
        self.progressBar.setValue(progress)
    
    def showResults(self, data):
        self.amountOfSpam, self.amountOfHam = evaluate(data)
        self.labelAmountOfHam.setText("Los archivos procesados tienen " + str(self.amountOfHam) + " Ham")
        self.labelAmountOfSpam.setText("Los archivos procesados tienen " +  str(self.amountOfSpam) + " Spam")


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = Ui_MainWindow()
    window.show()
    app.exec_()