import sys

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QStackedWidget, QWidget
from Testing_Pi.pyqt_base import PictureApp

app = QApplication(sys.argv)
ex = PictureApp()
window = QMainWindow()
window.setWindowTitle("Title")
left = 10
top = 10
width = 320
height = 200
window.setGeometry(left, top, width,height)
window.setStyleSheet("background-color:black;")
stack = QStackedWidget(parent=window)
label1 = QLabel('label1')
stack.addWidget(ex)
stack.addWidget(label1)
print('current', stack.currentIndex())
window.showFullScreen()

def next():
      stack.setCurrentIndex(stack.currentIndex()+1)
      print('current', stack.currentIndex())

QTimer.singleShot(1000, next)

sys.exit(app.exec_())