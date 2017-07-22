import sys, os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QMainWindow,QDesktopWidget
from PyQt5.QtGui import QIcon, QMovie, QPixmap
from PyQt5.QtCore import pyqtSlot, QSize, QRect, Qt, QTimer,QObject, pyqtSignal
from tkinter import *
import time
import threading
import datetime
from PIL import Image
if sys.version_info >(3,5):
    from Alpha.Printer import Printer
else:
    from Printer import Printer
class IndiApp(QWidget):
    def __init__(self,parent,comm):
        super(QWidget,self).__init__(parent)
        self.title = 'Nandor Magic Mirror'
        self.lastTrigger = time.time()
        self.comm=comm
        self.comm.goToIndividual.connect(self.begin)
        self.active=False
        self.print = Printer()
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


        # Add image
        self.image = QLabel(self)
        pixmap = QPixmap("../Resource/Photo/show.jpg")
        pixmap.scaledToWidth(self.width-200)
        self.image.setGeometry(
            QRect(100,50,self.width-100,self.height-400))
        self.image.setPixmap(pixmap)
        self.image.hide()

        #Label
        self.textLabel = QLabel(self)
        self.textLabel.setText("...Nothing")
        self.textLabel.setStyleSheet(
            "QLabel{background: transparent;outline: none;border: none;color:white; font-size:42pt}")
        self.textLabel.setGeometry(QRect(self.width / 2 - 100, self.height / 2 - 80, 300, 80))
        self.textLabel.hide()

        self.bstyle = "QPushButton{background: transparent;outline: none;border: none}"
        # Button    border-width: 5px;padding: 5px;border-style:solid;border-radius: 5px
        self.button = QPushButton(self)
        size = max(self.width, self.height) / 10
        self.Icon_photo_active=QIcon()
        self.Icon_photo_active.addPixmap(QPixmap('../Resource/Image/back.png'),mode=QIcon.Disabled)
        self.Icon_photo_active.addPixmap(QPixmap('../Resource/Image/back.png'), mode=QIcon.Active)
        self.button.setIcon(self.Icon_photo_active)
        self.button.setIconSize(QSize(size, size))
        self.button.setGeometry(
            QRect(size / 3, self.height - size - size / 4, size + 20, size + 20))
        self.button.clicked.connect(self.photo_click)
        self.button.pressed.connect(self.photo_pressed)
        self.button.setStyleSheet(self.bstyle)

        #Button2
        self.button2 = QPushButton(self)
        self.Icon_print = QIcon()
        self.Icon_print.addPixmap(QPixmap('../Resource/Image/print_img.png'), mode=QIcon.Disabled)
        self.Icon_print.addPixmap(QPixmap('../Resource/Image/print_img.png'), mode=QIcon.Active)
        self.button2.setIcon(self.Icon_print)
        size = max(self.width, self.height) / 6
        self.button2.setIconSize(QSize(size, size))
        self.button2.setGeometry(
            QRect(self.width / 2 - size / 2, self.height - size - size / 4, size + 20, size + 20))
        self.button2.clicked.connect(self.print_click)
        self.button2.pressed.connect(self.print_pressed)
        self.button2.setStyleSheet(self.bstyle)

        self.goBackTimer = QTimer(self)
        self.goBackTimer.timeout.connect(self.goBack)
        self.goBackTimer2 = QTimer(self)


    def begin(self,param1):
        print(param1)
        self.image_text=param1
        self.active=True
        pixmap = QPixmap("../Resource/Photo/"+param1)
        pixmap=pixmap.scaledToWidth(self.width-200)
        self.image.setPixmap(pixmap)
        self.image.show()
        self.textLabel.hide()

    def out(self):
        self.active=False
        self.image.hide()


    @pyqtSlot()
    def photo_click(self):
        self.comm.resetTimeout.emit()
        self.button.setIcon(self.Icon_photo_active)
        self.out()
        self.comm.goToList.emit()

    @pyqtSlot()
    def photo_pressed(self):
        self.button.setIcon(QIcon('../Resource/Image/back_down.png'))

    @pyqtSlot()
    def print_click(self):
        self.comm.resetTimeout.emit()
        self.button2.setIcon(self.Icon_print)
        self.button.setEnabled(False)
        self.button2.setEnabled(False)
        self.textLabel.setGeometry(QRect(self.width / 2 - 100, self.height / 2 - 80, 350, 100))
        self.textLabel.setText("...Printing")
        self.textLabel.show()
        self.comm.resetTimeout.emit()
        threading.Thread(target=self.print_photo, args=[self.image_text]).start()

    def print_photo(self,name):
        self.print.printPhoto(name)
        self.textLabel.setGeometry(QRect(self.width / 2 - 80, self.height / 2 - 80, 350, 100))
        self.textLabel.setText("Printed!")
        #Add part wit hactuall printing of photo
        print("Leaving Show Widget")
        self.comm.resetTimeout.emit()
        self.button.setEnabled(True)
        self.button2.setEnabled(True)
        time.sleep(0.5)

    def goBack(self):
        self.comm.resetTimeout.emit()
        self.button.setEnabled(True)
        self.button2.setEnabled(True)
        self.textLabel.hide()

    @pyqtSlot()
    def print_pressed(self):
        self.button2.setIcon(QIcon('../Resource/Image/print_img_down.png'))


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