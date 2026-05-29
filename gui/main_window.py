
"""
Main Window GUI
"""

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QTabWidget,
)

from gui.convert_page import ConvertPage
from gui.reader_page import ReaderPage
from gui.ftp_page import FTPPage


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle(
            "Mail Management System"
        )

        self.setMinimumSize(1400, 900)

        self.init_ui()

    def init_ui(self):

        central_widget = QWidget()

        layout = QVBoxLayout()

        tabs = QTabWidget()

        tabs.addTab(
            ConvertPage(),
            "Convert"
        )

        tabs.addTab(
            ReaderPage(),
            "Reader"
        )

        tabs.addTab(
            FTPPage(),
            "Remote Explorer"
        )

        layout.addWidget(tabs)

        central_widget.setLayout(layout)

        self.setCentralWidget(
            central_widget
        )
