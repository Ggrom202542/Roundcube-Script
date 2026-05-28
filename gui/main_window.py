from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
)

from gui.convert_page import ConvertPage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Mail Document System")
        self.setMinimumSize(1000, 700)

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        layout = QVBoxLayout()

        title = QLabel("Mail Document System")
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            padding: 10px;
        """)

        layout.addWidget(title)

        self.convert_page = ConvertPage()
        layout.addWidget(self.convert_page)

        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)

