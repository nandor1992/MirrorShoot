import sys, os
from PyQt5.QtWidgets import QMainWindow, QApplication, QStackedWidget, QDesktopWidget
from PyQt5.QtCore import pyqtSignal, QObject, Qt, QTimer
from helloWidget import IdleApp
from takePhotoWidget import PictureApp
from menuWidget import MenuApp
from showWidget import showApp
from ListWidget import ListApp
from IndiWidget import IndiApp

class Communicate(QObject):
    resetTimeout = pyqtSignal()
    goToPicture = pyqtSignal()
    goToMain = pyqtSignal()
    goToReview = pyqtSignal(['QString'])
    goToList = pyqtSignal()
    goToIndividual = pyqtSignal(['QString'])
    timeout = pyqtSignal()
    exit = pyqtSignal()

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        #Basics
        self.title = 'Nandor Mirror'
        self.setWindowTitle(self.title)
        screen=QDesktopWidget().screenGeometry(1)
        if screen.right()>0 and screen.bottom()>0:
            self.move(screen.right(),screen.top())
        self.setStyleSheet("background-color:black;")
        self.stack = QStackedWidget(parent=self)
        self.c = Communicate()

        #Idle Widget
        self.c.goToPicture.connect(self.go_takePic)
        self.idle = IdleApp(self, self.c)
        self.idle.active=True

        #Photo  Widget
        self.c.exit.connect(self.close)
        self.c.timeout.connect(self.go_idleTimeout)
        self.photo = PictureApp(self,self.c)

        #Menu Widget
        self.c.goToMain.connect(self.go_menu)
        self.menu = MenuApp(self,self.c)

        #Show Widget
        self.c.goToReview.connect(self.go_review)
        self.rev = showApp(self,self.c)

        #List Widget
        self.c.goToList.connect(self.go_list)
        self.list = ListApp(self,self.c)

        #Indi
        self.c.goToIndividual.connect(self.go_ind)
        self.ind = IndiApp(self,self.c)


        #Extra adding etc...
        self.stack.addWidget(self.idle)
        self.stack.addWidget(self.menu)
        self.stack.addWidget(self.photo)
        self.stack.addWidget(self.rev)
        self.stack.addWidget(self.list)
        self.stack.addWidget(self.ind)
        self.setCentralWidget(self.stack)

        #Main Timeout
        self.main_timer = QTimer(self)
        self.Idle_timer = 30000
        self.main_timer.timeout.connect(self.timeout_timer)
        self.c.resetTimeout.connect(self.resetTimeout)
        self.main_timer.start(self.Idle_timer)
        self.showFullScreen()

    def timeout_timer(self):
        print("Timeout")
        self.c.timeout.emit()
        self.stack.setCurrentIndex(0)
        self.main_timer.start()

    def resetTimeout(self):
        self.main_timer.start()

    def go_idleTimeout(self):
        self.stack.setCurrentIndex(0)

    def go_menu(self):
        self.stack.setCurrentIndex(1)

    def go_takePic(self):
        self.stack.setCurrentIndex(2)

    def go_review(self):
        self.stack.setCurrentIndex(3)

    def go_list(self):
        self.stack.setCurrentIndex(4)

    def go_ind(self):
        self.stack.setCurrentIndex(5)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    if os.name == 'posix':
        app.setOverrideCursor(Qt.BlankCursor)
    ex = App()
    sys.exit(app.exec_())