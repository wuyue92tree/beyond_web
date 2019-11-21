import sys
from widgets.bookmarkwidget import BookmarkWidget
from widgets.browsertabwidget import BrowserTabWidget
from widgets.downloadwidget import DownloadWidget
from widgets.findtoolbar import FindToolBar
from widgets.interceptors import WebEngineUrlRequestInterceptor
from widgets.webengineview import QWebEnginePage, WebEngineView
from PySide2 import QtCore, QtWebEngineCore
from PySide2.QtCore import Qt, QUrl
from PySide2.QtGui import QCloseEvent, QKeySequence, QIcon
from PySide2.QtWidgets import (qApp, QAction, QApplication, QDesktopWidget,
                               QDockWidget, QLabel, QLineEdit, QMainWindow,
                               QMenu, QMenuBar, QPushButton,
                               QStatusBar, QToolBar)
from PySide2.QtWebEngineWidgets import (QWebEngineDownloadItem, QWebEnginePage,
                                        QWebEngineView)

from widgets import (home, login)

main_windows = []


def create_main_window():
    """Creates a MainWindow using 75% of the available screen resolution."""
    main_win = MainWindow()
    main_windows.append(main_win)
    available_geometry = app.desktop().availableGeometry(main_win)
    main_win.resize(available_geometry.width() * 2 / 3,
                    available_geometry.height() * 3 / 4)
    main_win.show()
    return main_win


def create_main_window_with_browser():
    """Creates a MainWindow with a BrowserTabWidget."""
    main_win = create_main_window()
    return main_win.add_browser_tab()


class MainWindow(QMainWindow, home.Ui_MainWindow):
    """Provides the parent window that includes the BookmarkWidget,
    BrowserTabWidget, and a DownloadWidget, to offer the complete
    web browsing experience."""

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self._tab_widget = BrowserTabWidget(create_main_window_with_browser)
        self._tab_widget.enabled_changed.connect(self._enabled_changed)
        self._tab_widget.download_requested.connect(self._download_requested)
        self.setCentralWidget(self._tab_widget)
        self.connect(self._tab_widget, QtCore.SIGNAL("url_changed(QUrl)"),
                     self.url_changed)

        # _bookmark_dock && _bookmark_widget
        self._bookmark_widget.open_bookmark.connect(self.load_url)
        self._bookmark_widget.open_bookmark_in_new_tab.connect(
            self.load_url_in_new_tab)
        self._bookmark_dock.setWidget(self._bookmark_widget)
        self.addDockWidget(Qt.LeftDockWidgetArea, self._bookmark_dock)

        self._find_tool_bar = None

        # _tool_bar && actions
        self.actionBack.triggered.connect(self._tab_widget.back)
        self.actionForward.triggered.connect(self._tab_widget.forward)
        self.actionReload.triggered.connect(self._tab_widget.reload)
        self._actions = self._tool_bar.actions()

        self._addres_line_edit = QLineEdit()
        self._addres_line_edit.setClearButtonEnabled(True)
        self._addres_line_edit.returnPressed.connect(self.load)
        self._tool_bar.addWidget(self._addres_line_edit)

        self._search_button = QPushButton('Search')
        self._search_button.clicked.connect(self.load)
        self._tool_bar.addWidget(self._search_button)

        # _menu && actions
        self.menuWindow.insertAction(self.actionZoom_In,
                                     self._bookmark_dock.toggleViewAction())
        self.menuWindow.insertSeparator(self.actionZoom_In)
        self.actionExit.triggered.connect(qApp.quit)
        self.actionNew_Tab.triggered.connect(self.add_browser_tab)
        self.actionClose_Current_Tab.triggered.connect(self._close_current_tab)
        self.actionHistory.triggered.connect(self._tab_widget.show_history)
        self.actionFind.triggered.connect(self._show_find)
        self.actionAdd_Bookmark.triggered.connect(self._add_bookmark)
        self.actionAdd_Bookmark_to_Tool_Bar.triggered.connect(
            self._add_tool_bar_bookmark)
        self.actionOpen_Downloads.triggered.connect(
            DownloadWidget.open_download_directory)
        self.actionZoom_In.triggered.connect(self._zoom_in)
        self.actionZoom_Out.triggered.connect(self._zoom_out)
        self.actionReset_Zoom.triggered.connect(self._reset_zoom)
        self.actionAbout.triggered.connect(qApp.aboutQt)

        self._zoom_label = QLabel()
        self.statusBar().addPermanentWidget(self._zoom_label)
        self._update_zoom_label()

        # _bookmarksToolBar
        self.addToolBar(Qt.TopToolBarArea, self._bookmarksToolBar)
        self.insertToolBarBreak(self._bookmarksToolBar)
        self._bookmark_widget.changed.connect(self._update_bookmarks)
        self._update_bookmarks()
        self.interceptor = WebEngineUrlRequestInterceptor()

    def _update_bookmarks(self):
        self._bookmark_widget.populate_tool_bar(self._bookmarksToolBar)
        self._bookmark_widget.populate_other(self.menuBookmarks, 3)

    def add_browser_tab(self):
        browser_tab = self._tab_widget.add_browser_tab()
        browser_tab.page().profile().defaultProfile().setUrlRequestInterceptor(
            self.interceptor)
        return browser_tab

    def _close_current_tab(self):
        if self._tab_widget.count() > 1:
            self._tab_widget.close_current_tab()
        else:
            self.close()

    def close_event(self, event):
        main_windows.remove(self)
        event.accept()

    def load(self):
        url_string = self._addres_line_edit.text().strip()
        if url_string:
            self.load_url_string(url_string)

    def load_url_string(self, url_s):
        url = QUrl.fromUserInput(url_s)
        if (url.isValid()):
            self.load_url(url)

    def load_url(self, url):
        self._tab_widget.load(url)

    def load_url_in_new_tab(self, url):
        self.add_browser_tab().load(url)

    def url_changed(self, url):
        self._addres_line_edit.setText(url.toString())

    def _enabled_changed(self, web_action, enabled):
        # print(web_action)
        return
        action = self._actions[web_action]
        if action:
            action.setEnabled(enabled)

    def _add_bookmark(self):
        index = self._tab_widget.currentIndex()
        if index >= 0:
            url = self._tab_widget.url()
            title = self._tab_widget.tabText(index)
            icon = self._tab_widget.tabIcon(index)
            self._bookmark_widget.add_bookmark(url, title, icon)

    def _add_tool_bar_bookmark(self):
        index = self._tab_widget.currentIndex()
        if index >= 0:
            url = self._tab_widget.url()
            title = self._tab_widget.tabText(index)
            icon = self._tab_widget.tabIcon(index)
            self._bookmark_widget.add_tool_bar_bookmark(url, title, icon)

    def _zoom_in(self):
        new_zoom = self._tab_widget.zoom_factor() * 1.5
        if (new_zoom <= WebEngineView.maximum_zoom_factor()):
            self._tab_widget.set_zoom_factor(new_zoom)
            self._update_zoom_label()

    def _zoom_out(self):
        new_zoom = self._tab_widget.zoom_factor() / 1.5
        if (new_zoom >= WebEngineView.minimum_zoom_factor()):
            self._tab_widget.set_zoom_factor(new_zoom)
            self._update_zoom_label()

    def _reset_zoom(self):
        self._tab_widget.set_zoom_factor(1)
        self._update_zoom_label()

    def _update_zoom_label(self):
        percent = int(self._tab_widget.zoom_factor() * 100)
        self._zoom_label.setText("{}%".format(percent))

    def _download_requested(self, item):
        # Remove old downloads before opening a new one
        for old_download in self.statusBar().children():
            if type(old_download).__name__ == 'download_widget' and \
                old_download.state() != QWebEngineDownloadItem.DownloadInProgress:
                self.statusBar().removeWidget(old_download)
                del old_download

        item.accept()
        download_widget = download_widget(item)
        download_widget.removeRequested.connect(self._remove_download_requested,
                                                Qt.QueuedConnection)
        self.statusBar().addWidget(download_widget)

    def _remove_download_requested(self):
        download_widget = self.sender()
        self.statusBar().removeWidget(download_widget)
        del download_widget

    def _show_find(self):
        if self._find_tool_bar is None:
            self._find_tool_bar = FindToolBar()
            self._find_tool_bar.find.connect(self._tab_widget.find)
            self.addToolBar(Qt.BottomToolBarArea, self._find_tool_bar)
        else:
            self._find_tool_bar.show()
        self._find_tool_bar.focus_find()

    def write_bookmarks(self):
        self._bookmark_widget.write_bookmarks()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = create_main_window()
    initial_urls = sys.argv[1:]
    if not initial_urls:
        initial_urls.append('https://www.baidu.com')
    for url in initial_urls:
        main_win.load_url_in_new_tab(QUrl.fromUserInput(url))
    exit_code = app.exec_()
    main_win.write_bookmarks()
    sys.exit(exit_code)
