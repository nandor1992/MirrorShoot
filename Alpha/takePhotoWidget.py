import sys, os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QMainWindow
from PyQt5.QtGui import QIcon, QMovie, QPixmap
from PyQt5.QtCore import pyqtSlot, QSize, QRect, Qt, QTimer
from tkinter import *
import time
import threading
import datetime
from PIL import Image

if os.name == 'posix':
    import picamera
    import RPi.GPIO as GPIO
elif os.name =='nt':
    import cv2

class PictureApp(QWidget):
    def __init__(self,parent,comm):
        super(QWidget,self).__init__(parent)
        self.title = 'Nandor Magic Mirror'
        self.lastTrigger = time.time()
        self.comm=comm
        self.comm.goToPicture.connect(self.begin)
        self.active=False
        self.initUI()

    def initUI(self):
        self.root = Tk()
        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        self.root.destroy()
        self.Gif_timer=7000
        self.Idle_timer=30000
        # Add image
        self.image = QLabel(self)
        pixmap = QPixmap("../Resource/Photo/show.jpg")
        pixmap.scaledToHeight(self.height)
        self.image.setPixmap(pixmap)
        self.image.mouseReleaseEvent=self.image_click
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
            QRect(self.width / 2 - size / 2, self.height / 2 - size / 2 + diff * 2, size + 20, size + 20))
        self.button.clicked.connect(self.photo_click)
        self.button.pressed.connect(self.photo_pressed)
        self.button.setStyleSheet(self.bstyle)

        # Button Exity
        self.button2 = QPushButton(self)
        size = max(self.width, self.height) / 15
        diff = max(self.width, self.height) / 8
        self.button2.move(self.width / 2 - size / 2 + diff, self.height / 2 - size / 2 + diff)
        self.Icon_back_active=QIcon()
        self.Icon_back_active.addPixmap(QPixmap('../Resource/Image/back.png'),mode=QIcon.Disabled)
        self.Icon_back_active.addPixmap(QPixmap('../Resource/Image/back.png'), mode=QIcon.Active)
        self.button2.setIcon(self.Icon_back_active)
        self.button2.setIconSize(QSize(size, size))
        self.button2.setGeometry(
            QRect(self.width / 5 - size / 2 , self.height / 2 - size / 2 + diff * 2, size + 20, size + 20))
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

    def begin(self):
        self.main_timer.start()
        self.image.hide()
        self.movie.jumpToFrame(0)
        self.movie.stop()
        self.movie2.jumpToFrame(0)
        self.movie2.stop()
        self.moviee.hide()
        self.button.setEnabled(True)
        self.button2.setEnabled(True)
        self.active=True

    def out(self):
        self.active=False
        self.main_timer.stop()
        self.image.hide()
        self.movie.jumpToFrame(0)
        self.movie.stop()
        self.movie2.jumpToFrame(0)
        self.movie2.stop()
        self.moviee.hide()
        if hasattr(self, 't2'):
            self.t2.stop()


    def timeout_timer(self):
        if  self.button.isEnabled():
            self.out()
            self.comm.timeout.emit()
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
        if self.active:
            self.button2.setEnabled(False)
            if os.name == 'posix':
                camera = picamera.PiCamera()
                camera.resolution = (2592, 1944)
                camera.rotation = 90
                name = "../Resource/Photo/Picture_" + datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".jpg"
                camera.capture(name)
                camera.close()
                correctionVal = 0.1
                img_file = Image.open(name)
                width, height = img_file.size
                img_file_white = Image.new("RGB", (width, height), "white")
                img_blended = Image.blend(img_file, img_file_white, correctionVal)
                img_blended.save("../Resource/Photo/show.jpg")
            elif os.name =='nt':
                cap = cv2.VideoCapture(0)
                ret, frame = cap.read()
                if ret!=False:
                    name = "../Resource/Photo/Picture_" + datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")+".jpg"
                    cv2.imwrite(name,frame)
                    correctionVal = 0.1
                    img_file = Image.open(name)
                    width, height = img_file.size
                    img_file_white = Image.new("RGB", (width, height), "white")
                    img_blended = Image.blend(img_file, img_file_white, correctionVal)
                    img_blended.save("../Resource/Photo/show.jpg")
                else:
                    time.sleep(2)
                cap.release()
            else:
                time.sleep(2)
            pixmap = QPixmap("../Resource/Photo/show.jpg")
            self.movie.stop()
            self.moviee.hide()
            pixmap = pixmap.scaledToWidth(self.width)
            self.image.move(0, self.height / 2 - pixmap.height() / 2)
            self.image.setPixmap(pixmap)
            self.image.show()
        self.button2.setEnabled(True)
        self.button.setEnabled(True)
        self.out()
        self.comm.goToReview.emit()

    def countdown(self):
        self.movie2.stop()
        self.moviee.setMovie(self.movie)
        self.movie.jumpToFrame(0)
        threading.Thread(target=self.takePicture,args=[]).start()
        self.movie.start()

    @pyqtSlot()
    def photo_click(self):
        self.button.setEnabled(False)
        self.main_timer.start()
        print("PyQt5 button1 click")
        self.button.setIcon(self.Icon_photo_active)
        self.image.hide()
        self.t2 = QTimer(self)
        self.t2.timeout.connect(self.countdown)
        self.t2.setSingleShot(True)
        self.t2.start(self.Gif_timer)  # changed timer timeout to 1s
        self.moviee.setMovie(self.movie2)
        self.movie2.jumpToFrame(0)
        self.moviee.show()
        self.movie2.start()

    @pyqtSlot()
    def close_click(self):
        print('PyQt5 button2 click')
        self.button2.setIcon(self.Icon_back_active)
        self.out()
        self.comm.goToMain.emit()

    @pyqtSlot()
    def photo_pressed(self):
        print('PyQt5 button1 pressed')
        self.button.setIcon(QIcon('../Resource/Image/photo_down.png'))

    @pyqtSlot()
    def close_pressed(self):
        print('PyQt5 button2 pressed')
        self.button2.setIcon(QIcon('../Resource/Image/back_down.png'))

    def gif_click(self, event):
        print('PyQt5 Gif Click')

    def image_click(self,event):
        self.out()
        self.comm.goToReview.emit()


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