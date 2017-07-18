import sys, os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QMainWindow,QDesktopWidget
from PyQt5.QtGui import QIcon, QMovie, QPixmap
from PyQt5.QtCore import pyqtSlot, QSize, QRect, Qt, QTimer,QObject, pyqtSignal
from tkinter import *
import time
import threading
import datetime
from PIL import Image

class MenuApp(QWidget):
    def __init__(self,parent,comm):
        super(QWidget,self).__init__(parent)
        self.title = 'Nandor Magic Mirror'
        self.lastTrigger = time.time()
        self.comm=comm
        self.comm.goToMain.connect(self.begin)
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
        self.image = QLabel(self)
        pixmap = QPixmap("../Resource/Image/title.png")
        pixmap = pixmap.scaledToWidth(self.width/4*3)
        self.image.move(self.width/2-pixmap.width()/2, self.height / 4 - pixmap.height())
        self.image.setPixmap(pixmap)
        self.image.show()


        self.bstyle = "QPushButton{background: transparent;outline: none;border: none}"
        # Button    border-width: 5px;padding: 5px;border-style:solid;border-radius: 5px
        self.button = QPushButton(self)
        self.Icon_photo_active=QIcon()
        pixmap = QPixmap("../Resource/Image/take_pic.png")
        pixmap = pixmap.scaledToWidth(self.width / 2)
        self.Icon_photo_active.addPixmap(pixmap,mode=QIcon.Disabled)
        self.Icon_photo_active.addPixmap(pixmap, mode=QIcon.Active)
        self.button.setIcon(self.Icon_photo_active)
        self.button.setIconSize(QSize(pixmap.width(), pixmap.height()))
        self.button.setGeometry(
            QRect(self.width / 2 - pixmap.width() / 2 , self.height / 2  - pixmap.height() , pixmap.width() +20 , pixmap.height()+20))
        self.button.clicked.connect(self.photo_click)
        self.button.pressed.connect(self.photo_pressed)
        self.button.setStyleSheet(self.bstyle)

        self.button2 = QPushButton(self)
        self.Icon_back_active = QIcon()
        pixmap2 = QPixmap("../Resource/Image/list_pic.png")
        pixmap2 = pixmap2.scaledToWidth(self.width / 2)
        self.Icon_back_active.addPixmap(pixmap2, mode=QIcon.Disabled)
        self.Icon_back_active.addPixmap(pixmap2, mode=QIcon.Active)
        self.button2.setIcon(self.Icon_back_active)
        self.button2.setIconSize(QSize(pixmap2.width(), pixmap2.height()))
        self.button2.setGeometry(
            QRect(self.width / 2 - pixmap2.width() / 2, self.height / 2 +50, pixmap2.width() + 20,
                  pixmap2.height() + 20))

        self.button2.clicked.connect(self.close_click)
        self.button2.pressed.connect(self.close_pressed)
        self.button2.setStyleSheet(self.bstyle)
        self.button2.setFlat(True)

        self.button3 = QPushButton(self)
        self.Icon_back_exit = QIcon()
        pixmap3 = QPixmap("../Resource/Image/off.png")
        pixmap3 = pixmap3.scaledToWidth(self.width / 4)
        self.Icon_back_exit.addPixmap(pixmap3, mode=QIcon.Disabled)
        self.Icon_back_exit.addPixmap(pixmap3, mode=QIcon.Active)
        self.button3.setIcon(self.Icon_back_exit)
        self.button3.setIconSize(QSize(pixmap3.width(), pixmap3.height()))
        self.button3.setGeometry(
            QRect(self.width / 2 - pixmap3.width() / 2, self.height - 50 - pixmap3.height(), pixmap3.width() + 20,
                  pixmap3.height() + 20))

        self.button3.clicked.connect(self.exit_click)
        self.button3.pressed.connect(self.exit_pressed)
        self.button3.setStyleSheet(self.bstyle)
        self.button3.setFlat(True)

        self.main_timer = QTimer(self)
        self.Idle_timer = 30000
        self.main_timer.timeout.connect(self.timeout_timer)
        self.main_timer.start(self.Idle_timer)  # changed timer timeout to 1s


    def begin(self):
        self.active=True
        self.main_timer.start(self.Idle_timer)

    def out(self):
        self.active=False
        self.main_timer.stop()

    def timeout_timer(self):
        self.out()
        self.comm.timeout.emit()


    def countdown(self):
        self.movie2.stop()
        self.moviee.setMovie(self.movie)
        self.movie.jumpToFrame(0)
        threading.Thread(target=self.takePicture,args=[]).start()
        self.movie.start()

    @pyqtSlot()
    def photo_click(self):
        print("PyQt5 button1 click")
        self.button.setIcon(self.Icon_photo_active)
        self.out()
        self.comm.goToPicture.emit()

    @pyqtSlot()
    def photo_pressed(self):
        print('PyQt5 button1 pressed')
        self.button.setIcon(QIcon('../Resource/Image/take_pic_down.png'))

    @pyqtSlot()
    def close_click(self):
        print('PyQt5 button2 click')
        self.button2.setIcon(self.Icon_back_active)
        self.out()
        self.comm.goToList.emit()

    @pyqtSlot()
    def close_pressed(self):
        print('PyQt5 button2 pressed')
        self.button2.setIcon(QIcon('../Resource/Image/list_pic_down.png'))

    @pyqtSlot()
    def exit_click(self):
        print('PyQt5 button2 click')
        self.button3.setIcon(self.Icon_back_exit)
        self.out()
        self.comm.exit.emit()

    @pyqtSlot()
    def exit_pressed(self):
        print('PyQt5 button2 pressed')
        self.button3.setIcon(QIcon('../Resource/Image/off_down.png'))

class Communicate(QObject):
    goToPicture = pyqtSignal()
    goToMain = pyqtSignal()
    goToReview = pyqtSignal()
    goToList = pyqtSignal()
    goToIndividual = pyqtSignal()
    timeout = pyqtSignal()
    exit = pyqtSignal()

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Nandor Mirror'
        self.setWindowTitle(self.title)
        self.setStyleSheet("background-color:black;")
        self.c = Communicate()
        self.table_widget = MenuApp(self,self.c)
        self.setCentralWidget(self.table_widget)
        self.showFullScreen()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())