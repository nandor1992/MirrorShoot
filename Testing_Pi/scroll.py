import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Example(QWidget):
    def __init__(self):
        super(Example, self).__init__()
        tab1_layout = QVBoxLayout(self)
        self.setLayout(tab1_layout)
        #self.setWidgetResizable(True)
        for i in range(0,20):
            l1 = QLabel("Drag scrollbar sliders to change color")
            l1.setFont(QFont("Arial", 16))
            tab1_layout.addWidget(l1)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('QSplitter demo')
        self.show()


def main():
    app = QApplication(sys.argv)
    tab1 = QScrollArea()
    ex=Example()
    tab1.setWidget(ex)
    tab1.setWidgetResizable(True)
    tab1.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()