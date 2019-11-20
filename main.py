#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wuyue
@contact: wuyue92tree@163.com
@software: IntelliJ IDEA
@file: main2.py.py
@create at: 2019-11-19 15:16

这一行开始写关于本文件的说明与解释
"""

from PySide2 import QtCore, QtWidgets, QtWebEngineCore
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QMainWindow, QTabBar
from widgets import (home, login)

mainWins = []


def create_main_window(parent=None):
    main_win = MainWindow(parent)
    available_geometry = app.desktop().availableGeometry(main_win)
    main_win.resize(available_geometry.width() * 2 / 3,
                    available_geometry.height() * 3 / 4)
    main_win.show()
    mainWins.append(main_win)
    return main_win


class MainWindow(QMainWindow, home.Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.urlAddressLineEdit = QtWidgets.QLineEdit()
        self.urlAddressLineEdit.setText("https://www.baidu.com/")
        self.urlAddressLineEdit.setClearButtonEnabled(True)
        self.urlAddressLineEdit.returnPressed.connect(self.load)
        self.searchButton = QtWidgets.QPushButton('Search')
        self.searchButton.clicked.connect(self.load)
        self.toolBar.addWidget(self.urlAddressLineEdit)
        self.toolBar.addWidget(self.searchButton)
        if not parent:
            self.add_browser_tab()

        self.connect(self.browserTabWidget, QtCore.SIGNAL("url_changed(QUrl)"),
                     self.url_changed)

        self.actionBack.triggered.connect(self.browserTabWidget.back)
        self.actionForward.triggered.connect(self.browserTabWidget.forward)
        self.actionReload.triggered.connect(self.browserTabWidget.reload)

    def load(self):
        self.browserTabWidget.load(self.urlAddressLineEdit.text())

    def add_browser_tab(self):
        return self.browserTabWidget.add_browser_tab()

    def url_changed(self, url):
        self.urlAddressLineEdit.setText(url.toString())

    def create_main_window(self):
        create_main_window(parent=self)


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    main_win = create_main_window()
    sys.exit(app.exec_())
