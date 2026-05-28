import re


def sanitize_filename(filename: str) -> str:
    """
    Remove invalid filename characters
    """

    filename = re.sub(r'[\\/*?:"<>|]', "_", filename)

    filename = filename.strip()

    return filename
