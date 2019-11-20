from PySide2 import QtWebEngineWidgets


class WebEngineView(QtWebEngineWidgets.QWebEngineView):
    def __init__(self, parent=None):
        super(WebEngineView, self).__init__(parent)
        self.parent_obj = parent

    def createWindow(self, window_type):
        if window_type == QtWebEngineWidgets.QWebEnginePage.WebWindowType.WebBrowserTab:
            return self.parent_obj.add_browser_tab()
        # return self.parent().main_win.create_main_window()
