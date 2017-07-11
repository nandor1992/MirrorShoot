import sys
from PyQt5.QtWidgets import (QWidget, QToolTip,
                             QPushButton, QApplication)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import pyqtSlot

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        btn = QPushButton('Button', self)
        btn.move(50, 50)
        btn.clicked.connect(self.conBut)
        btn.pressed.connect(self.conBut2)
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Tooltips')
        self.show()

    @pyqtSlot()
    def conBut(self):
        print("Button")

    @pyqtSlot()
    def conBut2(self):
        print("Button2")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())