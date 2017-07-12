import sys, os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QMainWindow
from PyQt5.QtGui import QIcon, QMovie, QPixmap
from PyQt5.QtCore import pyqtSlot, QSize, QRect, Qt, QTimer
from tkinter import *
import time
import threading

if os.name == 'posix':
    import picamera
    import RPi.GPIO as GPIO

class PictureApp(QWidget):
    def __init__(self,parent,comm):
        super(QWidget,self).__init__(parent)
        self.title = 'Nandor Magic Mirror'
        self.lastTrigger = time.time()
        self.comm=comm
        self.comm.takePicture.connect(self.restart)
        self.initUI()

    def initUI(self):
        self.root = Tk()
        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        self.root.destroy()
        self.Gif_timer=7000
        self.Idle_timer=15000
        # Add image
        self.image = QLabel(self)
        pixmap = QPixmap("../Resource/Photo/test_image.jpg")
        pixmap.scaledToHeight(self.height)
        self.image.setPixmap(pixmap)
        self.image.hide()

        self.bstyle = "QPushButton{background: transparent;outline: none;border: none}"
        # Button    border-width: 5px;padding: 5px;border-style:solid;border-radius: 5px
        self.button = QPushButton(self)
        size = max(self.width, self.height) / 6
        diff = max(self.width, self.height) / 8
        self.button.move(self.width / 2 - size / 2 - diff, self.height / 2 - size / 2 + diff)
        self.Icon_photo_active=QIcon()
        self.Icon_photo_active.addPixmap(QPixmap('../Resource/Image/photo.png'),mode=QIcon.Disabled)
        self.Icon_photo_active.addPixmap(QPixmap('../Resource/Image/photo.png'), mode=QIcon.Active)
        self.button.setIcon(self.Icon_photo_active)
        self.button.setIconSize(QSize(size, size))
        self.button.setGeometry(
            QRect(self.width / 2 - size / 2 - diff, self.height / 2 - size / 2 + diff * 2, size + 20, size + 20))
        self.button.clicked.connect(self.photo_click)
        self.button.pressed.connect(self.photo_pressed)
        self.button.setStyleSheet(self.bstyle)

        # Button Exity
        self.button2 = QPushButton(self)
        size = max(self.width, self.height) / 6
        diff = max(self.width, self.height) / 8
        self.button2.move(self.width / 2 - size / 2 + diff, self.height / 2 - size / 2 + diff)
        self.button2.setIcon(QIcon('../Resource/Image/off.png'))
        self.button2.setIconSize(QSize(size, size))
        self.button2.setGeometry(
            QRect(self.width / 2 - size / 2 + diff, self.height / 2 - size / 2 + diff * 2, size + 20, size + 20))
        self.button2.clicked.connect(self.close_click)
        self.button2.pressed.connect(self.close_pressed)
        self.button2.setStyleSheet(self.bstyle)
        self.button2.setFlat(True)

        self.addLoading()
        self.main_timer = QTimer(self)
        self.main_timer.timeout.connect(self.timeout_timer)
        self.main_timer.start(self.Idle_timer)  # changed timer timeout to 1s
        # Show
        self.showFullScreen()

    def restart(self):
        self.image.hide()
        self.main_timer.start(self.Idle_timer)

    def timeout_timer(self):
        if  self.button.isEnabled():
            self.comm.timeout.emit()
            self.main_timer.stop()
        else:
            self.main_timer.start(self.Idle_timer)


    def addLoading(self):
        self.moviee = QLabel(self)
        self.movie = QMovie("../Resource/Gif/load.gif")
        self.movie2= QMovie("../Resource/Gif/countdown.gif")
        size = max(self.width, self.height) / 5
        diff = max(self.width, self.height) / 12
        self.movie.setScaledSize(QSize(size, size))
        self.movie2.setScaledSize(QSize(size, size))
        self.moviee.setMovie(self.movie)
        self.moviee.move(self.width / 2 - size / 2 + diff, self.height / 2 - size / 2 + diff)
        self.moviee.setGeometry(
            QRect(self.width / 2 - size / 2, self.height / 2 - size / 2 - diff, size + 20, size + 20))
        self.moviee.setAttribute(Qt.WA_TranslucentBackground)
        self.moviee.mouseReleaseEvent = self.gif_click
        #self.movie.timerEvent()
        # self.movie.start

    def takePicture(self):
        if os.name == 'posix':
            camera = picamera.PiCamera()
            camera.resolution = (2592, 1944)
            camera.rotation = 90
            camera.capture("../Resource/Photo/test_image.jpg")
            camera.close()
        else:
            time.sleep(2)
        self.movie.stop()
        self.moviee.hide()
        pixmap = QPixmap("../Resource/Photo/test_image.jpg")
        pixmap = pixmap.scaledToWidth(self.width)
        self.image.move(0, self.height / 2 - pixmap.height() / 2)
        self.image.setPixmap(pixmap)
        self.image.show()
        self.button.setEnabled(True)

    def countdown(self):
        self.movie2.stop()
        self.moviee.setMovie(self.movie)
        self.movie.jumpToFrame(0)
        t1=threading.Thread(target=self.takePicture,args=[])
        t1.start()
        self.movie.start()

    @pyqtSlot()
    def photo_click(self):
        self.button.setEnabled(False)
        self.main_timer.start()
        print("PyQt5 button1 click")
        self.button.setIcon(self.Icon_photo_active)
        self.image.hide()
        if not hasattr(self,'t2'):
            self.t2 = QTimer(self)
            self.t2.timeout.connect(self.countdown)
            self.t2.singleShot=True
        self.t2.start(self.Gif_timer)  # changed timer timeout to 1s
        self.moviee.setMovie(self.movie2)
        self.movie2.jumpToFrame(0)
        self.moviee.show()
        self.movie2.start()

    @pyqtSlot()
    def close_click(self):
        self.main_timer.stop()
        print('PyQt5 button2 click')
        self.comm.exit.emit()
        self.close()

    @pyqtSlot()
    def photo_pressed(self):
        print('PyQt5 button1 pressed')
        self.button.setIcon(QIcon('../Resource/Image/photo_down.png'))

    @pyqtSlot()
    def close_pressed(self):
        print('PyQt5 button2 pressed')
        self.button2.setIcon(QIcon('../Resource/Image/off_down.png'))

    def gif_click(self, event):
        print('PyQt5 Gif Click')


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Nandor Mirror'
        self.setWindowTitle(self.title)
        self.setStyleSheet("background-color:black;")
        self.table_widget = PictureApp(self)
        self.setCentralWidget(self.table_widget)
        self.showFullScreen()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())