import sys, os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QMainWindow
from PyQt5.QtGui import QIcon, QMovie, QPixmap
from PyQt5.QtCore import pyqtSlot, QSize, QRect, Qt, QTimer,QObject, pyqtSignal
from tkinter import *
import time
import threading
import datetime
from PIL import Image

class IndiApp(QWidget):
    def __init__(self,parent,comm):
        super(QWidget,self).__init__(parent)
        self.title = 'Nandor Magic Mirror'
        self.lastTrigger = time.time()
        self.comm=comm
        self.comm.goToIndividual.connect(self.begin)
        self.active=False
        self.initUI()

    def initUI(self):
        self.root = Tk()
        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        self.root.destroy()

        self.textLabel = QLabel(self)
        self.textLabel.setText("...Nothing")
        self.textLabel.setStyleSheet(
            "QLabel{background: transparent;outline: none;border: none;color:white; font-size:42pt}")
        self.textLabel.setGeometry(QRect(self.width / 2 - 100, self.height / 2 - 80, 300, 80))
        self.textLabel.hide()

        self.bstyle = "QPushButton{background: transparent;outline: none;border: none}"
        # Button    border-width: 5px;padding: 5px;border-style:solid;border-radius: 5px
        self.button = QPushButton(self)
        size = max(self.width, self.height) / 6
        diff = max(self.width, self.height) / 8
        self.button.move(self.width / 2 - size / 2 - diff, self.height / 2 - size / 2 + diff)
        self.Icon_photo_active=QIcon()
        self.Icon_photo_active.addPixmap(QPixmap('../Resource/Image/back.png'),mode=QIcon.Disabled)
        self.Icon_photo_active.addPixmap(QPixmap('../Resource/Image/back.png'), mode=QIcon.Active)
        self.button.setIcon(self.Icon_photo_active)
        self.button.setIconSize(QSize(size, size))
        self.button.setGeometry(
            QRect(self.width / 2 - size / 2 - diff, self.height / 2 - size / 2 + diff * 2, size + 20, size + 20))
        self.button.clicked.connect(self.photo_click)
        self.button.pressed.connect(self.photo_pressed)
        self.button.setStyleSheet(self.bstyle)

        self.main_timer = QTimer(self)
        self.Idle_timer = 30000
        self.main_timer.timeout.connect(self.timeout_timer)
        self.main_timer.start(self.Idle_timer)  # changed timer timeout to 1s

    def begin(self,param1):
        print(param1)
        self.active=True
        self.textLabel.setGeometry(QRect(self.width / 2 - 120, self.height / 2 - 80, 300, 100))
        self.textLabel.setText(param1)
        self.textLabel.show()
        self.main_timer.start(self.Idle_timer)

    def out(self):
        self.active=False
        self.main_timer.stop()
        self.textLabel.hide()

    def timeout_timer(self):
        self.out()
        self.comm.timeout.emit()


    @pyqtSlot()
    def photo_click(self):
        print("PyQt5 button1 click")
        self.button.setIcon(self.Icon_photo_active)
        self.out()
        self.comm.goToList.emit()

    @pyqtSlot()
    def photo_pressed(self):
        print('PyQt5 button1 pressed')
        self.button.setIcon(QIcon('../Resource/Image/back_down.png'))


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