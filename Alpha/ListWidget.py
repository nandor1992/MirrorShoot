import sys, os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QMainWindow, QScrollArea, QGridLayout
from PyQt5.QtGui import QIcon, QMovie, QPixmap
from PyQt5.QtCore import pyqtSlot, QSize, QRect, Qt, QTimer,QObject, pyqtSignal
from tkinter import *
from os import listdir
from os.path import isfile, join
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
            QRect(self.width / 2 - size / 2, self.height  - size / 2 - diff , size + 20, size + 20))
        self.button2.clicked.connect(self.close_click)
        self.button2.pressed.connect(self.close_pressed)
        self.button2.setStyleSheet(self.bstyle)
        self.button2.setFlat(True)

        self.tab1 = QScrollArea(self)
        self.tab1.setStyleSheet("QScrollArea{background: transparent;outline: none;border: none}")
        self.tab1.setGeometry(QRect(50,50,self.width-100 ,self.height*0.7))
        tab1_w=QWidget()
        tab1_layout = QGridLayout()
        tab1_layout.setColumnStretch(2, 4)
        tab1_w.setLayout(tab1_layout)
        # self.setWidgetResizable(True)
        onlyfiles = [f for f in listdir("../Resource/Photo") if isfile(join("../Resource/Photo", f))]
        cnt=0;
        self.images={}
        for i in onlyfiles:
            if i!="show.jpg" and i!="test_image.jpg":
                self.images[i] = QLabel(self)
                pixmap = QPixmap("../Resource/Photo/"+i)
                pixmap=pixmap.scaledToWidth((self.width-160)/4)
                self.images[i].setPixmap(pixmap)
                self.images[i].mouseReleaseEvent = lambda event, arg=i :self.image_click(arg)
                tab1_layout.addWidget(self.images[i],int(cnt/4),int(divmod(cnt,4)[1]))
                cnt += 1

        self.tab1.setWidget(tab1_w)
        self.tab1.setWidgetResizable(True)

        self.main_timer = QTimer(self)
        self.Idle_timer = 30000
        self.main_timer.timeout.connect(self.timeout_timer)
        self.main_timer.start(self.Idle_timer)  # changed timer timeout to 1s
        self.show()

    def begin(self):
        self.active=True
        self.main_timer.start(self.Idle_timer)

    def out(self):
        self.active=False
        self.main_timer.stop()


    def image_click(self,i):
        print("Clicked"+str(i))
        self.comm.goToIndividual.emit(i)


    def timeout_timer(self):
        self.out()
        self.comm.timeout.emit()

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
        self.setStyleSheet("background-color:blue;")
        self.c = Communicate()
        self.table_widget = ListApp(self,self.c)
        self.setCentralWidget(self.table_widget)
        self.showFullScreen()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())