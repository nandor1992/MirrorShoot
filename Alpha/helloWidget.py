import sys, os
from PyQt5.QtWidgets import QApplication, QWidget,QLabel, QMainWindow, QStackedWidget
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
        self.Delay_timer=5000
        self.gif_timer=1800
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
        self.main_timer.start()
        self.movie.stop()  # those lines
        self.timer.stop()
        self.movie.jumpToFrame(0)
        self.active=True

    def out(self):
        self.active=False
        self.movie.jumpToFrame(0)
        self.movie.stop()
        self.timer.stop()
        self.main_timer.stop()

    def initUI(self):
        self.root = Tk()
        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        self.root.destroy()


        #Add Gif
        self.moviee = QLabel(self)
        self.movie = QMovie("../Resource/Gif/hello.gif")
        size = max(self.width, self.height) / 3
        self.movie.setScaledSize(QSize(size+300,size))
        self.moviee.setMovie(self.movie)
        self.moviee.setGeometry(QRect(self.width / 2 - size/2-150, self.height / 2 - size / 2, size+300,size))
        self.moviee.setAttribute(Qt.WA_TranslucentBackground)
        self.moviee.mouseReleaseEvent = self.gif_click
        self.moviee.show()
        self.movie.start()

        #Timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.timer_)
        self.timer.start(self.gif_timer)  # changed timer timeout to 1s

        self.main_timer = QTimer(self)
        self.main_timer.timeout.connect(self.timer2_)
        self.main_timer.start(self.Delay_timer)  # changed timer timeout to 1s


    def timer_(self):
        self.movie.stop()  # those lines
        self.timer.stop()
        self.main_timer.start(self.Delay_timer)

    def timer2_(self):
        self.timer.start(self.gif_timer)
        self.lastTrigger=time.time()
        self.movie.start()
        self.main_timer.stop()

    def gpio_callback(self, channel):
        if time.time() > self.lastTrigger + self.Delay_timer/1000 and self.active:
            self.lastTrigger = time.time()
            self.movie.jumpToFrame(0)
            self.movie.start()
            self.timer.start(self.gif_timer)

    def gpio_callback2(self, channel):
        if time.time() > self.lastTrigger + self.Delay_timer/1000 and self.active:
            self.lastTrigger = time.time()
            self.movie.jumpToFrame(0)
            self.movie.start()
            self.timer.start(self.gif_timer)

    def gif_click(self, event):
        print('PyQt5 Gif Click')
        self.out()
        self.comm.goToMain.emit()


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Nandor Mirror'
        self.setWindowTitle(self.title)
        self.setStyleSheet("background-color:blue;")
        self.table_widget = IdleApp(self)
        self.setCentralWidget(self.table_widget)
        self.showFullScreen()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
