import sys, os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QMainWindow,QDesktopWidget
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

class PictureApp(QWidget):
    def __init__(self,parent,comm):
        super(QWidget,self).__init__(parent)
        self.title = 'Nandor Magic Mirror'
        self.lastTrigger = time.time()
        self.comm=comm
        self.comm.goToPicture.connect(self.begin)
        self.active=False
        self.initUI()

    def initScreen(self):
        screen2 = QDesktopWidget().screenGeometry(1)
        screen1 = QDesktopWidget().screenGeometry(0)
        if screen2.right()>0:
            self.width = screen2.right()-screen2.left()
            self.height = screen2.bottom()
        else:
            self.width = screen1.right()
            self.height = screen1.bottom()

    def initUI(self):
        self.initScreen()
        self.Gif_timer=7000
        self.Idle_timer=30000
        # Add image
        self.image = QLabel(self)
        pixmap = QPixmap("../Resource/Photo/show.jpg")
        pixmap.scaledToWidth(self.width*0.6)
        self.image.setPixmap(pixmap)
        self.image.mouseReleaseEvent=self.image_click
        self.image.hide()

        self.bstyle = "QPushButton{background: transparent;outline: none;border: none}"
        # Button    border-width: 5px;padding: 5px;border-style:solid;border-radius: 5px
        self.button = QPushButton(self)
        size = max(self.width, self.height) / 6
        self.Icon_photo_active=QIcon()
        self.Icon_photo_active.addPixmap(QPixmap('../Resource/Image/photo.png'),mode=QIcon.Disabled)
        self.Icon_photo_active.addPixmap(QPixmap('../Resource/Image/photo.png'), mode=QIcon.Active)
        self.button.setIcon(self.Icon_photo_active)
        self.button.setIconSize(QSize(size, size))
        self.button.setGeometry(
            QRect(self.width / 2 - size / 2, self.height - size -size/4 , size + 20, size + 20))
        self.button.clicked.connect(self.photo_click)
        self.button.pressed.connect(self.photo_pressed)
        self.button.setStyleSheet(self.bstyle)

        # Button Exity
        self.button2 = QPushButton(self)
        size = max(self.width, self.height) / 15
        self.Icon_back_active=QIcon()
        self.Icon_back_active.addPixmap(QPixmap('../Resource/Image/back.png'),mode=QIcon.Disabled)
        self.Icon_back_active.addPixmap(QPixmap('../Resource/Image/back.png'), mode=QIcon.Active)
        self.button2.setIcon(self.Icon_back_active)
        self.button2.setIconSize(QSize(size, size))
        self.button2.setGeometry(
            QRect(self.width / 6 - size / 2 , self.height - 2*size, size + 20, size + 20))
        self.button2.clicked.connect(self.close_click)
        self.button2.pressed.connect(self.close_pressed)
        self.button2.setStyleSheet(self.bstyle)
        self.button2.setFlat(True)

        self.addLoading()
        self.showFullScreen()

    def begin(self):
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
        self.image.hide()
        self.movie.jumpToFrame(0)
        self.movie.stop()
        self.movie2.jumpToFrame(0)
        self.movie2.stop()
        self.moviee.hide()
        if hasattr(self, 't2'):
            self.t2.stop()


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
        self.comm.resetTimeout.emit()
        if self.active:
            self.button2.setEnabled(False)
            if os.name == 'posix':
                camera = picamera.PiCamera()
                camera.resolution = (2592, 1944)
                name = "../Resource/Photo/Picture_" + datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".jpg"
                camera.capture(name)
                camera.close()
                correctionVal = 0
                img_file = Image.open(name)
                width, height = img_file.size
                img_file_white = Image.new("RGB", (width, height), "white")
                img_blended = Image.blend(img_file, img_file_white, correctionVal)
                img_blended.save("../Resource/Photo/show.jpg")
            elif os.name =='nt':
                name = "../Resource/Photo/Picture_" + datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")+".jpg"
                name_pic="Picture_" + datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")+".jpg"
                self.takeNikonPic(name_pic)
                correctionVal = 0
                img_file = Image.open(name)
                img2=img_file.rotate(90,expand=True)
                #width, height = img_file.size
                #img_file_white = Image.new("RGB", (width, height), "white")
                #img_blended = Image.blend(img_file, img_file_white, correctionVal)
                img2.save("../Resource/Photo/show.jpg")
                img2.save(name)
            else:
                time.sleep(2)
            pixmap = QPixmap("../Resource/Photo/show.jpg")
            self.movie.stop()
            self.moviee.hide()
            pixmap = pixmap.scaledToWidth(self.width*0.6)
            self.image.setPixmap(pixmap)
            self.image.show()
        self.button2.setEnabled(True)
        self.button.setEnabled(True)
        self.out()
        self.comm.goToReview.emit()

    def takeNikonPic(self,name):
        dir_path = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
        dir_path += "\Resource\Photo\\"
        print(dir_path)
        dir = '"C:/Program Files (x86)/digiCamControl/CameraControlCmd.exe"'
        os.system(dir + "/filename " + dir_path + name + " /capture ")

    def countdown(self):
        self.movie2.stop()
        self.moviee.setMovie(self.movie)
        self.movie.jumpToFrame(0)
        threading.Thread(target=self.takePicture,args=[]).start()
        self.movie.start()

    @pyqtSlot()
    def photo_click(self):
        self.comm.resetTimeout.emit()
        self.button.setEnabled(False)
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
        self.comm.resetTimeout.emit()
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
        self.comm.resetTimeout.emit()
        print('PyQt5 Gif Click')

    def image_click(self,event):
        self.out()
        self.comm.resetTimeout.emit()
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