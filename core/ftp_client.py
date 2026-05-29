
"""
FTP Client
"""

import os
from ftplib import FTP_TLS


class FTPClient:

    def __init__(
        self,
        host,
        username,
        password,
        port=21
    ):

        self.host = host
        self.username = username
        self.password = password
        self.port = port

        self.ftp = None

    def connect(self):

        self.ftp = FTP_TLS()

        self.ftp.connect(
            self.host,
            self.port
        )

        self.ftp.login(
            self.username,
            self.password
        )

        self.ftp.prot_p()

    def disconnect(self):

        if self.ftp:

            self.ftp.quit()

    def list_dir(self, path):

        self.ftp.cwd(path)

        return self.ftp.nlst()

    def download_file(
        self,
        remote_file,
        local_file
    ):

        os.makedirs(
            os.path.dirname(local_file),
            exist_ok=True
        )

        with open(local_file, "wb") as f:

            self.ftp.retrbinary(
                f"RETR {remote_file}",
                f.write
            )

    def get_size(self, file_name):

        try:
            return self.ftp.size(file_name)
        except:
            return 0
