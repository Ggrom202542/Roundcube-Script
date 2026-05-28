
"""
EML Parser
"""

from pathlib import Path

from email import policy
from email.parser import BytesParser

from core.subject_decoder import (
    decode_mime_header,
)

from core.body_extractor import (
    extract_body,
)

from core.attachment_extractor import (
    get_attachments,
)


def parse_eml(file_path):

    file_path = Path(file_path)

    with open(file_path, "rb") as f:

        msg = BytesParser(
            policy=policy.default
        ).parse(f)

    body_data = extract_body(msg)

    attachments = get_attachments(msg)

    return {

        "filename": file_path.name,

        "file_size": round(
            file_path.stat().st_size / 1024,
            2
        ),

        "subject": decode_mime_header(
            msg.get("Subject")
        ),

        "from": decode_mime_header(
            msg.get("From")
        ),

        "to": decode_mime_header(
            msg.get("To")
        ),

        "cc": decode_mime_header(
            msg.get("Cc")
        ),

        "date": decode_mime_header(
            msg.get("Date")
        ),

        "body": body_data["plain"],

        "html": body_data["html"],

        "attachments": attachments,

        "attachment_count": len(
            attachments
        ),

        "content_type": msg.get_content_type(),

        "message_id": decode_mime_header(
            msg.get("Message-ID")
        ),
    }
