import sys, os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel,QMainWindow
from PyQt5.QtGui import QIcon,QMovie,QPixmap
from PyQt5.QtCore import pyqtSlot, QSize, QRect,Qt
from tkinter import *
import time
from threading import Timer
import threading
if os.name == 'posix':
    import picamera
    import RPi.GPIO as GPIO

class PictureApp(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Nandor Magic Mirror'
        self.widget=self
        self.left = 10
        self.top = 10
        self.lastTrigger=time.time()
        self.width = 320
        self.height = 200
        self.setAutoFillBackground(True)
        if os.name == 'posix':
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(4, GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
            GPIO.setup(17, GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
            GPIO.add_event_detect(4,GPIO.FALLING)
            GPIO.add_event_callback(4, self.gpio_callback)
            GPIO.add_event_detect(17,GPIO.RISING)
            GPIO.add_event_callback(17, self.gpio_callback2)
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setStyleSheet("background-color:black;")
        self.root = Tk()
        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        self.root.destroy()
        # Add image
        self.image = QLabel(self)
        pixmap = QPixmap("test_image.jpg")
        pixmap.scaledToHeight(self.height)
        self.image.setPixmap(pixmap)
        self.image.hide()

        self.bstyle="QPushButton{background: transparent;outline: none;border: none}"
        #Button    border-width: 5px;padding: 5px;border-style:solid;border-radius: 5px
        self.button = QPushButton(self)
        size=max(self.width,self.height)/6
        diff=max(self.width,self.height)/8
        self.button.move(self.width/2-size/2-diff, self.height/2-size/2+diff)
        self.button.setIcon(QIcon('photo.png'))
        self.button.setIconSize(QSize(size, size))
        self.button.setGeometry(QRect(self.width/2-size/2-diff, self.height/2-size/2+diff*2, size+20, size+20))
        self.button.clicked.connect(self.photo_click)
        self.button.pressed.connect(self.photo_pressed)
        self.button.setStyleSheet(self.bstyle)
        
        #Button Exity
        self.button2 = QPushButton( self)
        size=max(self.width,self.height)/6
        diff=max(self.width,self.height)/8
        self.button2.move(self.width/2-size/2+diff, self.height/2-size/2+diff)
        self.button2.setIcon(QIcon('off.png'))
        self.button2.setIconSize(QSize(size, size))
        self.button2.setGeometry(QRect(self.width/2-size/2+diff, self.height/2-size/2+diff*2, size+20, size+20))
        self.button2.clicked.connect(self.close_click)
        self.button2.pressed.connect(self.close_pressed)
        self.button2.setStyleSheet(self.bstyle)
        self.button2.setFlat(True)

        self.addLoading()

        #Text for Sensors
        self.sense=QLabel('Nothing to Sense',self)
        self.sense.setStyleSheet("background: transparent;color:white;font-size:36pt")
        width = self.sense.fontMetrics().boundingRect(self.sense.text()).width()
        self.sense.move(self.width / 2 - 220, 200)
        self.sense.update()

        #Show
        self.showFullScreen()

    def gpio_callback(self,channel):
        if time.time() > self.lastTrigger + 5:
            self.lastTrigger=time.time()
            self.sense.setText('Proximity Sense')
            width = self.sense.fontMetrics().boundingRect(self.sense.text()).width()
            self.sense.move(self.width / 2 - width/2, 200)
            self.sense.update()

    def gpio_callback2(self,channel):
        if time.time() > self.lastTrigger + 5:
            self.lastTrigger=time.time()
            self.sense.setText('PiR Sense')
            width = self.sense.fontMetrics().boundingRect(self.sense.text()).width()
            self.sense.move(self.width / 2 - width/2, 200)
            self.sense.update()

    def takePicture(self):
        if os.name == 'posix':
            camera=picamera.PiCamera()
            camera.resolution = (1920, 1080)
            camera.capture("test_image.jpg")
            camera.close()
        else:
            time.sleep(2)
        self.movie.stop()
        self.moviee.hide()
        pixmap = QPixmap("test_image.jpg")
        pixmap=pixmap.scaledToWidth(self.width)
        self.image.move(0,self.height/2-pixmap.height()/2)
        self.image.setPixmap(pixmap)
        self.image.show()

    def addLoading(self):
        self.moviee = QLabel(self)
        self.movie = QMovie("load.gif")
        size = max(self.width,self.height) / 5
        diff = max(self.width,self.height) / 12
        self.movie.setScaledSize(QSize(size, size))
        self.moviee.setMovie(self.movie)
        self.moviee.move(self.width / 2 - size / 2 + diff, self.height / 2 - size / 2 + diff)
        self.moviee.setGeometry(
            QRect(self.width / 2 - size / 2, self.height / 2 - size / 2 - diff, size + 20, size + 20))
        self.moviee.setAttribute(Qt.WA_TranslucentBackground)
        self.moviee.mouseReleaseEvent=self.gif_click
        self.movie.timerEvent()
        # self.movie.start



    @pyqtSlot()
    def photo_click(self):
        print("PyQt5 button1 click")
        self.button.setIcon(QIcon('photo.png'))
        self.image.hide()
        self.t1=threading.Thread(target=self.takePicture,args=[])
        self.t1.start()
        self.moviee.show()
        self.movie.start()

    @pyqtSlot()
    def close_click(self):
        print('PyQt5 button2 click')
        self.close()

    @pyqtSlot()
    def photo_pressed(self):
        print('PyQt5 button1 pressed')
        self.button.setIcon(QIcon('photo down.png'))

    @pyqtSlot()
    def close_pressed(self):
        print('PyQt5 button2 pressed')
        self.button2.setIcon(QIcon('off_down.png'))

    def gif_click(self,event):
        print('PyQt5 Gif Click')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QMainWindow()
    ex = PictureApp(parent=window)
    sys.exit(app.exec_())
