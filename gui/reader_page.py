
"""
Professional Reader Page
"""

import os

from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QFileDialog,
    QTextEdit,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QLineEdit,
    QSplitter,
    QTabWidget,
)

from services.mail_service import (
    read_eml,
    export_attachment,
)

from gui.html_viewer import HtmlViewer

from utils.recent_manager import (
    save_recent_folder,
    load_recent_folder,
)


class ReaderPage(QWidget):

    def __init__(self):
        super().__init__()

        self.current_data = None

        self.current_folder = ""

        self.init_ui()

        self.load_recent()

    def init_ui(self):

        main_layout = QVBoxLayout()

        # SEARCH
        self.search_box = QLineEdit()

        self.search_box.setPlaceholderText(
            "ค้นหาไฟล์..."
        )

        self.search_box.textChanged.connect(
            self.filter_files
        )

        # SPLITTER
        splitter = QSplitter()

        # LEFT PANEL
        left_widget = QWidget()

        left_layout = QVBoxLayout()

        self.btn_select_folder = QPushButton(
            "เลือกโฟลเดอร์ EML"
        )

        self.btn_select_folder.clicked.connect(
            self.select_folder
        )

        self.file_list = QListWidget()

        self.file_list.itemClicked.connect(
            self.load_selected_eml
        )

        left_layout.addWidget(
            self.btn_select_folder
        )

        left_layout.addWidget(
            self.search_box
        )

        left_layout.addWidget(
            self.file_list
        )

        left_widget.setLayout(
            left_layout
        )

        # RIGHT PANEL
        right_widget = QWidget()

        right_layout = QVBoxLayout()

        # METADATA
        self.lbl_subject = QLabel()
        self.lbl_from = QLabel()
        self.lbl_to = QLabel()
        self.lbl_date = QLabel()
        self.lbl_size = QLabel()
        self.lbl_attachment_count = QLabel()

        right_layout.addWidget(
            self.lbl_subject
        )

        right_layout.addWidget(
            self.lbl_from
        )

        right_layout.addWidget(
            self.lbl_to
        )

        right_layout.addWidget(
            self.lbl_date
        )

        right_layout.addWidget(
            self.lbl_size
        )

        right_layout.addWidget(
            self.lbl_attachment_count
        )

        # BODY TABS
        self.tabs = QTabWidget()

        self.body_text = QTextEdit()
        self.body_text.setReadOnly(True)

        self.html_viewer = HtmlViewer()

        self.tabs.addTab(
            self.body_text,
            "Text View"
        )

        self.tabs.addTab(
            self.html_viewer,
            "HTML View"
        )

        right_layout.addWidget(
            self.tabs
        )

        # ATTACHMENTS
        right_layout.addWidget(
            QLabel("Attachments")
        )

        self.attachment_list = QListWidget()

        self.attachment_list.itemDoubleClicked.connect(
            self.open_attachment
        )

        right_layout.addWidget(
            self.attachment_list
        )

        # BUTTONS
        button_layout = QHBoxLayout()

        self.btn_save_attachment = QPushButton(
            "ดาวน์โหลด"
        )

        self.btn_open_attachment = QPushButton(
            "เปิดไฟล์"
        )

        self.btn_save_attachment.clicked.connect(
            self.save_attachment
        )

        self.btn_open_attachment.clicked.connect(
            self.open_attachment
        )

        button_layout.addWidget(
            self.btn_save_attachment
        )

        button_layout.addWidget(
            self.btn_open_attachment
        )

        right_layout.addLayout(
            button_layout
        )

        right_widget.setLayout(
            right_layout
        )

        splitter.addWidget(left_widget)

        splitter.addWidget(right_widget)

        splitter.setSizes([300, 900])

        main_layout.addWidget(splitter)

        self.setLayout(main_layout)

        self.apply_style()

    def apply_style(self):

        self.setStyleSheet("""

            QWidget {
                font-size: 14px;
            }

            QPushButton {
                padding: 8px;
            }

            QListWidget {
                border: 1px solid #ccc;
            }

            QTextEdit {
                border: 1px solid #ccc;
            }

        """)

    def load_recent(self):

        folder = load_recent_folder()

        if folder and os.path.exists(folder):

            self.load_folder(folder)

    def select_folder(self):

        folder = QFileDialog.getExistingDirectory(
            self,
            "เลือกโฟลเดอร์"
        )

        if not folder:
            return

        self.load_folder(folder)

        save_recent_folder(folder)

    def load_folder(self, folder):

        self.current_folder = folder

        self.file_list.clear()

        for file_name in os.listdir(folder):

            if file_name.lower().endswith(
                ".eml"
            ):

                full_path = os.path.join(
                    folder,
                    file_name
                )

                item = QListWidgetItem(
                    file_name
                )

                item.setData(
                    Qt.UserRole,
                    full_path
                )

                self.file_list.addItem(
                    item
                )

    def filter_files(self):

        keyword = (
            self.search_box.text()
            .lower()
        )

        for i in range(
            self.file_list.count()
        ):

            item = self.file_list.item(i)

            item.setHidden(
                keyword not in item.text().lower()
            )

    def load_selected_eml(self, item):

        file_path = item.data(
            Qt.UserRole
        )

        try:

            data = read_eml(file_path)

            self.current_data = data

            self.lbl_subject.setText(
                f"Subject: {data['subject']}"
            )

            self.lbl_from.setText(
                f"From: {data['from']}"
            )

            self.lbl_to.setText(
                f"To: {data['to']}"
            )

            self.lbl_date.setText(
                f"Date: {data['date']}"
            )

            self.lbl_size.setText(
                f"File Size: "
                f"{data['file_size']} KB"
            )

            self.lbl_attachment_count.setText(
                f"Attachments: "
                f"{data['attachment_count']}"
            )

            self.body_text.setText(
                data["body"]
            )

            self.html_viewer.set_html(
                data["html"]
            )

            self.attachment_list.clear()

            for attachment in data[
                "attachments"
            ]:

                self.attachment_list.addItem(
                    attachment["filename"]
                )

        except Exception as e:

            QMessageBox.critical(
                self,
                "ERROR",
                str(e)
            )

    def get_selected_attachment(self):

        current_row = (
            self.attachment_list.currentRow()
        )

        if current_row < 0:
            return None

        return self.current_data[
            "attachments"
        ][current_row]

    def save_attachment(self):

        attachment = (
            self.get_selected_attachment()
        )

        if not attachment:

            QMessageBox.warning(
                self,
                "WARNING",
                "กรุณาเลือกไฟล์"
            )

            return

        folder = QFileDialog.getExistingDirectory(
            self,
            "เลือกโฟลเดอร์"
        )

        if not folder:
            return

        try:

            file_path = export_attachment(
                attachment,
                folder
            )

            QMessageBox.information(
                self,
                "SUCCESS",
                f"บันทึกแล้ว\n{file_path}"
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "ERROR",
                str(e)
            )

    def open_attachment(self):

        attachment = (
            self.get_selected_attachment()
        )

        if not attachment:
            return

        temp_dir = "temp"

        try:

            file_path = export_attachment(
                attachment,
                temp_dir
            )

            os.startfile(file_path)

        except Exception as e:

            QMessageBox.critical(
                self,
                "ERROR",
                str(e)
            )
