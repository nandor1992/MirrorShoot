import sys, os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QMainWindow
from PyQt5.QtGui import QIcon, QMovie, QPixmap
from PyQt5.QtCore import pyqtSlot, QSize, QRect, Qt, QTimer,QObject, pyqtSignal
from tkinter import *
import time
import threading
import datetime
from PIL import Image

class ListApp(QWidget):
    def __init__(self,parent,comm):
        super(QWidget,self).__init__(parent)
        self.title = 'Nandor Magic Mirror'
        self.lastTrigger = time.time()
        self.comm=comm
        self.comm.goToList.connect(self.begin)
        self.active=False
        self.initUI()

    def initUI(self):
        self.root = Tk()
        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        self.root.destroy()

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
        self.Icon_back_active = QIcon()
        self.Icon_back_active.addPixmap(QPixmap('../Resource/Image/back.png'), mode=QIcon.Disabled)
        self.Icon_back_active.addPixmap(QPixmap('../Resource/Image/back.png'), mode=QIcon.Active)
        self.button2.setIcon(self.Icon_back_active)
        self.button2.setIconSize(QSize(size, size))
        self.button2.setGeometry(
            QRect(self.width / 2 - size / 2 + diff, self.height / 2 - size / 2 + diff * 2, size + 20, size + 20))
        self.button2.clicked.connect(self.close_click)
        self.button2.pressed.connect(self.close_pressed)
        self.button2.setStyleSheet(self.bstyle)
        self.button2.setFlat(True)

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

    @pyqtSlot()
    def photo_click(self):
        print("PyQt5 button1 click")
        self.button.setIcon(QIcon('../Resource/Image/photo.png'))
        self.out()
        self.comm.goToIndividual.emit("Nandor")

    @pyqtSlot()
    def photo_pressed(self):
        print('PyQt5 button1 pressed')
        self.button.setIcon(QIcon('../Resource/Image/photo_down.png'))

    @pyqtSlot()
    def close_click(self):
        print('PyQt5 button2 click')
        self.button2.setIcon(self.Icon_back_active)
        self.out()
        self.comm.goToMain.emit()

    @pyqtSlot()
    def close_pressed(self):
        print('PyQt5 button2 pressed')
        self.button2.setIcon(QIcon('../Resource/Image/back_down.png'))

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