from PyQt5 import uic
from PyQt5.QtWidgets import *

class TheBook(QMainWindow):
    def __init__(self):
        super(TheBook, self).__init__()
        uic.loadUi("TheBookUI.ui", self)
        self.show()

def run():
    app = QApplication([])
    window = TheBook()
    app.exec_()


if __name__ == '__main__':
    run()
