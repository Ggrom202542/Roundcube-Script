from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QTabWidget,
)

from gui.convert_page import ConvertPage
from gui.reader_page import ReaderPage


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle(
            "Mail Document System"
        )

        self.setMinimumSize(1200, 800)

        self.init_ui()

    def init_ui(self):

        central_widget = QWidget()

        layout = QVBoxLayout()

        tabs = QTabWidget()

        tabs.addTab(
            ConvertPage(),
            "Convert Mail"
        )

        tabs.addTab(
            ReaderPage(),
            "EML Reader"
        )

        layout.addWidget(tabs)

        central_widget.setLayout(layout)

        self.setCentralWidget(
            central_widget
        )

