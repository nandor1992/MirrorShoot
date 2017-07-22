import sys, os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QMainWindow, QScrollArea, QGridLayout,QDesktopWidget
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
        self.images = {}
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

    def addButton(self,image,size,rect):
        button=QPushButton(self)
        Icon_back_active = QIcon()
        Icon_back_active.addPixmap(QPixmap('../Resource/Image/'+image+'.png'), mode=QIcon.Disabled)
        Icon_back_active.addPixmap(QPixmap('../Resource/Image/'+image+'.png'), mode=QIcon.Active)
        button.setIcon(Icon_back_active)
        button.setIconSize(QSize(size, size))
        button.setGeometry(rect)
        button.setStyleSheet(self.bstyle)
        button.setFlat(True)
        return[button,Icon_back_active]

    def initUI(self):
        self.initScreen()
        self.bstyle = "QPushButton{background: transparent;outline: none;border: none}"
        # Button    border-width: 5px;padding: 5px;border-style:solid;border-radius: 5px

        # Button Exity
        size = max(self.width, self.height) / 10
        rect = QRect(size/3, self.height-size - size / 4, size + 20, size + 20)
        [self.button2,self.Icon_back_active]= self.addButton("back",size,rect)
        self.button2.clicked.connect(self.close_click)
        self.button2.pressed.connect(self.close_pressed)

        # Button Up
        rect=QRect(self.width/2-size/2-10, 20, size + 20, size + 20)
        [self.button_up,self.Icon_up]= self.addButton("up",size,rect)
        self.button_up.clicked.connect(self.up_click)
        self.button_up.pressed.connect(self.up_pressed)

        #Button Down
        rect=QRect(self.width/2-size/2-10, self.height  - size -size/4*3, size + 20, size + 20)
        [self.button_down,self.Icon_down]= self.addButton("down",size,rect)
        self.button_down.clicked.connect(self.down_click)
        self.button_down.pressed.connect(self.down_pressed)

        self.tab1 = QScrollArea(self)
        self.tab1.setStyleSheet("QScrollArea{background: transparent;outline: none;border: none}"+
                                    "QScrollBar:vertical{width: 0px; background: transparent;}")
        self.tab1.setGeometry(QRect(50,230,self.height-230 ,(self.height-230)*0.8))
        self.updateList()
        self.tab1.setWidgetResizable(True)

        if self.tab1.verticalScrollBar().maximum() ==0 and self.tab1.verticalScrollBar().minimum()==0:
            self.button_up.hide()
            self.button_down.hide()
        self.show()


    def updateList(self):
        if len(self.images)==0:
            #Init
            self.tab1_w = QWidget()
            self.tab1_layout = QGridLayout()
            self.tab1_layout.setColumnStretch(2, 3)
            self.tab1_w.setLayout(self.tab1_layout)
            # self.setWidgetResizable(True)
            onlyfiles = [f for f in listdir("../Resource/Photo") if isfile(join("../Resource/Photo", f))]
            cnt=0;
            self.images_list=onlyfiles
            for i in onlyfiles:
                if i!="show.jpg" and i!="test_image.jpg":
                    self.images[i] = QLabel(self)
                    pixmap = QPixmap("../Resource/Photo/"+i)
                    pixmap=pixmap.scaledToWidth((self.width-140)/3)
                    self.images[i].setPixmap(pixmap)
                    self.images[i].mouseReleaseEvent = lambda event, arg=i :self.image_click(arg)
                    self.tab1_layout.addWidget(self.images[i],int(cnt/3),int(divmod(cnt,3)[1]))
                    cnt += 1
            self.tab1.setWidget(self.tab1_w)
        else:
            #Update
            onlyfiles = [f for f in listdir("../Resource/Photo") if isfile(join("../Resource/Photo", f))]
            diff=list(set(onlyfiles).difference(self.images_list))
            cnt = len(self.images_list)-3
            self.images_list = onlyfiles
            print(diff)
            if len(diff)!=0:
                print("Diff found")
                for i in diff:
                        self.images[i] = QLabel(self)
                        pixmap = QPixmap("../Resource/Photo/" + i)
                        pixmap = pixmap.scaledToWidth((self.width - 140) / 3)
                        self.images[i].setPixmap(pixmap)
                        self.images[i].mouseReleaseEvent = lambda event, arg=i: self.image_click(arg)
                        self.tab1_layout.addWidget(self.images[i], int(cnt / 3), int(divmod(cnt, 3)[1]))
                        cnt += 1
        if self.tab1.verticalScrollBar().maximum() ==0 and self.tab1.verticalScrollBar().minimum()==0:
            self.button_up.hide()
            self.button_down.hide()
        else:
            self.button_up.show()
            self.button_down.show()

    def begin(self):
        self.active=True
        self.updateList()

    def out(self):
        self.active=False


    def image_click(self,i):
        self.comm.resetTimeout.emit()
        print("Clicked"+str(i))
        self.out()
        self.comm.goToIndividual.emit(i)


    @pyqtSlot()
    def close_click(self):
        self.comm.resetTimeout.emit()
        self.button2.setIcon(self.Icon_back_active)
        self.out()
        self.comm.goToMain.emit()

    @pyqtSlot()
    def close_pressed(self):
        self.button2.setIcon(QIcon('../Resource/Image/back_down.png'))

    @pyqtSlot()
    def up_click(self):
        self.comm.resetTimeout.emit()
        self.tab1.verticalScrollBar().setValue(self.tab1.verticalScrollBar().value() - self.height/10)
        if self.tab1.verticalScrollBar().minimum() >=self.tab1.verticalScrollBar().value():
            self.button_up.hide()
        self.button_down.show()
        self.button_up.setIcon(self.Icon_up)

    @pyqtSlot()
    def up_pressed(self):
        self.button_up.setIcon(QIcon('../Resource/Image/up_down.png'))

    @pyqtSlot()
    def down_click(self):
        self.comm.resetTimeout.emit()
        self.tab1.verticalScrollBar().setValue(self.tab1.verticalScrollBar().value() +self.height/10)
        if self.tab1.verticalScrollBar().maximum() <=self.tab1.verticalScrollBar().value():
            self.button_down.hide()
        self.button_up.show()
        self.button_down.setIcon(self.Icon_down)

    @pyqtSlot()
    def down_pressed(self):
        self.button_down.setIcon(QIcon('../Resource/Image/down_down.png'))


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