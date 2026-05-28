
"""
HTML Mail Viewer
"""

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
)

from PySide6.QtWebEngineWidgets import (
    QWebEngineView,
)


class HtmlViewer(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.browser = QWebEngineView()

        layout.addWidget(self.browser)

        self.setLayout(layout)

    def set_html(self, html):

        self.browser.setHtml(html)
