import sys

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QStackedWidget
from pyqt_base import App
app = QApplication(sys.argv)

window = QMainWindow()
stack = QStackedWidget(parent=window)
label1 = QLabel('label1')
label2 = App()
stack.addWidget(label1)
stack.addWidget(label2)
print('current', stack.currentIndex())
window.show()

def next():
      stack.setCurrentIndex(stack.currentIndex()+1)
      print('current', stack.currentIndex())

QTimer.singleShot(1000, next)

sys.exit(app.exec_())