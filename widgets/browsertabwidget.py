from PySide2 import QtWidgets, QtCore
from PySide2.QtCore import Qt, QUrl
from PySide2.QtWidgets import QTabBar
from widgets.webengineview import WebEngineView
from widgets.interceptors import WebEngineUrlRequestInterceptor


class BrowserTabWidget(QtWidgets.QTabWidget):
    url_changed = QtCore.Signal(QUrl)

    def __init__(self, parent=None):
        super(BrowserTabWidget, self).__init__(parent)
        self.setTabsClosable(True)
        # self.setMovable(True)
        self._web_engine_views = []
        tab_bar = self.tabBar()
        tab_bar.setSelectionBehaviorOnRemove(QTabBar.SelectPreviousTab)
        tab_bar.setContextMenuPolicy(Qt.CustomContextMenu)

        self.currentChanged.connect(self._current_changed)
        self.tabCloseRequested.connect(self._tab_close_requested)

    def _current_web_engine_view(self):
        index = self.currentIndex()
        return self._web_engine_views[index]

    def _current_changed(self):
        self.url_changed.emit(self._current_web_engine_view().url())

    def _tab_close_requested(self, index):
        self._web_engine_views.remove(self._web_engine_views[index])
        self.removeTab(index)

    def add_browser_tab(self):
        index = self.count()
        interceptor = WebEngineUrlRequestInterceptor()
        web_engine_view = WebEngineView(self)
        web_engine_view.page().profile().defaultProfile().setUrlRequestInterceptor(
            interceptor)
        web_engine_view.load(QtCore.QUrl('https://www.baidu.com'))
        self.addTab(web_engine_view, 'Tab-{}'.format(index))
        page = web_engine_view.page()
        page.titleChanged.connect(self._title_changed)
        # page.iconChanged.connect(self._icon_changed)
        # page.profile().downloadRequested.connect(self._download_requested)
        web_engine_view.urlChanged.connect(self._url_changed)
        # web_engine_view.enabled_changed.connect(self._enabled_changed)
        self._web_engine_views.append(web_engine_view)
        self.setCurrentIndex(index)
        return web_engine_view

    def _title_changed(self, title):
        self.setTabText(self.currentIndex(), title)

    def _url_changed(self, url):
        self.url_changed.emit(url)

    def load(self, url):
        self._current_web_engine_view().load(url)

    def back(self):
        self._current_web_engine_view().back()

    def forward(self):
        self._current_web_engine_view().forward()

    def reload(self):
        self._current_web_engine_view().reload()

