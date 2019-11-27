import sys
import os
import requests
from PyQt5.QtGui import QImage, QPixmap
from bs4 import BeautifulSoup
from PyQt5 import QtWidgets

from PyQt5.QtWebEngineWidgets import QWebEnginePage, QWebEngineView, \
    QWebEngineSettings

from PyQt5 import QtCore, QtWebEngineCore

from windows import ImagesWindow
from widgets.interceptors import WebEngineUrlRequestInterceptor

_web_actions = [QWebEnginePage.Back, QWebEnginePage.Forward,
                QWebEnginePage.Reload,
                QWebEnginePage.Undo, QWebEnginePage.Redo,
                QWebEnginePage.Cut, QWebEnginePage.Copy,
                QWebEnginePage.Paste, QWebEnginePage.SelectAll]

DEBUG_PORT = '5588'
DEBUG_URL = 'http://127.0.0.1:{}'.format(DEBUG_PORT)
os.environ['QTWEBENGINE_REMOTE_DEBUGGING'] = DEBUG_PORT


class WebEngineView(QWebEngineView):
    enabled_changed = QtCore.pyqtSignal(QWebEnginePage.WebAction, bool)

    @staticmethod
    def web_actions():
        return _web_actions

    @staticmethod
    def minimum_zoom_factor():
        return 0.25

    @staticmethod
    def maximum_zoom_factor():
        return 5

    def __init__(self, tab_factory_func, window_factory_func):
        super(WebEngineView, self).__init__()
        self._tab_factory_func = tab_factory_func
        self._window_factory_func = window_factory_func
        page = self.page()
        self._actions = {}
        for web_action in WebEngineView.web_actions():
            action = page.action(web_action)
            action.changed.connect(self._enabled_changed)
            self._actions[action] = web_action

        # web_engine_view interceptor
        self.interceptor = WebEngineUrlRequestInterceptor()
        page.profile().defaultProfile().setUrlRequestInterceptor(
            self.interceptor)

        # inspector
        self.inspector = None

        # enable plugins
        self.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)

        page.loadStarted.connect(self._load_started)
        page.loadFinished.connect(self._load_finished)
        self.html = ''

    def is_web_action_enabled(self, web_action):
        return self.page().action(web_action).isEnabled()

    def createWindow(self, window_type):
        if window_type == QWebEnginePage.WebBrowserTab or \
            window_type == QWebEnginePage.WebBrowserBackgroundTab:
            return self._tab_factory_func()
        return self._window_factory_func()

    def _enabled_changed(self):
        action = self.sender()
        web_action = self._actions[action]
        self.enabled_changed.emit(web_action, action.isEnabled())

    def call_inspector(self):
        if not self.inspector or self.inspector.isHidden():
            self.inspector = QWebEngineView()
            self.inspector.setWindowTitle('Web Inspector')
            self.inspector.load(QtCore.QUrl(DEBUG_URL))
            self.page().setDevToolsPage(self.inspector.page())
            self.inspector.show()
            self.inspector.raise_()
        else:
            self.inspector.close()
            self.inspector = None

    def render_options(self, id=None):
        widget = QtWidgets.QWidget()
        view_btn = QtWidgets.QPushButton('view')
        delete_btn = QtWidgets.QPushButton('delete')

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(view_btn)
        layout.addWidget(delete_btn)
        layout.setContentsMargins(5, 2, 5, 2)
        widget.setLayout(layout)
        return widget

    def call_images(self):
        images_window = ImagesWindow(self)
        # table_widgets = images_window.tableWidget()
        images = BeautifulSoup(self.html, 'html.parser').findAll('img')
        print(images)
        for image in images:
            row = images_window.tableWidget.rowCount()
            images_window.tableWidget.insertRow(row)
            image_url = image.get('src')
            if 'http' not in image_url:
                image_url = 'http:' + image_url
            image_content = requests.get(image_url).content
            img = QImage.fromData(image_content)
            print(img.width(), img.height())
            t_image_url = QtWidgets.QTableWidgetItem(image_url)
            t_image_width = QtWidgets.QTableWidgetItem(img.width())
            t_image_height = QtWidgets.QTableWidgetItem(img.height())
            images_window.tableWidget.setItem(row, 0, t_image_url)
            images_window.tableWidget.setItem(row, 1, t_image_width)
            images_window.tableWidget.setItem(row, 2, t_image_height)
            images_window.tableWidget.setCellWidget(row, 3,
                                                    self.render_options())
            # lab = QtWidgets.QLabel(images_window.scrollAreaWidgetContents)
            # lab.setPixmap(QPixmap.fromImage(img))
            # lab.move(0, img.height())
            # break

            print(image_url)
        images_window.show()

    def _load_started(self):
        # print('页面开始加载')
        pass

    def _load_finished(self, ok):
        if ok:
            self.page().toHtml(self.callable)

    def callable(self, data):
        self.html = data
