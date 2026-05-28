
"""
Background Worker Thread
"""

from PySide6.QtCore import (
    QThread,
    Signal,
)

from services.convert_service import (
    convert_mail_file,
    convert_folder,
)


class ConvertWorker(QThread):

    log_signal = Signal(str)
    finished_signal = Signal()
    result_signal = Signal(int, int)

    def __init__(
        self,
        mode,
        paths,
        output_dir
    ):
        super().__init__()

        self.mode = mode
        self.paths = paths
        self.output_dir = output_dir

    def run(self):

        success = 0
        failed = 0

        try:

            if self.mode == "files":

                total = len(self.paths)

                for index, file_path in enumerate(
                    self.paths,
                    start=1
                ):

                    try:

                        result = convert_mail_file(
                            file_path,
                            self.output_dir
                        )

                        self.log_signal.emit(
                            f"[{index}/{total}] SUCCESS\n{result}"
                        )

                        success += 1

                    except Exception as e:

                        self.log_signal.emit(
                            f"ERROR\n{file_path}\n{str(e)}"
                        )

                        failed += 1

            elif self.mode == "folder":

                results = convert_folder(
                    self.paths,
                    self.output_dir
                )

                success = len(results)

                for result in results:
                    self.log_signal.emit(
                        f"SUCCESS\n{result}"
                    )

        except Exception as e:

            self.log_signal.emit(str(e))

        self.result_signal.emit(success, failed)

        self.finished_signal.emit()
