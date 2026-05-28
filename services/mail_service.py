
"""
Mail Service
"""

from core.eml_parser import (
    parse_eml,
)

from core.attachment_extractor import (
    save_attachment,
)


def read_eml(file_path):

    return parse_eml(file_path)


def export_attachment(
    attachment,
    output_dir
):

    return save_attachment(
        attachment,
        output_dir
    )
