
"""
Recent Folder Manager
"""

import json
from pathlib import Path


RECENT_FILE = (
    Path("config")
    / "recent.json"
)


def save_recent_folder(folder):

    RECENT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    data = {
        "recent_folder": folder
    }

    with open(
        RECENT_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=4
        )


def load_recent_folder():

    if not RECENT_FILE.exists():
        return ""

    try:

        with open(
            RECENT_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)

        return data.get(
            "recent_folder",
            ""
        )

    except:
        return ""
