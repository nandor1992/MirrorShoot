import sys, os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QMainWindow,QDesktopWidget, QAction,QMenuBar,QScrollArea
from PyQt5.QtGui import QIcon, QMovie, QPixmap, QCursor
from PyQt5.QtCore import pyqtSlot, QSize, QRect, Qt, QTimer,QObject, pyqtSignal, QPoint
from tkinter import *
import time
import threading
import datetime
from PIL import Image
from Printer import Printer
from PhotoEdit import Editor
from os.path import isfile, join

from PyQt5.QtWidgets import QGridLayout


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
            self.screen2_diff=0
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
        pixmap=pixmap.scaledToWidth(self.width - 50)
        self.image.setGeometry(
            QRect(25, 50, self.width - 50, self.height - 350))
        self.image.setPixmap(pixmap)
        self.image.setAlignment(Qt.AlignTop)
        self.image.setAlignment(Qt.AlignLeft)
        self.image.hide()
        self.editor=Editor(self.base_dir+"/Resource/Photo/show.jpg",[pixmap.width(),pixmap.height()],(self.width - 140) / 5)

        self.frame = QLabel(self)
        pixmap = QPixmap("../Resource/Image/frame.png")
        pixmap=pixmap.scaledToWidth(self.width - 50)
        self.frame.setGeometry(
            QRect(25, 50, self.width - 25, self.height - 350))
        self.frame.setPixmap(pixmap)
        self.frame.setStyleSheet("QLabel{background: transparent;outline: none;border: none;}")
        self.frame.hide()

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

        # Button    border-width: 5px;padding: 5px;border-style:solid;border-radius: 5px
        self.button6 = QPushButton(self)
        self.edit_icon = QIcon()
        pixmap = QPixmap(self.base_dir + "/Resource/Image/edit.png")
        pixmap = pixmap.scaledToWidth(self.width / 5)
        self.edit_icon.addPixmap(pixmap, mode=QIcon.Disabled)
        self.edit_icon.addPixmap(pixmap, mode=QIcon.Active)
        self.button6.setIcon(self.edit_icon)
        self.button6.setIconSize(QSize(pixmap.width(), pixmap.height()))
        self.button6.setGeometry(
            QRect(self.width-50-pixmap.width(), 50 , pixmap.width() + 40,
                  pixmap.height() + 60))
        self.button6.clicked.connect(self.edit_click)
        self.button6.pressed.connect(self.edit_pressed)
        self.button6.setStyleSheet(self.bstyle)
        self.button6.hide()

        self.tab1 = QScrollArea(self)
        self.tab1.setStyleSheet("QScrollArea{background: transparent;outline: 2px;border: 2px}" +
                                "QScrollBar:vertical{width: 0px; background: transparent;}")
        self.tab1.setGeometry(QRect(250, 200, self.width - 280, self.height-200-400))
        self.tab1.setWidgetResizable(True)

        #Add Delete Grow and Shring, but delete first
        # Add Delete
        self.del_emoji = QLabel(self)
        self.del_emoji.setAlignment(Qt.AlignCenter)
        pixmap = QPixmap("../Resource/Image/delete.png")
        pixmap=pixmap.scaledToWidth(self.width / 4)
        self.del_emoji.setGeometry(QRect(0, self.height - 50 - pixmap.height(), self.width,
                  pixmap.height() + 50))
        self.del_emoji.setStyleSheet(
            "QLabel{background-color: rgba(255, 255, 255, 30);}")
        self.del_emoji.setPixmap(pixmap)
        self.del_emoji.hide()

        # Add Zoom
        self.zoom_emoji = QLabel(self)
        self.zoom_emoji.setAlignment(Qt.AlignCenter)
        pixmap = QPixmap("../Resource/Image/zoom.png")
        pixmap = pixmap.scaledToWidth(self.width / 4)
        self.zoom_emoji.setGeometry(QRect(self.width-pixmap.width()-20, self.height/2 - pixmap.height()+20, pixmap.width()+20,
                                         pixmap.height()+20))
        self.zoom_emoji.setStyleSheet(
            "QLabel{background-color: rgba(255, 255, 255, 40);}")
        self.zoom_emoji.setPixmap(pixmap)
        self.zoom_emoji.hide()

        self.add_emojis()

        self.addLoading()

    def add_emojis(self):
        self.images={}
        self.tab1_w = QWidget()
        self.tab1_w.setStyleSheet(
            "QWidget{background-color: rgba(255, 255, 255, 40);}")
        self.tab1_layout = QGridLayout()
        self.tab1_w.setLayout(self.tab1_layout)
        # self.setWidgetResizable(True)
        onlyfiles = [f for f in os.listdir("../Resource/Image/Emoji")]
        cnt = 0;
        self.emojis={}
        self.image_names={}
        self.e_cnt=0;
        self.add_pressed={}
        self.emoji_size={}
        self.images_list = onlyfiles
        for i in onlyfiles:
            self.images[i] = QLabel(self)
            pixmap = QPixmap("../Resource/Image/Emoji/" + i)
            pixmap = pixmap.scaledToWidth((self.width - 140) / 5)
            self.emoji_width=pixmap.width()
            self.emoji_height=pixmap.height()
            self.images[i].setPixmap(pixmap)
            self.images[i].mouseReleaseEvent = lambda event, arg=i: self.image_click(arg)
            self.tab1_layout.addWidget(self.images[i], int(cnt / 4), int(divmod(cnt, 4)[1]))
            cnt += 1
        self.tab1.setWidget(self.tab1_w)
        self.tab1.hide()

    def image_click(self,i):
        #self.comm.resetTimeout.emit()
        print("Clicked"+str(i))
        self.tab1.hide()
        self.alterButtons("hide")
        self.emojis[self.e_cnt]=QPushButton(self)
        pixmap = QPixmap(self.base_dir + "/Resource/Image/Emoji/"+i)
        pixmap = pixmap.scaledToWidth((self.width - 140) / 5)
        icon=QIcon()
        icon.addPixmap(pixmap, mode=QIcon.Disabled)
        self.image_names[self.e_cnt]=i
        self.emojis[self.e_cnt].setIcon(icon)
        self.emojis[self.e_cnt].setIconSize(QSize(pixmap.width(), pixmap.height()))
        self.emojis[self.e_cnt].setGeometry(
            QRect(self.width/2 - pixmap.width()/2, self.height/2 - pixmap.height()/2, pixmap.width(),
                  pixmap.height()))
        self.emojis[self.e_cnt].mousePressEvent = lambda event, arg=self.e_cnt: self.emoji_press(arg)
        self.emojis[self.e_cnt].mouseReleaseEvent = lambda event, arg=self.e_cnt: self.emoji_release(arg)
        self.emojis[self.e_cnt].setStyleSheet(self.bstyle)
        self.emojis[self.e_cnt].show()
        self.emoji_size[self.e_cnt] = 1.0
        self.add_pressed[self.e_cnt]=False
        self.e_cnt += 1

    def alterButtons(self,hide):
        if hide=="show":
            self.button.show()
            self.button.raise_()
            self.button2.show()
            self.button2.raise_()
            self.button3.show()
            self.button3.raise_()
            self.button4.show()
            self.button4.raise_()
            self.button5.show()
            self.button5.raise_()
            if len(self.emojis)!=0:
                self.button6.show()
                self.button6.raise_()
            self.del_emoji.hide()
            self.zoom_emoji.hide()
        else:
            self.del_emoji.show()
            self.zoom_emoji.show()
            self.button.hide()
            self.button2.hide()
            self.button3.hide()
            self.button4.hide()
            self.button5.hide()
            self.button6.hide()

    def emoji_press(self,i):
        try:
            self.alterButtons("hide")
            print("Pressed"+str(i))
            self.add_pressed[i] = True
            threading.Thread(target=self.Move_picture, kwargs={'cnt':i}).start()
        except:
            print("Error:"+str(sys.exc_info()[0]))

    def emoji_release(self,i):
        #self.comm.resetTimeout.emit()
        print("Released" + str(i))
        self.add_pressed[i] = False
        cursor = self.getAbsMouse()
        if cursor[1] > self.height - 220:
            self.emojis[i].hide()
            del self.emojis[i]
            self.alterButtons("show")
        if (cursor[0] > self.width - self.width / 4 + 50) and (cursor[1] < self.height / 2) and (cursor[1] > self.height / 4):
            if cursor[1] > self.height / 8*3:
                if self.emoji_size[i]>0.4:
                    self.emoji_size[i]=self.emoji_size[i]*0.9
            else:
                if self.emoji_size[i] <3:
                # between a and c  - > Zooom
                    self.emoji_size[i] = self.emoji_size[i] * 1.1

            pixmap = QPixmap(self.base_dir + "/Resource/Image/Emoji/"+self.image_names[i])
            pixmap = pixmap.scaledToWidth((self.width - 140) / 5*self.emoji_size[i])
            icon = QIcon()
            icon.addPixmap(pixmap, mode=QIcon.Disabled)
            self.emojis[i].setIcon(icon)
            self.emojis[i].setIconSize(QSize(pixmap.width(), pixmap.height()))
            self.emojis[i].setGeometry(
                QRect(cursor[0] - pixmap.width()/2-20, cursor[1] - pixmap.height()/2 -30,
                      pixmap.width() + 40,
                      pixmap.height() + 60))
            self.emojis[i].show()
        else:
            self.alterButtons("show")

    def Move_picture(self,cnt):
        while self.add_pressed[cnt]:
            try:
                cursor=self.getAbsMouse()
                self.emojis[cnt].setGeometry(
                QRect(cursor[0]-self.emoji_width/2*self.emoji_size[cnt]-20, cursor[1]- self.emoji_height/2*self.emoji_size[cnt]-30, self.emoji_width*self.emoji_size[cnt] + 40,
                    self.emoji_height*self.emoji_size[cnt] + 60))
            except:
                print("Error:" + str(sys.exc_info()[0]))

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
        self.editor.update(name)
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
        self.addExtras()
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

    @pyqtSlot()
    def save_click(self):
        self.addExtras()
       # self.comm.resetTimeout.emit()
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

    def addExtras(self):
        try:
            eName={}
            eSize={}
            ePos={}
            if not self.frame.isHidden():
                self.editor.addFrame(self.base_dir+"/Resource/Image/Frames/frame.png")
            for e in self.emojis:
                eName[e]=self.image_names[e]
                eSize[e]=self.emoji_size[e]
                rect=self.emojis[e].pos()
                ePos[e]=[rect.x(),rect.y()]
            if len(eName)!=0:
                self.editor.addEmojis(eName,eSize,ePos)
        except:
            print("Error:" + str(sys.exc_info()))

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
        #self.comm.resetTimeout.emit()
        print("PyQt5 frame add click")
        self.button4.setIcon(self.Icon_frame)
        if self.frame.isHidden():
            self.frame.show()
        else:
            self.frame.hide()

    @pyqtSlot()
    def frame_pressed(self):
        print('PyQt5 frame add pressed')
        self.button4.setIcon(QIcon(self.base_dir+"/Resource/Image/frame_button_down.png"))

    @pyqtSlot()
    def added_click(self):
        #self.comm.resetTimeout.emit()
        print("PyQt5 Added click")
        self.button5.setIcon(self.add_icon)
        if self.tab1.isHidden():
            self.tab1.show()
            self.tab1.raise_()
        else:
            self.tab1.hide()
        #self.add_pressed=False

    @pyqtSlot()
    def added_pressed(self):
        print('PyQt5 frame add pressed')
        self.button5.setIcon(QIcon(self.base_dir+"/Resource/Image/added_down.png"))

    @pyqtSlot()
    def edit_click(self):
        self.comm.resetTimeout.emit()
        self.button6.setIcon(self.edit_icon)
        self.alterButtons("hide")

    @pyqtSlot()
    def edit_pressed(self):
        print('PyQt5 frame add pressed')
        self.button6.setIcon(QIcon(self.base_dir+"/Resource/Image/edit_down.png"))


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