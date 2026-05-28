
"""
Attachment Extractor
"""

from pathlib import Path

from core.subject_decoder import (
    decode_mime_header,
)


def get_attachments(msg):

    attachments = []

    for part in msg.walk():

        content_disposition = str(
            part.get("Content-Disposition")
        )

        if "attachment" not in content_disposition:
            continue

        filename = part.get_filename()

        if not filename:
            filename = "unknown_file"

        filename = decode_mime_header(
            filename
        )

        attachments.append({
            "filename": filename,
            "part": part,
        })

    return attachments


def save_attachment(
    attachment,
    output_dir
):

    output_path = Path(output_dir)

    output_path.mkdir(
        parents=True,
        exist_ok=True
    )

    filename = attachment["filename"]

    file_path = output_path / filename

    counter = 1

    while file_path.exists():

        stem = Path(filename).stem
        suffix = Path(filename).suffix

        file_path = (
            output_path
            / f"{stem}_{counter}{suffix}"
        )

        counter += 1

    payload = attachment[
        "part"
    ].get_payload(decode=True)

    with open(file_path, "wb") as f:
        f.write(payload)

    return str(file_path)
