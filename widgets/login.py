# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/wuyue/Project/fun/beyond_web/ui/login.ui',
# licensing of '/Users/wuyue/Project/fun/beyond_web/ui/login.ui' applies.
#
# Created: Thu Nov 21 16:31:58 2019
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(540, 342)
        MainWindow.setMinimumSize(QtCore.QSize(540, 342))
        MainWindow.setMaximumSize(QtCore.QSize(540, 342))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setGeometry(QtCore.QRect(150, 260, 226, 32))
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.signInButton = QtWidgets.QPushButton(self.splitter)
        self.signInButton.setObjectName("signInButton")
        self.signUpButton = QtWidgets.QPushButton(self.splitter)
        self.signUpButton.setObjectName("signUpButton")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(60, 30, 421, 101))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.username = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.username.setObjectName("username")
        self.horizontalLayout.addWidget(self.username)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(60, 150, 421, 80))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.password = QtWidgets.QLineEdit(self.horizontalLayoutWidget_2)
        self.password.setObjectName("password")
        self.horizontalLayout_2.addWidget(self.password)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "User Login", None, -1))
        MainWindow.setWhatsThis(QtWidgets.QApplication.translate("MainWindow", "<html><head/><body><p>ffffffff</p></body></html>", None, -1))
        self.signInButton.setText(QtWidgets.QApplication.translate("MainWindow", "sign in", None, -1))
        self.signUpButton.setText(QtWidgets.QApplication.translate("MainWindow", "sign up", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("MainWindow", "Username", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("MainWindow", "Password", None, -1))

