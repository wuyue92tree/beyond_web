from PyQt5 import QtWebEngineCore


class WebEngineUrlRequestInterceptor(
    QtWebEngineCore.QWebEngineUrlRequestInterceptor):
    def interceptRequest(self, info):
        url = info.requestUrl().toString()
        print(url)
