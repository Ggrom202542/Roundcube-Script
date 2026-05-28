
"""
Convert Service
"""

from pathlib import Path

from core.eml_converter import convert_to_eml


def convert_mail_file(
    file_path: str,
    output_dir: str
):
    """
    Convert single file
    """

    return convert_to_eml(
        file_path,
        output_dir
    )


def convert_folder(
    folder_path: str,
    output_dir: str
):
    """
    Convert all files in folder
    """

    folder = Path(folder_path)

    results = []

    for file in folder.iterdir():
        if file.is_file():
            try:
                result = convert_to_eml(
                    str(file),
                    output_dir
                )

                results.append(result)

            except Exception as e:
                print(e)

    return results

