from PyQt5.QtWidgets import QMainWindow
from .ui import (
    about, login, urlcollector, history
)


class AboutWindow(QMainWindow, about.Ui_MainWindow):
    def __init__(self, parent=None):
        super(AboutWindow, self).__init__(parent)
        self.setupUi(self)


class LoginWindow(QMainWindow, login.Ui_MainWindow):
    def __init__(self, parent=None):
        super(LoginWindow, self).__init__(parent)
        self.setupUi(self)


class UrlCollectorWindow(QMainWindow, urlcollector.Ui_MainWindow):
    def __init__(self, parent=None):
        super(UrlCollectorWindow, self).__init__(parent)
        self.setupUi(self)


class HistoryWindow(QMainWindow, history.Ui_MainWindow):
    def __init__(self, parent=None):
        super(HistoryWindow, self).__init__(parent)
        self.setupUi(self)

