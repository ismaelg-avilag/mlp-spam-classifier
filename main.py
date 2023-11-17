import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices

from main_window import *

class Ui_MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.pushButtonGitHub.clicked.connect(self.open_github_repo)

    def open_github_repo(self):
        repo_url = "https://github.com/ismaelg-avilag/spam-classifier"
        QDesktopServices.openUrl(QUrl(repo_url))


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = Ui_MainWindow()
    window.show()
    app.exec_()