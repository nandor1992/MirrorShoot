import sys, os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt5.QtGui import QIcon,QMovie,QPixmap
from PyQt5.QtCore import pyqtSlot, QSize, QRect,Qt
from tkinter import *
import time
from threading import Timer
if os.name == 'posix':
    import picamera

class MyCamera():
    def __init__(self):
        if os.name =='posix':
            self.camera=picamera.PiCamera()
            self.camera.resolution = (1920, 1080)
        else:
            self.camer=None

    def takeSnap(self,name):
        if os.name == 'posix':
            self.camera.capture("test_image.jpg")


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Nandor Magic Mirror'
        self.widget=self
        self.left = 10
        self.top = 10
        self.width = 320
        self.height = 200
        self.setAutoFillBackground(True)
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setStyleSheet("background-color:black;")
        root = Tk()
        self.cam=MyCamera()
        self.width = root.winfo_screenwidth()
        self.height = root.winfo_screenheight()
        print([self.width,self.height])
        size=self.width/10
        diff=self.width/12
        # Add image
        self.image = QLabel(self)
        pixmap = QPixmap("test_image.jpg")
        self.image.setPixmap(pixmap)
        self.image.hide()

        #Button
        self.button = QPushButton(self)
        self.button.setToolTip('This is an example button')
        self.button.move(self.width/2-size/2-diff, self.height/2-size/2+diff)
        self.button.setIcon(QIcon('photo.png'))
        self. button.setIconSize(QSize(size, size))
        self.button.setGeometry(QRect(self.width/2-size/2-diff, self.height/2-size/2+diff, size+20, size+20))
        self.button.clicked.connect(self.on_click)
        self.button.setFlat(True)
        self.button.setStyleSheet("QPushButton{background: transparent;}")
        #self.button.setProperty()
        #Button Exity
        self.button2 = QPushButton( self)
        size=self.width/10
        diff=self.width/12
        self.button2.setToolTip('This is an example button')
        self.button2.move(self.width/2-size/2+diff, self.height/2-size/2+diff)
        self.button2.setIcon(QIcon('off.png'))
        self.button2.setIconSize(QSize(size, size))
        self.button2.setGeometry(QRect(self.width/2-size/2+diff, self.height/2-size/2+diff, size+20, size+20))
        self.button2.clicked.connect(self.on_click2)
        self.button2.setFlat(True)
        self.button2.setStyleSheet("QPushButton{background: transparent;}")
        self.addLoading()


        #Show
        self.show()
        self.showFullScreen()

    def timeout(self):
        pixmap = QPixmap("test_image.jpg")
        self.image.setPixmap(pixmap)
        pixmap.scaledToHeight(self.height)
        self.movie.stop()
        self.moviee.hide()
        self.image.show()

    def addLoading(self):
        self.moviee = QLabel(self)
        self.movie = QMovie("load.gif")
        size = self.width / 5
        diff = self.width / 12
        self.movie.setScaledSize(QSize(size, size))
        self.moviee.setMovie(self.movie)
        self.moviee.move(self.width / 2 - size / 2 + diff, self.height / 2 - size / 2 + diff)
        self.moviee.setGeometry(
            QRect(self.width / 2 - size / 2, self.height / 2 - size / 2 - diff, size + 20, size + 20))
        self.moviee.setAttribute(Qt.WA_TranslucentBackground)
        self.moviee.mouseReleaseEvent=self.on_click3
        # self.movie.start



    @pyqtSlot()
    def on_click(self):
        print("Qlabel")
        #self.addLoading()
        self.t=Timer(2,self.timeout)
        self.t.start()
        self.cam.takeSnap("test_image.jpg")
        self.image.hide()
        self.moviee.show()
        self.movie.start()

    @pyqtSlot()
    def on_click2(self):
        print('PyQt5 button2 click')
        self.t.cancel()
        self.close()

    def on_click3(self,event):
        print('PyQt5 Gif Click')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())