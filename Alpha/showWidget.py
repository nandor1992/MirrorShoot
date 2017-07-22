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

class showApp(QWidget):
    def __init__(self,parent,comm):
        super(QWidget,self).__init__(parent)
        self.title = 'Nandor Magic Mirror'
        self.lastTrigger = time.time()
        self.comm=comm
        self.comm.goToReview.connect(self.begin)
        self.active=False
        self.print=Printer()
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
        pixmap.scaledToWidth(self.width - 200)
        self.image.setGeometry(
            QRect(100, 50, self.width - 100, self.height - 400))
        self.image.setPixmap(pixmap)
        self.image.hide()

        self.textLabel = QLabel(self)
        self.textLabel.setText("...Nothing")
        self.textLabel.setStyleSheet("QLabel{background: transparent;outline: none;border: none;color:white; font-size:42pt}")
        self.textLabel.setGeometry(QRect(self.width / 2 -100, self.height / 2 -80, 300,80))
        self.textLabel.hide()
        self.bstyle = "QPushButton{background: transparent;outline: none;border: none}"

        # Button    border-width: 5px;padding: 5px;border-style:solid;border-radius: 5px
        self.button = QPushButton(self)
        self.Icon_save = QIcon()
        pixmap = QPixmap("../Resource/Image/save.png")
        pixmap = pixmap.scaledToWidth(self.width / 5)
        self.Icon_save.addPixmap(pixmap, mode=QIcon.Disabled)
        self.Icon_save.addPixmap(pixmap, mode=QIcon.Active)
        self.button.setIcon(self.Icon_save)
        self.button.setIconSize(QSize(pixmap.width(), pixmap.height()))
        self.button.setGeometry(
            QRect(self.width / 4 - pixmap.width() / 2, self.height/7*6 - pixmap.height()/2 , pixmap.width() + 40,
                  pixmap.height() + 60))
        self.button.clicked.connect(self.save_click)
        self.button.pressed.connect(self.save_pressed)
        self.button.setStyleSheet(self.bstyle)

        # Button    border-width: 5px;padding: 5px;border-style:solid;border-radius: 5px
        self.button2 = QPushButton(self)
        self.Icon_print = QIcon()
        pixmap = QPixmap("../Resource/Image/print.png")
        pixmap = pixmap.scaledToWidth(self.width / 5)
        self.Icon_print.addPixmap(pixmap, mode=QIcon.Disabled)
        self.Icon_print.addPixmap(pixmap, mode=QIcon.Active)
        self.button2.setIcon(self.Icon_print)
        self.button2.setIconSize(QSize(pixmap.width(), pixmap.height()))
        self.button2.setGeometry(
            QRect(self.width / 2 - pixmap.width() / 2, self.height/7*6 - pixmap.height()/2 , pixmap.width() + 40,
                  pixmap.height() + 60))
        self.button2.clicked.connect(self.print_click)
        self.button2.pressed.connect(self.print_pressed)
        self.button2.setStyleSheet(self.bstyle)


        # Button    border-width: 5px;padding: 5px;border-style:solid;border-radius: 5px
        self.button3 = QPushButton(self)
        self.Icon_delete = QIcon()
        pixmap = QPixmap("../Resource/Image/delete.png")
        pixmap = pixmap.scaledToWidth(self.width / 5)
        self.Icon_delete.addPixmap(pixmap, mode=QIcon.Disabled)
        self.Icon_delete.addPixmap(pixmap, mode=QIcon.Active)
        self.button3.setIcon(self.Icon_delete)
        self.button3.setIconSize(QSize(pixmap.width(), pixmap.height()))
        self.button3.setGeometry(
            QRect(self.width / 4*3 - pixmap.width() / 2, self.height/7*6 - pixmap.height()/2 , pixmap.width() + 40,
                  pixmap.height() + 60))
        self.button3.clicked.connect(self.delete_click)
        self.button3.pressed.connect(self.delete_pressed)
        self.button3.setStyleSheet(self.bstyle)

    def begin(self,name):
        self.active=True
        self.name=name
        pixmap = QPixmap(name)
        pixmap = pixmap.scaledToWidth(self.width - 200)
        self.image.setPixmap(pixmap)
        self.image.show()
        self.button.setEnabled(True)
        self.button2.setEnabled(True)
        self.button3.setEnabled(True)
        self.textLabel.hide()

    def out(self):
        self.active=False

    def goBack(self):
        print("Leaving Show Widget")
        time.sleep(0.5)
        self.out()
        self.comm.goToPicture.emit()

    def setTextSave(self):
        time.sleep(1.5)
        print("Saving")
        self.textLabel.setGeometry(QRect(self.width / 2 - 60, self.height / 2 - 80, 350, 100))
        self.textLabel.setText("Saved!")
        threading.Thread(target=self.goBack).start()

    def setTextDelete(self):
        time.sleep(1.5)
        print("Deleting "+self.name)
        self.textLabel.setGeometry(QRect(self.width / 2 - 80, self.height / 2 - 80, 350, 100))
        os.remove(self.name)
        self.textLabel.setText("Deleted!")
        threading.Thread(target=self.goBack).start()


    @pyqtSlot()
    def print_click(self):
        self.comm.resetTimeout.emit()
        print("PyQt5 button1 click")
        self.button2.setIcon(self.Icon_print)
        self.button.setEnabled(False)
        self.button2.setEnabled(False)
        self.button3.setEnabled(False)
        self.textLabel.setGeometry(QRect(self.width / 2 - 120, self.height / 2 - 80, 300, 100))
        self.textLabel.setText("...Printing")
        self.textLabel.show()
        self.comm.resetTimeout.emit()
        threading.Thread(target=self.print_photo, args=["show.jpg"]).start()

    def print_photo(self,name):
        self.print.printPhoto(name)
        self.textLabel.setGeometry(QRect(self.width / 2 - 80, self.height / 2 - 80, 350, 100))
        self.textLabel.setText("Printed!")
        #Add part wit hactuall printing of photo
        print("Leaving Show Widget")
        time.sleep(0.5)
        self.goBack()

    @pyqtSlot()
    def print_pressed(self):
        print('PyQt5 button1 pressed')
        self.button2.setIcon(QIcon('../Resource/Image/print_down.png'))

    @pyqtSlot()
    def save_click(self):
        self.comm.resetTimeout.emit()
        print("PyQt5 button1 click")
        self.button.setIcon(self.Icon_save)
        self.button.setEnabled(False)
        self.button2.setEnabled(False)
        self.button3.setEnabled(False)
        self.textLabel.setGeometry(QRect(self.width / 2 - 100, self.height / 2 - 80, 300, 100))
        self.textLabel.setText("...Saving")
        self.textLabel.show()
        threading.Thread(target=self.setTextSave).start()

    @pyqtSlot()
    def save_pressed(self):
        print('PyQt5 button1 pressed')
        self.button.setIcon(QIcon('../Resource/Image/save_down.png'))

    @pyqtSlot()
    def delete_click(self):
        self.comm.resetTimeout.emit()
        print("PyQt5 button1 click")
        self.button3.setIcon(self.Icon_delete)
        self.button.setEnabled(False)
        self.button2.setEnabled(False)
        self.button3.setEnabled(False)
        self.textLabel.setGeometry(QRect(self.width / 2 - 100, self.height / 2 - 80, 350, 100))
        self.textLabel.setText("...Deleting")
        self.textLabel.show()
        threading.Thread(target=self.setTextDelete).start()

    @pyqtSlot()
    def delete_pressed(self):
        print('PyQt5 button1 pressed')
        self.button3.setIcon(QIcon('../Resource/Image/delete_down.png'))

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
        self.table_widget = showApp(self,self.c)
        self.table_widget.begin()
        self.setCentralWidget(self.table_widget)
        self.showFullScreen()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())