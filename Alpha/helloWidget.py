import sys, os
from PyQt5.QtWidgets import QApplication, QWidget,QLabel, QMainWindow, QStackedWidget,QDesktopWidget
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import QRect, Qt, QSize, QTimer
from tkinter import *
import time

if os.name == 'posix':
    import picamera
    import RPi.GPIO as GPIO

class IdleApp(QWidget):
    def __init__(self,parent,comm):
        super(QWidget,self).__init__(parent)
        self.title = 'Nandor Magic Mirror'
        self.lastTrigger = time.time()
        self.comm=comm
        self.gif_timer=2600
        self.active=False
        comm.timeout.connect(self.begin)
        if os.name == 'posix':
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            GPIO.add_event_detect(4, GPIO.FALLING)
            GPIO.add_event_callback(4, self.gpio_callback)
            GPIO.add_event_detect(17, GPIO.RISING)
            GPIO.add_event_callback(17, self.gpio_callback2)
        self.initUI()

    def begin(self):
        self.lastTrigger = time.time()
        self.movie2.stop()
        self.movie2.jumpToFrame(0)
        self.movie2.stop()
        self.movie.jumpToFrame(0)
        self.active=True
        self.moviee.setMovie(self.movie)
        self.movie.start()
        self.timer.start(self.gif_timer)

    def out(self):
        self.active=False
        self.movie.jumpToFrame(0)
        self.movie.stop()
        self.movie2.jumpToFrame(0)
        self.movie2.stop()
        self.timer.stop()

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
        #Add Gif
        self.moviee = QLabel(self)
        self.movie = QMovie("../Resource/Gif/hello.gif")
        size = max(self.width, self.height) / 3
        self.movie.setScaledSize(self.scaleToWidth(size,self.movie))
        self.movie2 = QMovie("../Resource/Gif/IdleGif.gif")
        self.movie2.setScaledSize(self.scaleToWidth(size,self.movie2))
        self.moviee.setMovie(self.movie2)
        self.moviee.setAlignment(Qt.AlignCenter)
        self.moviee.setGeometry(QRect(50,50, self.width -50, self.height-50))
        self.moviee.setAttribute(Qt.WA_TranslucentBackground)
        self.moviee.mouseReleaseEvent = self.gif_click
        self.moviee.show()
        self.movie2.start()
        #Timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.timer_)


    def timer_(self):
        self.movie.stop()
        self.timer.stop()
        self.moviee.setMovie(self.movie2)
        self.movie2.jumpToFrame(0)
        self.movie2.start()

    def gpio_callback(self, channel):
        if time.time() > self.lastTrigger + 10 and self.active:
            self.comm.resetTimeout.emit()
            self.lastTrigger = time.time()
            self.movie.jumpToFrame(0)
            self.movie.start()
            self.timer.start(self.gif_timer)

    def gpio_callback2(self, channel):
        if time.time() > self.lastTrigger + 10 and self.active:
            self.comm.resetTimeout.emit()
            self.lastTrigger = time.time()
            self.movie.jumpToFrame(0)
            self.movie.start()
            self.timer.start(self.gif_timer)

    def gif_click(self, event):
        print('PyQt5 Gif Click')
        self.out()
        self.comm.resetTimeout.emit()
        self.comm.goToMain.emit()

    def scaleToWidth(self,width,movie):
        movie.jumpToFrame(0)
        w=movie.currentPixmap().width()
        h=movie.currentPixmap().height()
        ratio=float(width/w)
        return QSize(w*ratio,h*ratio)

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Nandor Mirror'
        self.setWindowTitle(self.title)
        self.setStyleSheet("background-color:blue;")
        self.table_widget = IdleApp(self)
        self.setCentralWidget(self.table_widget)
        self.showFullScreen()


if __name__ == '__main2__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
