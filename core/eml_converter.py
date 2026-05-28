
from pathlib import Path

from email import policy
from email.parser import BytesParser

from core.subject_decoder import decode_mime_header
from core.filename_sanitizer import sanitize_filename


def convert_to_eml(
    file_path: str,
    output_dir: str
) -> str:
    """
    Convert raw mail file to EML
    """

    raw_path = Path(file_path)

    with open(raw_path, "rb") as f:
        raw_data = f.read()

    # Parse email
    msg = BytesParser(
        policy=policy.default
    ).parsebytes(raw_data)

    # Decode subject
    subject = decode_mime_header(
        msg.get("Subject")
    )

    # Clean filename
    safe_subject = sanitize_filename(subject)

    if not safe_subject:
        safe_subject = "mail"

    output_path = Path(output_dir)

    output_path.mkdir(
        parents=True,
        exist_ok=True
    )

    # Prevent duplicate filename
    eml_file = output_path / f"{safe_subject}.eml"

    counter = 1

    while eml_file.exists():
        eml_file = output_path / (
            f"{safe_subject}_{counter}.eml"
        )
        counter += 1

    with open(eml_file, "wb") as f:
        f.write(raw_data)

    return str(eml_file)

