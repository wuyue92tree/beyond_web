import sys
from windows.ui import home
from windows import AboutWindow
from widgets.browsertabwidget import BrowserTabWidget
from widgets.downloadwidget import DownloadWidget
from widgets.interceptors import WebEngineUrlRequestInterceptor
from widgets.webengineview import WebEngineView
from PySide2 import QtCore
from PySide2.QtCore import Qt, QUrl
from PySide2.QtWidgets import (QApplication, QLabel, QLineEdit, QMainWindow)
from PySide2.QtWebEngineWidgets import (
    QWebEngineDownloadItem, QWebEnginePage
)

main_windows = []


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
        self._bookmark_dock.hide()

        # _tool_bar && actions
        self.actionBack.triggered.connect(self._tab_widget.back)
        self.actionForward.triggered.connect(self._tab_widget.forward)
        self.actionReload.triggered.connect(self._tab_widget.reload)
        self.actionUndo.triggered.connect(self._tab_widget.undo)
        self.actionRedo.triggered.connect(self._tab_widget.redo)
        self.actionCut.triggered.connect(self._tab_widget.cut)
        self.actionCopy.triggered.connect(self._tab_widget.copy)
        self.actionPaste.triggered.connect(self._tab_widget.paste)
        self.actionSelectAll.triggered.connect(self._tab_widget.select_all)
        self._actions = dict()
        self._actions[QWebEnginePage.Back] = self.actionBack
        self._actions[QWebEnginePage.Forward] = self.actionForward
        self._actions[QWebEnginePage.Reload] = self.actionReload
        self._actions[QWebEnginePage.Undo] = self.actionUndo
        self._actions[QWebEnginePage.Redo] = self.actionRedo
        self._actions[QWebEnginePage.Cut] = self.actionCut
        self._actions[QWebEnginePage.Copy] = self.actionCopy
        self._actions[QWebEnginePage.Paste] = self.actionPaste
        self._actions[QWebEnginePage.SelectAll] = self.actionSelectAll

        self._addres_line_edit = QLineEdit()
        self._addres_line_edit.setClearButtonEnabled(True)
        self._addres_line_edit.returnPressed.connect(self.load)
        self._tool_bar.insertWidget(self.actionSearch, self._addres_line_edit)
        self.actionSearch.triggered.connect(self.load)

        # _about_window
        self._about_window = AboutWindow(self)

        # _menu && actions
        self.menuWindow.insertAction(self.actionZoom_In,
                                     self._bookmark_dock.toggleViewAction())
        self.menuWindow.insertSeparator(self.actionZoom_In)
        self.actionExit.triggered.connect(QApplication.quit)
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
        self.actionAbout.triggered.connect(self._about_window.show)

        self._zoom_label = QLabel()
        self._status_bar.addPermanentWidget(self._zoom_label)
        self._update_zoom_label()

        # _bookmarks_tool_bar
        self.addToolBar(Qt.TopToolBarArea, self._bookmarks_tool_bar)
        self.insertToolBarBreak(self._bookmarks_tool_bar)
        self._bookmark_widget.changed.connect(self._update_bookmarks)
        self._update_bookmarks()

        # _find_tool_bar
        self._find_tool_bar.hide()
        self._find_tool_bar.find.connect(self._tab_widget.find)

        # web_engine_view interceptor
        self.interceptor = WebEngineUrlRequestInterceptor()

    def _update_bookmarks(self):
        self._bookmark_widget.populate_tool_bar(self._bookmarks_tool_bar)
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
        for old_download in self._status_bar.children():
            if type(old_download).__name__ == 'DownloadWidget' and \
                old_download.state() != QWebEngineDownloadItem.DownloadInProgress:
                self._status_bar.removeWidget(old_download)
                del old_download

        item.accept()
        download_widget = DownloadWidget(item)
        download_widget.remove_requested.connect(
            self._remove_download_requested,
            Qt.QueuedConnection)
        self._status_bar.addWidget(download_widget)

    def _remove_download_requested(self):
        download_widget = self.sender()
        self._status_bar.removeWidget(download_widget)
        del download_widget

    def _show_find(self):
        self._find_tool_bar.show()
        self._find_tool_bar.focus_find()

    def write_bookmarks(self):
        self._bookmark_widget.write_bookmarks()


def create_main_window():
    """Creates a MainWindow using 75% of the available screen resolution."""
    main_win = MainWindow()
    main_windows.append(main_win)
    available_geometry = QApplication.desktop().availableGeometry(main_win)
    main_win.resize(available_geometry.width() * 2 / 3,
                    available_geometry.height() * 3 / 4)
    main_win.show()
    return main_win


def create_main_window_with_browser():
    """Creates a MainWindow with a BrowserTabWidget."""
    main_win = create_main_window()
    return main_win.add_browser_tab()


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
