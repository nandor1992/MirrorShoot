import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QStackedWidget
from PyQt5.QtCore import pyqtSignal, QObject
if sys.version_info >(2,5):
    from Alpha.helloWidget import IdleApp
    from Alpha.takePhotoWidget import PictureApp
    from Alpha.menuWidget import MenuApp
    from Alpha.showWidget import showApp
    from Alpha.ListWidget import ListApp
    from Alpha.IndiWidget import IndiApp
else:
    from helloWidget import IdleApp
    from takePhotoWidget import PictureApp
    from menuWidget import MenuApp
    from showWidget import showApp
    from ListWidget import ListApp
    from IndiWidget import IndiApp

class Communicate(QObject):
    goToPicture = pyqtSignal()
    goToMain = pyqtSignal()
    goToReview = pyqtSignal()
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
        self.showFullScreen()


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
    ex = App()
    sys.exit(app.exec_())