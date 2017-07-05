from PyQt5.QtWidgets import (QMessageBox, QApplication, QWidget, QToolTip, QPushButton,
                             QDesktopWidget, QMainWindow, QAction, qApp, QToolBar, QVBoxLayout,
                             QComboBox, QLabel, QLineEdit, QGridLayout, QMenuBar, QMenu, QStatusBar,
                             QTextEdit, QDialog, QFrame, QProgressBar
                             )
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import QIcon, QFont, QPixmap, QPalette
from PyQt5.QtCore import QCoreApplication, Qt, QBasicTimer, QTimer, QPoint
import PyQt5.QtWidgets, PyQt5.QtCore

import time, random, subprocess, sys, json


class cssden(QMainWindow):
    def __init__(self):
        super(cssden, self).__init__()

        self.mwidget = QMainWindow(self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self.setFixedSize(1400, 923)

        self.center()

        # timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.timer_)
        self.timer.start(1000)  # changed timer timeout to 1s

        # gif
        self.moviee = QLabel(self)
        self.movie = QtGui.QMovie("test.gif")
        self.moviee.setMovie(self.movie)
        self.moviee.setGeometry(5, -80, 380, 250)
        self.movie.start()
        self.show()

    def timer_(self):
        self.movie = QtGui.QMovie("test.gif")
        self.moviee.setMovie(self.movie)  # I added
        self.movie.start()  # those lines

    # center of the screen
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


app = QApplication(sys.argv)
app.setStyleSheet("QMainWindow{background-color: rgb(30,30,30);border: 1px solid black}")

ex = cssden()
sys.exit(app.exec_())