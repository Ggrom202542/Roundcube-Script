
"""
Remote Mail Explorer
Production Stable Version
"""

import os
import re
from datetime import datetime

from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QTextEdit,
    QFileDialog,
    QMessageBox,
    QSplitter,
    QAbstractItemView,
)

from services.ftp_service import (
    FTPService,
)


class FTPPage(QWidget):

    def __init__(self):
        super().__init__()

        self.ftp_service = None

        self.current_remote_path = ""

        self.current_selected_file = ""

        self.init_ui()

    def init_ui(self):

        main_layout = QVBoxLayout()

        # =========================
        # FTP LOGIN
        # =========================

        login_layout = QHBoxLayout()

        self.host_input = QLineEdit()

        self.host_input.setPlaceholderText(
            "FTP Host"
        )

        self.user_input = QLineEdit()

        self.user_input.setPlaceholderText(
            "FTP Username"
        )

        self.pass_input = QLineEdit()

        self.pass_input.setPlaceholderText(
            "FTP Password"
        )

        self.pass_input.setEchoMode(
            QLineEdit.Password
        )

        self.btn_connect = QPushButton(
            "CONNECT"
        )

        self.btn_connect.clicked.connect(
            self.connect_ftp
        )

        login_layout.addWidget(
            self.host_input
        )

        login_layout.addWidget(
            self.user_input
        )

        login_layout.addWidget(
            self.pass_input
        )

        login_layout.addWidget(
            self.btn_connect
        )

        main_layout.addLayout(
            login_layout
        )

        # =========================
        # MAIL USER
        # =========================

        user_layout = QHBoxLayout()

        self.mail_user_input = QLineEdit()

        self.mail_user_input.setPlaceholderText(
            "Mail User Folder"
        )

        self.btn_inbox = QPushButton(
            "INBOX"
        )

        self.btn_sent = QPushButton(
            "SENT"
        )

        self.btn_inbox.clicked.connect(
            self.load_inbox
        )

        self.btn_sent.clicked.connect(
            self.load_sent
        )

        user_layout.addWidget(
            self.mail_user_input
        )

        user_layout.addWidget(
            self.btn_inbox
        )

        user_layout.addWidget(
            self.btn_sent
        )

        main_layout.addLayout(
            user_layout
        )

        # =========================
        # STATUS
        # =========================

        self.status_label = QLabel(
            "🟢 Ready"
        )
        
        self.status_label.setFixedHeight(24)

        self.status_label.setStyleSheet("""

            QLabel {
                background-color: #2d2d2d;
                padding-left: 10px;
                border: 1px solid #444;
                font-size: 12px;
                color: #ddd;
            }

        """)

        main_layout.addWidget(
            self.status_label
        )

        # =========================
        # SPLITTER
        # =========================

        splitter = QSplitter()
        
        splitter.setChildrenCollapsible(
            False
        )

        splitter.setHandleWidth(8)


        # =========================
        # LEFT PANEL
        # =========================

        left_widget = QWidget()
        
        left_widget.setMinimumWidth(320)

        left_widget.setMaximumWidth(420)

        left_layout = QVBoxLayout()

        self.file_count_label = QLabel(
            "Files: 0"
        )

        self.file_list = QListWidget()
        
        self.file_list.setMinimumWidth(300)

        self.file_list.setUniformItemSizes(
            True
        )
        
        self.file_list.setStyleSheet("""

            QListWidget::item {
                padding: 6px;
                border-bottom: 1px solid #333;
            }

        """)

        self.file_list.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAsNeeded
        )
        
        self.file_list.setSelectionMode(
            QAbstractItemView.ExtendedSelection
        )

        self.file_list.itemClicked.connect(
            self.preview_selected
        )

        left_layout.addWidget(
            self.file_count_label
        )

        left_layout.addWidget(
            self.file_list
        )

        left_widget.setLayout(
            left_layout
        )

        # =========================
        # RIGHT PANEL
        # =========================

        right_widget = QWidget()
        
        right_widget.setMinimumWidth(600)

        right_layout = QVBoxLayout()

        self.lbl_subject = QLabel(
            "Subject:"
        )

        self.lbl_from = QLabel(
            "From:"
        )

        self.lbl_to = QLabel(
            "To:"
        )

        self.lbl_date = QLabel(
            "Date:"
        )

        self.lbl_size = QLabel(
            "Size:"
        )

        for label in [
            self.lbl_subject,
            self.lbl_from,
            self.lbl_to,
            self.lbl_date,
            self.lbl_size,
        ]:

            label.setWordWrap(True)

            label.setMinimumHeight(24)

            label.setMaximumHeight(50)

        self.lbl_from = QLabel()

        self.lbl_to = QLabel()

        self.lbl_date = QLabel()

        self.lbl_size = QLabel()

        self.body_text = QTextEdit()
        
        self.body_text.setMinimumHeight(
            250
        )

        self.body_text.setLineWrapMode(
            QTextEdit.WidgetWidth
        )
        
        self.attachment_label = QLabel(
            "Attachments: 0"
        )

        self.attachment_list = QListWidget()

        self.attachment_list.setFixedHeight(
            100
        )

        self.btn_download_attachment = QPushButton(
            "DOWNLOAD ATTACHMENT"
        )

        self.btn_download_attachment.clicked.connect(
            self.download_attachment
        )

        self.body_text.setReadOnly(True)

        self.btn_download = QPushButton(
            "DOWNLOAD SELECTED"
        )

        self.btn_download.clicked.connect(
            self.download_selected
        )

        # =========================
        # CONSOLE
        # =========================

        console_header = QHBoxLayout()

        console_header.addWidget(
            QLabel("Console Log")
        )

        self.btn_clear_console = QPushButton(
            "CLEAR"
        )

        self.btn_clear_console.clicked.connect(
            self.clear_console
        )

        console_header.addWidget(
            self.btn_clear_console
        )

        self.console = QTextEdit()

        self.console.setReadOnly(True)

        self.console.setMaximumHeight(180)

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
            self.body_text
        )
        
        right_layout.addWidget(
            self.attachment_label
        )

        right_layout.addWidget(
            self.attachment_list
        )

        right_layout.addWidget(
            self.btn_download_attachment
        )

        right_layout.addWidget(
            self.btn_download
        )

        right_layout.addLayout(
            console_header
        )

        right_layout.addWidget(
            self.console
        )

        right_widget.setLayout(
            right_layout
        )

        # =========================
        # SPLITTER CONFIG
        # =========================

        splitter.addWidget(
            left_widget
        )

        splitter.addWidget(
            right_widget
        )

        splitter.setStretchFactor(0, 0)

        splitter.setStretchFactor(1, 1)

        splitter.setSizes([340, 1000])

        main_layout.addWidget(
            splitter
        )

        self.setLayout(main_layout)

        self.apply_style()

    # =========================
    # STYLE
    # =========================

    def apply_style(self):

        self.setStyleSheet("""

            QWidget {
                font-size: 14px;
            }

            QPushButton {
                padding: 8px;
            }

            QTextEdit {
                border: 1px solid #ccc;
            }

            QListWidget {
                border: 1px solid #ccc;
            }
            
            QListWidget::item:selected {
                background-color: #505050;
                color: white;
            }

        """)

    # =========================
    # SAFE LOG
    # =========================

    def log(self, message):

        try:

            current_time = datetime.now().strftime(
                "%H:%M:%S"
            )

            self.console.append(
                f"[{current_time}] {message}"
            )

        except:
            pass

    # =========================
    # STATUS
    # =========================

    def set_status(
        self,
        text
    ):

        try:

            self.status_label.setText(
                text
            )

        except:
            pass

    # =========================
    # CLEAR CONSOLE
    # =========================

    def clear_console(self):

        try:

            self.console.clear()

        except:
            pass
        
    
    # =========================
    # FORMAT FILE SIZE
    # =========================

    def format_file_size(
        self,
        size
    ):

        try:

            size = float(size)

            units = [
                "B",
                "KB",
                "MB",
                "GB",
                "TB"
            ]

            unit_index = 0

            while (
                size >= 1024
                and unit_index < len(units) - 1
            ):

                size /= 1024

                unit_index += 1

            return (
                f"{size:.2f} "
                f"{units[unit_index]}"
            )

        except:

            return "0 B"
        
    # =========================
    # SAFE FILE NAME
    # =========================

    def make_safe_filename(
        self,
        filename
    ):

        filename = re.sub(
            r'[<>:"/\\\\|?*]',
            '_',
            filename
        )

        filename = filename.replace(
            "\n",
            ""
        )

        filename = filename.replace(
            "\r",
            ""
        )

        filename = filename.strip()

        # ป้องกันชื่อยาวเกิน
        if len(filename) > 180:
            filename = filename[:180]

        return filename

    # =========================
    # CONNECT FTP
    # =========================

    def connect_ftp(self):

        try:

            self.set_status(
                "🟡 Connecting..."
            )

            self.log(
                "Connecting FTP..."
            )

            self.ftp_service = FTPService(
                self.host_input.text(),
                self.user_input.text(),
                self.pass_input.text(),
            )

            self.ftp_service.connect()

            self.set_status(
                "🟢 Connected"
            )

            self.log(
                "FTP Connected"
            )

            QMessageBox.information(
                self,
                "SUCCESS",
                "FTP Connected"
            )

        except Exception as e:

            self.set_status(
                "🔴 Connection Failed"
            )

            self.log(
                f"Connection Error: {str(e)}"
            )

            QMessageBox.critical(
                self,
                "ERROR",
                str(e)
            )

    # =========================
    # LOAD INBOX
    # =========================

    def load_inbox(self):

        user = (
            self.mail_user_input.text()
            .strip()
        )

        if not user:

            QMessageBox.warning(
                self,
                "WARNING",
                "กรุณาระบุ User Folder"
            )

            return

        self.current_remote_path = (
            f"/{user}/Maildir/cur"
        )

        self.current_box = "INBOX"

        self.load_remote_files()

    # =========================
    # LOAD SENT
    # =========================

    def load_sent(self):

        user = (
            self.mail_user_input.text()
            .strip()
        )

        if not user:

            QMessageBox.warning(
                self,
                "WARNING",
                "กรุณาระบุ User Folder"
            )

            return

        self.current_remote_path = (
            f"/{user}/Maildir/.Sent/cur"
        )

        self.current_box = "SENT"

        self.load_remote_files()

    # =========================
    # LOAD REMOTE FILES
    # =========================

    def load_remote_files(self):

        try:

            self.set_status(
                "🟡 Loading Files..."
            )

            self.log(
                f"Loading Path: "
                f"{self.current_remote_path}"
            )

            self.file_list.clear()

            files = (
                self.ftp_service
                .list_mail_files(
                    self.current_remote_path
                )
            )

            count = 0

            for file_data in files:

                readable_size = (
                    self.format_file_size(
                        file_data["size"]
                    )
                )

                display_text = (
                    f"{file_data['name']}\n"
                    f"{readable_size} | "
                    f"{file_data['date']}"
                )

                item = QListWidgetItem(
                    display_text
                )

                item.setData(
                    Qt.UserRole,
                    file_data
                )

                self.file_list.addItem(
                    item
                )

                count += 1

            self.file_count_label.setText(
                f"Files: {count}"
            )

            self.set_status(
                f"🟢 {self.current_box} "
                f"| Loaded {count} files"
            )

            self.log(
                f"Loaded {count} files"
            )

        except Exception as e:

            self.set_status(
                "🔴 Load Failed"
            )

            self.log(
                f"Load Error: {str(e)}"
            )

            QMessageBox.critical(
                self,
                "ERROR",
                str(e)
            )

    # =========================
    # PREVIEW
    # =========================

    def preview_selected(self, item):

        try:

            file_data = item.data(
                Qt.UserRole
            )

            self.current_selected_file = (
                file_data["name"]
            )

            self.set_status(
                "🟡 Loading Preview..."
            )

            self.log(
                f"Downloading preview: "
                f"{file_data['name']}"
            )

            mail = (
                self.ftp_service
                .preview_mail(
                    self.current_remote_path,
                    file_data["name"]
                )
            )

            self.lbl_subject.setText(
                f"Subject: "
                f"{mail['subject']}"
            )

            self.lbl_from.setText(
                f"From: "
                f"{mail['from']}"
            )

            self.lbl_to.setText(
                f"To: "
                f"{mail['to']}"
            )

            self.lbl_date.setText(
                f"Date: "
                f"{mail['date']}"
            )

            readable_size = (
                self.format_file_size(
                    file_data["size"]
                )
            )

            self.lbl_size.setText(
                f"Size: "
                f"{readable_size}"
            )

            self.body_text.setText(
                mail["body"]
            )
            
            self.attachment_list.clear()

            attachments = mail.get(
                "attachments",
                []
            )

            self.attachment_label.setText(
                f"Attachments: "
                f"{len(attachments)}"
            )

            for attachment in attachments:

                self.attachment_list.addItem(
                    attachment["filename"]
                )

            self.set_status(
                f"🟢 {self.current_box} "
                f"| Preview Ready"
            )

            self.log(
                "Preview Loaded"
            )

        except Exception as e:

            self.set_status(
                "🔴 Preview Failed"
            )

            self.log(
                f"Preview Error: {str(e)}"
            )

            QMessageBox.critical(
                self,
                "ERROR",
                str(e)
            )

    # =========================
    # DOWNLOAD MULTIPLE
    # =========================

    def download_selected(self):

        selected_items = (
            self.file_list.selectedItems()
        )

        if not selected_items:

            QMessageBox.warning(
                self,
                "WARNING",
                "กรุณาเลือกไฟล์"
            )

            return

        save_dir = QFileDialog.getExistingDirectory(
            self,
            "Select Download Folder"
        )

        if not save_dir:
            return

        success_count = 0

        fail_count = 0

        self.set_status(
            "🟡 Downloading Files..."
        )

        self.log(
            f"Starting download "
            f"{len(selected_items)} files"
        )

        for item in selected_items:

            try:

                file_data = item.data(
                    Qt.UserRole
                )

                remote_name = (
                    file_data["name"]
                )

                safe_name = (
                    self.make_safe_filename(
                        remote_name
                    )
                )

                save_path = os.path.join(
                    save_dir,
                    safe_name + ".eml"
                )

                readable_size = (
                    self.format_file_size(
                        file_data["size"]
                    )
                )

                self.log(
                    f"Downloading: "
                    f"{remote_name} "
                    f"({readable_size})"
                )

                self.ftp_service.download_mail(
                    self.current_remote_path,
                    remote_name,
                    save_path
                )

                success_count += 1

            except Exception as e:

                fail_count += 1

                self.log(
                    f"Download Failed: "
                    f"{str(e)}"
                )

        self.set_status(
            f"🟢 Download Complete "
            f"({success_count} success)"
        )

        self.log(
            f"Download Complete "
            f"{success_count} success "
            f"{fail_count} failed"
        )

        QMessageBox.information(
            self,
            "DOWNLOAD COMPLETE",
            (
                f"Success: {success_count}\n"
                f"Failed: {fail_count}"
            )
        )
    
    # =========================
    # DOWNLOAD ATTACHMENT
    # =========================

    def download_attachment(self):

        selected_attachment = (
            self.attachment_list.currentItem()
        )

        if not selected_attachment:

            QMessageBox.warning(
                self,
                "WARNING",
                "กรุณาเลือก Attachment"
            )

            return

        filename = (
            selected_attachment.text()
        )

        save_file, _ = (
            QFileDialog.getSaveFileName(
                self,
                "Save Attachment",
                filename
            )
        )

        if not save_file:
            return

        try:

            self.set_status(
                "🟡 Downloading Attachment..."
            )

            self.ftp_service.download_attachment(
                save_file
            )

            self.set_status(
                "🟢 Attachment Downloaded"
            )

            self.log(
                f"Attachment Downloaded: "
                f"{filename}"
            )

            QMessageBox.information(
                self,
                "SUCCESS",
                "Attachment Downloaded"
            )

        except Exception as e:

            self.set_status(
                "🔴 Attachment Failed"
            )

            self.log(
                str(e)
            )

            QMessageBox.critical(
                self,
                "ERROR",
                str(e)
            )