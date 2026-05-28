from email.header import decode_header


def decode_mime_header(value):
    """
    Decode MIME encoded header
    """

    if not value:
        return "no_subject"

    decoded_parts = decode_header(value)

    subject = ""

    for part, encoding in decoded_parts:
        if isinstance(part, bytes):
            subject += part.decode(
                encoding or "utf-8",
                errors="ignore"
            )
        else:
            subject += part

    return subject
