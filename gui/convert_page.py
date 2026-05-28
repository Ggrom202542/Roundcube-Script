

from pathlib import Path

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QFileDialog,
    QTextEdit,
    QLabel,
    QMessageBox,
    QHBoxLayout,
)

from services.convert_service import (
    convert_mail_file,
    convert_folder,
)


class ConvertPage(QWidget):
    def __init__(self):
        super().__init__()

        self.output_dir = "output"

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Buttons Layout
        button_layout = QHBoxLayout()

        self.btn_select_files = QPushButton("เลือกหลายไฟล์")
        self.btn_select_files.clicked.connect(self.select_files)

        self.btn_select_folder = QPushButton("เลือกทั้งโฟลเดอร์")
        self.btn_select_folder.clicked.connect(self.select_folder)

        self.btn_output = QPushButton("เลือกตำแหน่งจัดเก็บ")
        self.btn_output.clicked.connect(self.select_output_folder)

        button_layout.addWidget(self.btn_select_files)
        button_layout.addWidget(self.btn_select_folder)
        button_layout.addWidget(self.btn_output)

        # Output Path
        self.lbl_output = QLabel(f"Output Folder: {self.output_dir}")

        # Log Output
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)

        layout.addLayout(button_layout)
        layout.addWidget(self.lbl_output)
        layout.addWidget(self.log_output)

        self.setLayout(layout)

    def select_output_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self,
            "เลือกโฟลเดอร์จัดเก็บ"
        )

        if folder:
            self.output_dir = folder
            self.lbl_output.setText(
                f"Output Folder: {self.output_dir}"
            )

    def select_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "เลือกไฟล์ Mail"
        )

        if not files:
            return

        success = 0
        failed = 0

        for file_path in files:
            try:
                result = convert_mail_file(
                    file_path,
                    self.output_dir
                )

                self.log_output.append(
                    f"[SUCCESS] {result}"
                )

                success += 1

            except Exception as e:
                self.log_output.append(
                    f"[ERROR] {file_path}\n{str(e)}"
                )

                failed += 1

        QMessageBox.information(
            self,
            "เสร็จสิ้น",
            f"สำเร็จ: {success}\nล้มเหลว: {failed}"
        )

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self,
            "เลือกโฟลเดอร์ Mail"
        )

        if not folder:
            return

        try:
            results = convert_folder(
                folder,
                self.output_dir
            )

            for result in results:
                self.log_output.append(
                    f"[SUCCESS] {result}"
                )

            QMessageBox.information(
                self,
                "สำเร็จ",
                f"แปลงทั้งหมด {len(results)} ไฟล์"
            )

        except Exception as e:
            QMessageBox.critical(
                self,
                "ERROR",
                str(e)
            )