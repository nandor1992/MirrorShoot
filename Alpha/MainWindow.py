import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QStackedWidget
from PyQt5.QtCore import pyqtSignal, QObject
from Alpha.helloWidget import IdleApp
from Alpha.takePhotoWidget import PictureApp

class Communicate(QObject):
    takePicture = pyqtSignal()
    timeout = pyqtSignal()
    exit = pyqtSignal()

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        #Basics
        self.title = 'Nandor Mirror'
        self.setWindowTitle(self.title)
        self.setStyleSheet("background-color:black;")
        self.stack = QStackedWidget(parent=self)
        self.c = Communicate()

        #Idle Widget
        self.c.takePicture.connect(self.takePic)
        self.idle = IdleApp(self, self.c)

        #Photo  Widget
        self.c.exit.connect(self.close)
        self.c.timeout.connect(self.idleTimeout)
        self.photo = PictureApp(self,self.c)

        #Extra adding etc...
        self.stack.addWidget(self.idle)
        self.stack.addWidget(self.photo)
        self.setCentralWidget(self.stack)
        self.showFullScreen()

    def idleTimeout(self):
        self.stack.setCurrentIndex(0)

    def takePic(self):
        self.stack.setCurrentIndex(1)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())