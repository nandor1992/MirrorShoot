import sys, os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QMainWindow,QDesktopWidget
from PyQt5.QtGui import QIcon, QMovie, QPixmap, QCursor
from PyQt5.QtCore import pyqtSlot, QSize, QRect, Qt, QTimer,QObject, pyqtSignal, QPoint
from tkinter import *
import time
import threading
import datetime
from PIL import Image
from Printer import Printer
from PhotoEdit import Editor

class showApp(QWidget):
    def __init__(self,parent,comm):
        super(QWidget,self).__init__(parent)
        self.title = 'Nandor Magic Mirror'
        self.lastTrigger = time.time()
        self.comm=comm
        self.comm.goToReview.connect(self.begin)
        self.active=False
        self.base_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
        self.print=Printer()
        self.editor=Editor(self.base_dir+"/Resource/Photo/show.jpg")
        self.add_pressed=False
        self.initUI()

    def initScreen(self):
        screen2 = QDesktopWidget().screenGeometry(1)
        screen1 = QDesktopWidget().screenGeometry(0)
        if screen2.right()>0:
            self.width = screen2.right()-screen2.left()
            self.height = screen2.bottom()
            self.screen2=True
            self.screen2_diff=screen2.left()
        else:
            self.screen2=False
            self.width = screen1.right()
            self.height = screen1.bottom()

    def getAbsMouse(self):
        if not self.screen2:
            return [QCursor.pos().x(),QCursor.pos().x()]
        else:
            return [QCursor.pos().x()-self.screen2_diff , QCursor.pos().y()]

    def initUI(self):
        self.initScreen()

        # Add image
        self.image = QLabel(self)
        pixmap = QPixmap("../Resource/Photo/show.jpg")
        pixmap.scaledToWidth(self.width - 50)
        self.image.setGeometry(
            QRect(25, 50, self.width - 25, self.height - 50))
        self.image.setPixmap(pixmap)
        self.image.hide()

        self.textLabel = QLabel(self)
        self.textLabel.setText("...Nothing")
        self.textLabel.setStyleSheet("QLabel{background: transparent;outline: none;border: none;color:white; font-size:42pt}")
        self.textLabel.setGeometry(QRect(self.width / 2 -100, self.height / 4, 300,80))
        self.textLabel.hide()
        self.bstyle = "QPushButton{background: transparent;outline: none;border: none}"

        # Button    border-width: 5px;padding: 5px;border-style:solid;border-radius: 5px
        self.button = QPushButton(self)
        self.Icon_save = QIcon()
        pixmap = QPixmap(self.base_dir+"/Resource/Image/save.png")
        pixmap = pixmap.scaledToWidth(self.width / 5)
        self.Icon_save.addPixmap(pixmap, mode=QIcon.Disabled)
        self.Icon_save.addPixmap(pixmap, mode=QIcon.Active)
        self.button.setIcon(self.Icon_save)
        self.button.setIconSize(QSize(pixmap.width(), pixmap.height()))
        self.button.setGeometry(
            QRect(25, self.height/10-pixmap.height()/2, pixmap.width() + 40,
                  pixmap.height() + 60))
        self.button.clicked.connect(self.save_click)
        self.button.pressed.connect(self.save_pressed)
        self.button.setStyleSheet(self.bstyle)

        # Button    border-width: 5px;padding: 5px;border-style:solid;border-radius: 5px
        self.button2 = QPushButton(self)
        self.Icon_print = QIcon()
        pixmap = QPixmap(self.base_dir+"/Resource/Image/print.png")
        pixmap = pixmap.scaledToWidth(self.width / 5)
        self.Icon_print.addPixmap(pixmap, mode=QIcon.Disabled)
        self.Icon_print.addPixmap(pixmap, mode=QIcon.Active)
        self.button2.setIcon(self.Icon_print)
        self.button2.setIconSize(QSize(pixmap.width(), pixmap.height()))
        self.button2.setGeometry(
            QRect(25, self.height/10+pixmap.height()/2 + 25 , pixmap.width() + 40,
                  pixmap.height() + 60))
        self.button2.clicked.connect(self.print_click)
        self.button2.pressed.connect(self.print_pressed)
        self.button2.setStyleSheet(self.bstyle)


        # Button    border-width: 5px;padding: 5px;border-style:solid;border-radius: 5px
        self.button3 = QPushButton(self)
        self.Icon_delete = QIcon()
        pixmap = QPixmap(self.base_dir+"/Resource/Image/delete.png")
        pixmap = pixmap.scaledToWidth(self.width / 5)
        self.Icon_delete.addPixmap(pixmap, mode=QIcon.Disabled)
        self.Icon_delete.addPixmap(pixmap, mode=QIcon.Active)
        self.button3.setIcon(self.Icon_delete)
        self.button3.setIconSize(QSize(pixmap.width(), pixmap.height()))
        self.button3.setGeometry(
            QRect(25, self.height/10+pixmap.height()/2*3 + 50, pixmap.width() + 40,
                  pixmap.height() + 60))
        self.button3.clicked.connect(self.delete_click)
        self.button3.pressed.connect(self.delete_pressed)
        self.button3.setStyleSheet(self.bstyle)

        # Button    border-width: 5px;padding: 5px;border-style:solid;border-radius: 5px
        self.button4 = QPushButton(self)
        self.Icon_frame = QIcon()
        pixmap = QPixmap(self.base_dir+"/Resource/Image/frame_button.png")
        pixmap = pixmap.scaledToWidth(self.width / 4)
        self.Icon_frame.addPixmap(pixmap, mode=QIcon.Disabled)
        self.Icon_frame.addPixmap(pixmap, mode=QIcon.Active)
        self.button4.setIcon(self.Icon_frame)
        self.button4.setIconSize(QSize(pixmap.width(), pixmap.height()))
        self.button4.setGeometry(
            QRect(50, self.height - 75 - pixmap.height() , pixmap.width() + 40,
                  pixmap.height() + 60))
        self.button4.clicked.connect(self.frame_click)
        self.button4.pressed.connect(self.frame_pressed)
        self.button4.setStyleSheet(self.bstyle)

        # Button    border-width: 5px;padding: 5px;border-style:solid;border-radius: 5px
        self.button5 = QPushButton(self)
        self.add_icon = QIcon()
        pixmap = QPixmap(self.base_dir + "/Resource/Image/added.png")
        pixmap = pixmap.scaledToWidth(self.width / 3.5)
        self.add_pic_width=pixmap.width()
        self.add_pic_height=pixmap.height()
        self.add_icon.addPixmap(pixmap, mode=QIcon.Disabled)
        self.add_icon.addPixmap(pixmap, mode=QIcon.Active)
        self.button5.setIcon(self.add_icon)
        self.button5.setIconSize(QSize(pixmap.width(), pixmap.height()))
        self.button5.setGeometry(
            QRect(self.width-50-pixmap.width(), self.height - 50 - pixmap.height(), pixmap.width() + 40,
                  pixmap.height() + 60))
        self.button5.clicked.connect(self.added_click)
        self.button5.pressed.connect(self.added_pressed)
        self.button5.setStyleSheet(self.bstyle)
        self.addLoading()

    def addLoading(self):
        self.moviee = QLabel(self)
        self.movie = QMovie("../Resource/Gif/load.gif")
        size = max(self.width, self.height) / 5
        diff = max(self.width, self.height) / 12
        self.movie.setScaledSize(self.scaleToWidth(size,self.movie))
        self.moviee.setMovie(self.movie)
        self.moviee.setGeometry(
            QRect(self.width / 2 - size / 2, self.height / 2 - size / 2 - diff, size + 20, size + 20))
        self.moviee.setAttribute(Qt.WA_TranslucentBackground)
        self.moviee.hide()

    def scaleToWidth(self,width,movie):
        movie.jumpToFrame(0)
        w=movie.currentPixmap().width()
        h=movie.currentPixmap().height()
        ratio=float(width/w)
        return QSize(w*ratio,h*ratio)

    def begin(self,name):
        self.active=True
        self.name=name
        self.editor=Editor(name)
        pixmap = QPixmap(name)
        pixmap = pixmap.scaledToWidth(self.width - 50)
        self.image.setPixmap(pixmap)
        self.image.show()
        self.ButtonsState(True)
        self.movie.stop()
        self.moviee.hide()
        self.movie.jumpToFrame(0)
        self.textLabel.hide()

    def out(self):
        self.active=False

    def goBack(self):
        print("Leaving Show Widget")
        self.out()
        self.comm.goToPicture.emit()

    def setTextSave(self):
        time.sleep(1.5)
        print("Saving")
        self.textLabel.setGeometry(QRect(self.width / 2 - 60, self.height / 4, 350, 100))
        self.movie.stop()
        self.moviee.hide()
        self.movie.jumpToFrame(0)
        threading.Thread(target=self.goBack).start()

    def setTextDelete(self):
        time.sleep(1.5)
        print("Deleting "+self.name)
        self.textLabel.setGeometry(QRect(self.width / 2 - 150, self.height / 4, 350, 100))
        try:
            os.remove(self.name)
        except:
            print("Exception Happend when Deleting: "+str(sys.exc_info()[0]))
        self.movie.stop()
        self.moviee.hide()
        self.movie.jumpToFrame(0)
        threading.Thread(target=self.goBack).start()


    @pyqtSlot()
    def print_click(self):
        self.comm.resetTimeout.emit()
        print("PyQt5 button1 click")
        self.button2.setIcon(self.Icon_print)
        self.ButtonsState(False)
        self.textLabel.setGeometry(QRect(self.width / 2 - 120, self.height / 4, 300, 100))
        self.textLabel.setText("...Printing")
        self.textLabel.show()
        self.comm.resetTimeout.emit()
        self.movie.jumpToFrame(0)
        self.moviee.show()
        self.movie.start()
        threading.Thread(target=self.print_photo, args=["show.jpg"]).start()

    def print_photo(self,name):
        self.print.printPhoto(name)
        self.textLabel.setGeometry(QRect(self.width / 2 - 150, self.height / 4, 350, 100))
        self.textLabel.setText("Printed!")
        #Add part wit hactuall printing of photo
        print("Leaving Show Widget")
        self.movie.stop()
        self.moviee.hide()
        self.movie.jumpToFrame(0)
        threading.Thread(target=self.goBack).start()

    @pyqtSlot()
    def print_pressed(self):
        print('PyQt5 button1 pressed')
        self.button2.setIcon(QIcon(self.base_dir+"/Resource/Image/print_down.png"))

    def print_photo(self,name):
        self.print.printPhoto(name)
        self.textLabel.setGeometry(QRect(self.width / 2 - 150, self.height / 4, 350, 100))
        self.textLabel.setText("Printed!")
        #Add part wit hactuall printing of photo
        print("Leaving Show Widget")
        time.sleep(0.5)
        self.goBack()

    @pyqtSlot()
    def print_pressed(self):
        print('PyQt5 button1 pressed')
        self.button2.setIcon(QIcon(self.base_dir+"/Resource/Image/print_down.png"))

    @pyqtSlot()
    def save_click(self):
        self.comm.resetTimeout.emit()
        print("PyQt5 button1 click")
        self.button.setIcon(self.Icon_save)
        self.ButtonsState(False)
        self.textLabel.setGeometry(QRect(self.width / 2 - 120, self.height / 4, 300, 100))
        self.textLabel.setText("...Saving")
        self.textLabel.show()
        self.movie.jumpToFrame(0)
        self.moviee.show()
        self.movie.start()
        threading.Thread(target=self.setTextSave).start()

    @pyqtSlot()
    def save_pressed(self):
        print('PyQt5 button1 pressed')
        self.button.setIcon(QIcon(self.base_dir+"/Resource/Image/save_down.png"))

    @pyqtSlot()
    def delete_click(self):
        self.comm.resetTimeout.emit()
        print("PyQt5 button1 click")
        self.button3.setIcon(self.Icon_delete)
        self.ButtonsState(False)
        self.textLabel.setGeometry(QRect(self.width / 2 - 150, self.height / 4, 350, 100))
        self.textLabel.setText("...Deleting")
        self.textLabel.show()
        self.movie.jumpToFrame(0)
        self.moviee.show()
        self.movie.start()
        threading.Thread(target=self.setTextDelete).start()

    @pyqtSlot()
    def delete_pressed(self):
        print('PyQt5 button1 pressed')
        self.button3.setIcon(QIcon(self.base_dir+"/Resource/Image/delete_down.png"))

    @pyqtSlot()
    def frame_click(self):
        self.comm.resetTimeout.emit()
        print("PyQt5 frame add click")
        self.button4.setIcon(self.Icon_frame)
        #self.movie.jumpToFrame(0)
        #self.moviee.show()
        #self.movie.start()
        self.ButtonsState(False)
        threading.Thread(target=self.frameSelect, args=[]).start()


    def frameSelect(self):
        if self.editor.stat=="Original":
            self.pImg=self.editor.addFrame(self.base_dir+"/Resource/Image/frame.png")
            pixmap = QPixmap(self.base_dir + "/Resource/Photo/edited.jpg")
            pixmap = pixmap.scaledToWidth(self.width - 200)
        else:
            pixmap = QPixmap(self.name)
            pixmap = pixmap.scaledToWidth(self.width - 200)
            self.editor.stat = "Original"
            time.sleep(0.1)
        #self.movie.stop()
        #self.moviee.hide()
        #self.movie.jumpToFrame(0)
        self.image.setPixmap(pixmap)
        self.ButtonsState(True)
        #Add part to add the Frame

    @pyqtSlot()
    def frame_pressed(self):
        print('PyQt5 frame add pressed')
        self.button4.setIcon(QIcon(self.base_dir+"/Resource/Image/frame_button_down.png"))

    @pyqtSlot()
    def added_click(self):
        #self.comm.resetTimeout.emit()
        print("PyQt5 Added click")
        self.button5.setIcon(self.add_icon)
        self.add_pressed=False

    @pyqtSlot()
    def added_pressed(self):
        print('PyQt5 frame add pressed')
        self.button5.setIcon(QIcon(self.base_dir+"/Resource/Image/added_down.png"))
        self.add_pressed = True
        threading.Thread(target=self.Move_picture).start()
            #self.setPos(event.scenePos() - QPoint(self.width / 2, self.height / 2))

    def Move_picture(self):
        while self.add_pressed:
            cursor=self.getAbsMouse()
            print(str(cursor))
            print("Moving")
            self.button5.setGeometry(
                QRect(cursor[0]-self.add_pic_width/2-20, cursor[1]- self.add_pic_height/2-30, self.add_pic_width + 40,
                  self.add_pic_height + 60))

    def ButtonsState(self,value):
        self.button.setEnabled(value)
        self.button2.setEnabled(value)
        self.button3.setEnabled(value)
        self.button4.setEnabled(value)
        self.button5.setEnabled(value)

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
        screen = QDesktopWidget().screenGeometry(1)
        if screen.right() > 0 and screen.bottom() > 0:
            self.move(screen.right(), screen.top())
        self.table_widget = showApp(self,self.c)
        self.table_widget.begin("../Resource/Photo/DSC_0098.JPG")
        self.setCentralWidget(self.table_widget)
        self.showFullScreen()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())