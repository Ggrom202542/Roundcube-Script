
"""
FTP Service
Production Stable Version
"""

import os
import ftplib
import email

from email.header import decode_header


class FTPService:

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

        self.current_attachments = []

    # =========================
    # CONNECT
    # =========================

    def connect(self):

        try:

            self.ftp = ftplib.FTP()

            self.ftp.connect(
                self.host,
                self.port,
                timeout=30
            )

            self.ftp.login(
                self.username,
                self.password
            )

            self.ftp.encoding = "utf-8"

            return True

        except Exception as e:

            raise Exception(
                f"FTP Connection Failed: "
                f"{str(e)}"
            )

    # =========================
    # CHECK CONNECTION
    # =========================

    def ensure_connection(self):

        if self.ftp is None:

            raise Exception(
                "FTP Not Connected"
            )

    # =========================
    # LIST MAIL FILES
    # =========================

    def list_mail_files(
        self,
        remote_path
    ):

        self.ensure_connection()

        files = []

        try:

            self.ftp.cwd(
                remote_path
            )

            lines = []

            self.ftp.retrlines(
                "LIST",
                lines.append
            )

            for line in lines:

                try:

                    parts = line.split()

                    if len(parts) < 9:
                        continue

                    filename = (
                        " ".join(parts[8:])
                    )

                    if (
                        filename == "."
                        or filename == ".."
                    ):
                        continue

                    size = parts[4]

                    date_str = (
                        " ".join(parts[5:8])
                    )

                    files.append({
                        "name": filename,
                        "size": size,
                        "date": date_str,
                    })

                except:
                    pass

            return files

        except Exception as e:

            raise Exception(
                f"Load Mail Files Failed: "
                f"{str(e)}"
            )

    # =========================
    # PREVIEW MAIL
    # =========================

    def preview_mail(
        self,
        remote_path,
        filename
    ):

        self.ensure_connection()

        temp_data = []

        remote_file = (
            f"{remote_path}/{filename}"
        )

        try:

            self.ftp.retrbinary(
                f"RETR {remote_file}",
                temp_data.append
            )

            raw_email = b"".join(
                temp_data
            )

            msg = email.message_from_bytes(
                raw_email
            )

            # =====================
            # HEADER
            # =====================

            subject = self.decode_mime(
                msg.get(
                    "Subject",
                    ""
                )
            )

            sender = self.decode_mime(
                msg.get(
                    "From",
                    ""
                )
            )

            to = self.decode_mime(
                msg.get(
                    "To",
                    ""
                )
            )

            date = msg.get(
                "Date",
                ""
            )

            body = ""

            attachments = []

            self.current_attachments = []

            # =====================
            # MULTIPART
            # =====================

            if msg.is_multipart():

                for part in msg.walk():

                    content_type = (
                        part.get_content_type()
                    )

                    disposition = str(
                        part.get(
                            "Content-Disposition",
                            ""
                        )
                    )

                    # =================
                    # BODY
                    # =================

                    if (
                        content_type
                        == "text/plain"
                        and "attachment"
                        not in disposition
                    ):

                        try:

                            charset = (
                                part.get_content_charset()
                                or "utf-8"
                            )

                            body = (
                                part.get_payload(
                                    decode=True
                                ).decode(
                                    charset,
                                    errors="ignore"
                                )
                            )

                        except:
                            pass

                    # =================
                    # ATTACHMENT
                    # =================

                    if (
                        "attachment"
                        in disposition.lower()
                    ):

                        attachment_name = (
                            part.get_filename()
                        )

                        if attachment_name:

                            attachment_name = (
                                self.decode_mime(
                                    attachment_name
                                )
                            )

                            file_data = (
                                part.get_payload(
                                    decode=True
                                )
                            )

                            attachment = {
                                "filename":
                                attachment_name,

                                "data":
                                file_data,
                            }

                            attachments.append(
                                attachment
                            )

                            self.current_attachments.append(
                                attachment
                            )

            else:

                try:

                    body = (
                        msg.get_payload(
                            decode=True
                        ).decode(
                            errors="ignore"
                        )
                    )

                except:
                    pass

            return {
                "subject": subject,
                "from": sender,
                "to": to,
                "date": date,
                "body": body,
                "attachments": attachments,
            }

        except Exception as e:

            raise Exception(
                f"Preview Mail Failed: "
                f"{str(e)}"
            )

    # =========================
    # DOWNLOAD MAIL
    # =========================

    def download_mail(
        self,
        remote_path,
        filename,
        save_path
    ):

        self.ensure_connection()

        remote_file = (
            f"{remote_path}/{filename}"
        )

        try:

            with open(
                save_path,
                "wb"
            ) as f:

                self.ftp.retrbinary(
                    f"RETR {remote_file}",
                    f.write
                )

        except Exception as e:

            raise Exception(
                f"Download Failed: "
                f"{str(e)}"
            )

    # =========================
    # DOWNLOAD ATTACHMENT
    # =========================

    def download_attachment(
        self,
        attachment_name,
        save_path
    ):

        for attachment in (
            self.current_attachments
        ):

            if (
                attachment["filename"]
                == attachment_name
            ):

                with open(
                    save_path,
                    "wb"
                ) as f:

                    f.write(
                        attachment["data"]
                    )

                return

        raise Exception(
            "Attachment Not Found"
        )

    # =========================
    # MIME DECODE
    # =========================

    def decode_mime(
        self,
        value
    ):

        try:

            decoded_parts = decode_header(
                value
            )

            decoded_string = ""

            for part, encoding in (
                decoded_parts
            ):

                if isinstance(
                    part,
                    bytes
                ):

                    decoded_string += (
                        part.decode(
                            encoding
                            or "utf-8",
                            errors="ignore"
                        )
                    )

                else:

                    decoded_string += part

            return decoded_string

        except:

            return value

    # =========================
    # DISCONNECT
    # =========================

    def disconnect(self):

        try:

            if self.ftp:

                self.ftp.quit()

                self.ftp = None

        except:
            pass
