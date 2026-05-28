"""
Convert Page
"""

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QFileDialog,
    QTextEdit,
    QLabel,
    QMessageBox,
    QHBoxLayout,
    QProgressBar,
)

from gui.worker import ConvertWorker


class ConvertPage(QWidget):

    def __init__(self):
        super().__init__()

        self.output_dir = "output"

        self.worker = None

        self.init_ui()

    def init_ui(self):

        layout = QVBoxLayout()

        # Buttons
        button_layout = QHBoxLayout()

        self.btn_select_files = QPushButton(
            "เลือกหลายไฟล์"
        )

        self.btn_select_folder = QPushButton(
            "เลือกทั้งโฟลเดอร์"
        )

        self.btn_output = QPushButton(
            "เลือกตำแหน่งจัดเก็บ"
        )

        self.btn_select_files.clicked.connect(
            self.select_files
        )

        self.btn_select_folder.clicked.connect(
            self.select_folder
        )

        self.btn_output.clicked.connect(
            self.select_output_folder
        )

        button_layout.addWidget(
            self.btn_select_files
        )

        button_layout.addWidget(
            self.btn_select_folder
        )

        button_layout.addWidget(
            self.btn_output
        )

        # Output Label
        self.lbl_output = QLabel(
            f"Output Folder: {self.output_dir}"
        )

        # Status Label
        self.lbl_status = QLabel(
            "สถานะ: พร้อมทำงาน"
        )

        # Progress Bar
        self.progress = QProgressBar()
        self.progress.setRange(0, 0)
        self.progress.hide()

        # Log Output
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)

        layout.addLayout(button_layout)

        layout.addWidget(self.lbl_output)

        layout.addWidget(self.lbl_status)

        layout.addWidget(self.progress)

        layout.addWidget(self.log_output)

        self.setLayout(layout)

    def set_loading(self, loading: bool):

        self.btn_select_files.setDisabled(
            loading
        )

        self.btn_select_folder.setDisabled(
            loading
        )

        self.btn_output.setDisabled(
            loading
        )

        if loading:

            self.progress.show()

            self.lbl_status.setText(
                "สถานะ: กำลังประมวลผล..."
            )

        else:

            self.progress.hide()

            self.lbl_status.setText(
                "สถานะ: พร้อมทำงาน"
            )

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

        self.start_worker(
            mode="files",
            paths=files
        )

    def select_folder(self):

        folder = QFileDialog.getExistingDirectory(
            self,
            "เลือกโฟลเดอร์ Mail"
        )

        if not folder:
            return

        self.start_worker(
            mode="folder",
            paths=folder
        )

    def start_worker(
        self,
        mode,
        paths
    ):

        self.set_loading(True)

        self.worker = ConvertWorker(
            mode,
            paths,
            self.output_dir
        )

        self.worker.log_signal.connect(
            self.append_log
        )

        self.worker.result_signal.connect(
            self.show_result
        )

        self.worker.finished_signal.connect(
            self.worker_finished
        )

        self.worker.start()

    def append_log(self, message):

        self.log_output.append(message)

    def show_result(
        self,
        success,
        failed
    ):

        QMessageBox.information(
            self,
            "เสร็จสิ้น",
            f"สำเร็จ: {success}\n"
            f"ล้มเหลว: {failed}"
        )

    def worker_finished(self):

        self.set_loading(False)

