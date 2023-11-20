import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices

from main_window import *
from about_window import *
from evaluateEmails import *

class Ui_MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.pushButtonGitHub.clicked.connect(self.open_github_repo)
        self.pushButtonAboutProject.clicked.connect(self.open_about_project_window)
        self.pushButtonSelectFiles.clicked.connect(self.select_directory)

    def open_github_repo(self):
        repo_url = "https://github.com/ismaelg-avilag/spam-classifier"
        QDesktopServices.openUrl(QUrl(repo_url))
    
    def open_about_project_window(self):
        self.about_window = QtWidgets.QDialog()
        self.ui = Ui_AboutWindow()
        self.ui.setupUi(self.about_window)
        self.about_window.show()

    def select_directory(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Selecciona una carpeta")
        
        if directory:
            amountOfSpam, amountOfHam = evaluate(directory)
            self.labelAmountOfHam.setText("Los archivos procesados tienen un " + str(amountOfHam) + "% Ham")
            self.labelAmountOfSpam.setText("Los archivos procesados tienen un  " +  str(amountOfSpam) + "% Spam")


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = Ui_MainWindow()
    window.show()
    app.exec_()